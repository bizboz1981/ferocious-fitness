from django.shortcuts import get_object_or_404, redirect, render
from products.models import Product

from .models import Cart, CartItem

# Create your views here.


def add_to_cart(request, product_id):
    # Get the product by ID or return 404 if not found
    product = get_object_or_404(Product, id=product_id)
    # Get or create a cart for the current user
    cart, created = Cart.objects.get_or_create(user=request.user)
    # Get or create a cart item for the product in the user's cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        # If the cart item already exists, increment the quantity
        cart_item.quantity += 1
        cart_item.save()
    # Redirect to the cart detail view
    return redirect("view_cart")


def view_cart(request):
    # Get the cart for the current user or return 404 if not found
    cart = get_object_or_404(Cart, user=request.user)
    # Render the cart detail template with the cart context
    return render(request, "cart/view_cart.html", {"cart": cart})


def remove_from_cart(request, item_id):
    # Get the cart item by ID or return 404 if not found
    cart_item = get_object_or_404(CartItem, id=item_id)
    # Delete the cart item
    cart_item.delete()
    # Redirect to the cart detail view
    return redirect("view_cart")