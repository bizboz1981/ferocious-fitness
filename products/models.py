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