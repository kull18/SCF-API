import uuid

import boto3
from botocore.exceptions import ClientError

from src.core.config import settings

_s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
)


def build_event_photo_key(event_id: int, filename: str) -> str:
    extension = filename.rsplit(".", 1)[-1] if "." in filename else "jpg"
    return f"events/{event_id}/{uuid.uuid4()}.{extension}"


def generate_upload_presigned_url(object_key: str, expires_in: int = 300) -> str:
    """El cliente sube el archivo directo a S3 usando este URL (PUT)."""
    return _s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": settings.S3_BUCKET_NAME, "Key": object_key},
        ExpiresIn=expires_in,
    )


def generate_download_presigned_url(object_key: str, expires_in: int = 3600) -> str:
    """Para mostrar la foto en la app sin exponer el bucket como público."""
    return _s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.S3_BUCKET_NAME, "Key": object_key},
        ExpiresIn=expires_in,
    )


def delete_object(object_key: str) -> None:
    try:
        _s3_client.delete_object(Bucket=settings.S3_BUCKET_NAME, Key=object_key)
    except ClientError as e:
        raise RuntimeError(f"Failed to delete S3 object {object_key}: {e}")