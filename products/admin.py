from django.contrib import admin

from .models import Category, Product


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "price",
        "category",
        "stock",
        "image",
        "image_url",
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "friendly_name"]
