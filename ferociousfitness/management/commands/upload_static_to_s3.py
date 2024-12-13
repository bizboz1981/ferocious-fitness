import os

import boto3
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Upload static files to S3"

    def handle(self, *args, **kwargs):
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        static_root = settings.STATIC_ROOT
        bucket = settings.AWS_STORAGE_BUCKET_NAME
        for root, dirs, files in os.walk(static_root):
            for file in files:
                file_path = os.path.join(root, file)
                s3_path = os.path.relpath(file_path, static_root)
                s3_client.upload_file(file_path, bucket, f"static/{s3_path}")
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Uploaded {file_path} to s3://{bucket}/static/{s3_path}"
                    )
                )
