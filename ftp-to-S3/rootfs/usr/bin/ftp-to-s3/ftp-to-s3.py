import sys
import time
from pathlib import Path
import logging
import os
import datetime

from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler

from config import Config, ConfigError
from s3bucket import S3Bucket, S3BucketError

logging.basicConfig()
logger = logging.getLogger(__name__)

class BackupEventHandler(RegexMatchingEventHandler):
    BACKUP_REGEX = [r".+\.*$"]

    def __init__(self, config: Config, s3_bucket: S3Bucket):
        """Handle new files in the Hass backup directory

        Args:
            s3_bucket (S3Bucket): S3 bucket to upload files to
        """
        super().__init__(self.BACKUP_REGEX)
        self.config = config
        self.s3_bucket = s3_bucket

    def on_created(self, event):
        self.process(event)

    def process(self, event):
        """Process a new file

        Args:
            event:
        """
        logger.info(f"Processing new file {event.src_path}")

        file_size = -1
        while file_size != os.path.getsize(event.src_path):
            file_size = os.path.getsize(event.src_path)
            time.sleep(1)

        file_name = Path(event.src_path).name
        slug = Path(event.src_path).stem

        try:
            upload_file(Path(event.src_path),
                        self.s3_bucket)
        except S3BucketError as err:
            logger.exception(f"Error uploading file: {err}")


class FileWatcher:
    def __init__(self, config: Config, s3_bucket: S3Bucket):
        """Watch for new files in the backup directory

        Args:
            monitor_path (str): Path to monitor for new files
            s3_bucket (S3Bucket): S3 bucket to upload files to
        """
        self.config = config
        self.event_handler = BackupEventHandler(
            config, s3_bucket)
        self.event_observer = Observer()

    def run(self):
        self.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def start(self):
        self.schedule()
        self.event_observer.start()

    def stop(self):
        self.event_observer.stop()
        self.event_observer.join()

    def schedule(self):
        logger.info(
            f"Monitoring path {self.config.monitor_path} for new uploads")
        self.event_observer.schedule(
            self.event_handler,
            str(self.config.monitor_path),
            recursive=True
        )


def set_log_level(hass_log_level: str):
    """Set this script's log level based on the level set in the HASS config for this addon

    Args:
        hass_log_level (str): A log level (1-8)
    """
    if hass_log_level:
        hass_log_level = hass_log_level.strip()

    level_map = {
        "8": logging.NOTSET,
        "7": logging.DEBUG,
        "6": logging.DEBUG,
        "5": logging.INFO,
        "4": logging.INFO,
        "3": logging.WARNING,
        "2": logging.ERROR,
        "1": logging.CRITICAL
    }
    logger.setLevel(level_map.get(hass_log_level, logging.NOTSET))


def upload_file(file: Path, s3_bucket: S3Bucket):
    s3_bucket.upload_file(str(file))
    # s3_bucket.sync_files()


if __name__ == "__main__":
    set_log_level(os.environ.get("LOG_LEVEL"))

    try:
        config = Config()
    except ConfigError as err:
        logger.critical(f"Configuration error: {err}")
        sys.exit(1)

    s3_bucket = S3Bucket(config.bucket_name,
                         config.bucket_region, config.storage_class)

    bucket_contents = []
    try:
        bucket_contents = s3_bucket.list_bucket()
    except Exception:
        logger.critical("Error listing contents of S3 bucket!")
        sys.exit(1)

    local_files = [x.name for x in config.monitor_path.iterdir()
                   if x.is_file()]

    for local_file in local_files:
        file = Path(config.monitor_path, local_file)
        file_size = file.stat().st_size
        found_in_s3 = [f for f in bucket_contents if f.get(
            "name") == str(file).lstrip("/")]
        if len(found_in_s3) > 0:
            if file_size == found_in_s3[0]["size"]:
                logger.debug(
                    f"Local file {file} found in S3 with matching size of {file_size} bytes")
            else:
                logger.warning(
                    f"Local file {file} does not match the file in S3")
                try:
                    upload_file(file, s3_bucket)
                except S3BucketError as err:
                    logger.exception(f"Error uploading file: {err}")
        else:
            logger.warning(
                f"Local file {file} not found in S3")
            if config.upload_missing_files:
                try:
                    upload_file(file, s3_bucket)
                except S3BucketError as err:
                    logger.exception(f"Error uploading file: {err}")

    FileWatcher(config, s3_bucket).run()
