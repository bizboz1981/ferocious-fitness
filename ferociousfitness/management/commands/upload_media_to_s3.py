import os

import boto3
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Upload media files to S3"

    def handle(self, *args, **kwargs):
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        media_root = settings.MEDIA_ROOT
        bucket = settings.AWS_STORAGE_BUCKET_NAME
        for root, dirs, files in os.walk(media_root):
            for file in files:
                file_path = os.path.join(root, file)
                s3_path = os.path.relpath(file_path, media_root)
                s3_client.upload_file(file_path, bucket, f"media/{s3_path}")
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Uploaded {file_path} to s3://{bucket}/media/{s3_path}"
                    )
                )
