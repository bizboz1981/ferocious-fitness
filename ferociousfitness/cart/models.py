from django.conf import settings
from django.db import models
from products.models import Product

# Create your models here.


# Model representing a shopping cart
class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # Each user has one cart
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Timestamp when the cart was created

    @property
    def total_order_price(self):
        return sum(item.subtotal for item in self.items.all())


# Model representing an item in the shopping cart
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items"
    )  # Each cart can have multiple items
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )  # Each item is associated with a product
    quantity = models.PositiveIntegerField(
        default=1
    )  # Quantity of the product in the cart

    @property
    def subtotal(self):
        return self.product.price * self.quantity
