import os

import boto3
from dotenv import load_dotenv


load_dotenv()


_s3_client = None


def _get_s3_client():
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client("s3")
    return _s3_client


def generate_presigned_url(
    object_key: str,
    expiration_seconds: int = 3600,
) -> str | None:
    """Generate a temporary URL for an S3 object."""

    bucket_name = os.getenv("ECOINFERENCE_S3_BUCKET")

    if not bucket_name:
        return None

    return _get_s3_client().generate_presigned_url(
        "get_object",
        Params={
            "Bucket": bucket_name,
            "Key": object_key,
        },
        ExpiresIn=expiration_seconds,
    )