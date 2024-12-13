import boto3
from django.conf import settings
from django.db import models


# Create your models here.
class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"  # Code from Boutique Ado project

    name = models.CharField(max_length=20, unique=True)
    friendly_name = models.CharField(
        max_length=254, blank=True
    )  # Code from Boutique Ado project

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products", blank=True, null=True)
    image_url = models.URLField(max_length=1024, blank=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )
            file_path = self.image.path
            bucket = settings.AWS_STORAGE_BUCKET_NAME
            s3_path = f"media/{self.image.name}"
            s3_client.upload_file(file_path, bucket, s3_path)
