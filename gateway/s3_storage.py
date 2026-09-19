import os

import boto3
from dotenv import load_dotenv


load_dotenv()


S3_BUCKET_NAME = os.getenv("ECOINFERENCE_S3_BUCKET")

s3_client = boto3.client("s3")


def generate_presigned_url(
    object_key: str,
    expiration_seconds: int = 3600,
) -> str:
    """Generate a temporary URL for an S3 object."""

    if not S3_BUCKET_NAME:
        raise RuntimeError(
            "ECOINFERENCE_S3_BUCKET environment variable is not set."
        )

    return s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": S3_BUCKET_NAME,
            "Key": object_key,
        },
        ExpiresIn=expiration_seconds,
    )