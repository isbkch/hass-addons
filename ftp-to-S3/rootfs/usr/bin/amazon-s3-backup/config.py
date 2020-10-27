import os
from pathlib import Path


class ConfigError(Exception):
    pass


class Config:
    DEFAULT_STORAGE_CLASS = "STANDARD"
    DEFAULT_UPLOAD_MISSING_FILES = "false"
    DEFAULT_MONITOR_PATH = "/root/backup"

    VALID_STORAGE_CLASSES = [
        "STANDARD",
        "REDUCED_REDUNDANCY",
        "STANDARD_IA",
        "ONEZONE_IA",
        "INTELLIGENT_TIERING",
        "GLACIER",
        "DEEP_ARCHIVE"
    ]

    def __init__(self):
        self.bucket_name = os.getenv("bucket_name")
        self.bucket_region = os.getenv("bucket_region")
        self.storage_class = os.getenv(
            "storage_class", Config.DEFAULT_STORAGE_CLASS)
        self.upload_missing_files = True if os.getenv(
            "upload_missing_files", Config.DEFAULT_UPLOAD_MISSING_FILES).lower() == "true" else False

        try:
            self.keep_local_recordings = int(os.getenv("keep_local_recordings"))
        except (TypeError, ValueError) as err:
            self.keep_local_recordings = None

        self.monitor_path = Path(
            os.getenv("monitor_path", Config.DEFAULT_MONITOR_PATH))

        self.validate()

    def validate(self):
        if not len(self.bucket_name) > 0:
            raise ConfigError("bucket_name must be specified")

        if not len(self.bucket_name) > 0:
            raise ConfigError("bucket_region must be specified")

        if not self.storage_class in Config.VALID_STORAGE_CLASSES:
            raise ConfigError(
                f"Invalid S3 storage class specified: {self.storage_class}")

        if self.keep_local_recordings is not None:
            if self.keep_local_recordings < 0:
                raise ConfigError(
                    "keep_local_recordings must be greater than zero")

        if not self.monitor_path.exists():
            raise ConfigError(
                f"monitor_path does not exist: {self.monitor_path}")
