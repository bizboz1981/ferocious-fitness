from django.conf import settings
from django.db import models

from products.models import Product

# Create your models here.


# Model representing a shopping cart
class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )  # Each user has one cart
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Timestamp when the cart was created

    @property
    def total_order_price(self):
        return sum(item.subtotal for item in self.items.all())

    def create_order(self):
        order = Order.objects.create(
            user=self.user if self.user else None, total_price=self.total_order_price
        )
        for item in self.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
        self.items.all().delete()  # Clear the cart after creating the order
        return order


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


# Model representing an order
class Order(models.Model):
    # Each order has: user, timestamp, total price
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Add form fields to the Order model
    name = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    address_line3 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)

    # String representation of the order
    def __str__(self):
        return f"Order ID: {self.id}"

    # Get all items in the order
    @property
    def items(self):
        return self.order_items.all()


# Model representing an item in an order
class OrderItem(models.Model):
    # Each order item has: order, product, quantity, price
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # String representation of the order item
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
