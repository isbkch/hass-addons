import logging
from typing import List
import boto3

logger = logging.getLogger(__name__)


class S3BucketError(Exception):
    pass


class S3Bucket:
    def __init__(self, bucket_name: str, bucket_region: str, storage_class: str):
        """Class representing an S3 bucket

        Args:
            bucket_name (str): Name of S3 bucket
            bucket_region (str): AWS region in which the bucket lives
            storage_class (str): S3 storage class to use for uploads
        """
        self.bucket_name = bucket_name
        self.storage_class = storage_class

        aws_config = {
            "region_name": bucket_region
        }
        logger.debug("Creating S3 client")
        self.s3_client = boto3.client("s3", **aws_config)

    def list_bucket(self) -> List:
        """List objects in the S3 bucket

        Raises:
            Exception: Thrown if bucket is not found or inaccessible

        Returns:
            List: List of objects {"name": str, "size": int, "last_modified": datetime.datetime}
        """
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
        except self.s3_client.exceptions.NoSuchBucket as err:
            raise S3BucketError(f"Error listing objects in S3 bucket: {err}")
        else:
            if response.get("IsTruncated") == True:
                logger.warning(
                    "Uh oh, received truncated results from S3 list object function and we haven't coded for that scenario. Somebody submit a pull request!")

            return [{"name": obj.get("Key"), "size": obj.get("Size"), "last_modified": obj.get("LastModified")} for obj in (response.get("Contents") or [])]

    def upload_file(self, file: str, metadata: dict):
        """Upload file to S3 bucket

        Args:
            file (str): Full path of file to upload
        """
        key = file.lstrip("/")
        extra_args = {}
        extra_args["StorageClass"] = self.storage_class
        if metadata is not None:
            extra_args["Metadata"] = metadata

        try:
            logger.info(f"Uploading file [{file}] to S3")
            self.s3_client.upload_file(Filename=file,
                                       Bucket=self.bucket_name,
                                       Key=key,
                                       ExtraArgs=extra_args)
            logger.info(
                f"Uploaded file [{key}] to S3 bucket [{self.bucket_name}] using storage class [{self.storage_class}]")
        except boto3.exceptions.S3UploadFailedError as err:
            raise S3BucketError(f"S3 upload error: {err}")
