import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe

from products.models import Product

from .models import Cart, CartItem, Order

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.


def add_to_cart(request, product_id):
    # Get the product by ID or return 404 if not found
    product = get_object_or_404(Product, id=product_id)
    # Get or create a cart for the current user
    cart = get_cart(request)  # Use the helper for both user and session carts

    # Get quantity from POST data, default to 1 if not provided or invalid
    try:
        quantity = int(request.POST.get("quantity", 1))
        if quantity < 1:
            quantity = 1
    except (TypeError, ValueError):
        quantity = 1

    # Get or create a cart item for the product in the user's cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        # If the cart item already exists, increment by the chosen quantity
        cart_item.quantity += quantity
    else:
        # If new, set to the chosen quantity
        cart_item.quantity = quantity
    cart_item.save()

    # Flash message to confirm the product was added to the cart
    # Then redirect to the products page
    messages.success(
        request,
        mark_safe(
            (
                f"{product.name} was successfully added to your basket. "
                "<a href='/cart/'>View Basket</a>"
            )
        ),
    )
    return redirect("view_cart")


def view_cart(request):
    # Get the cart for the current user or return 404 if not found
    cart = get_cart(request)  # Use the helper for both user and session carts
    # Render the cart detail template with the cart context
    return render(request, "cart/view_cart.html", {"cart": cart})


def remove_from_cart(request, item_id):
    # Get the cart item by ID or return 404 if not found
    cart_item = get_object_or_404(CartItem, id=item_id)
    # Delete the cart item
    cart_item.delete()
    # Redirect to the cart detail view
    return redirect("view_cart")


@login_required
def complete_order(request):
    if request.method == "POST":
        # Get the form data
        name = request.POST.get("name")
        address_line1 = request.POST.get("address_line1")
        address_line2 = request.POST.get("address_line2")
        address_line3 = request.POST.get("address_line3")
        city = request.POST.get("city")
        postcode = request.POST.get("postcode")
        country = request.POST.get("country")

        # Get the cart for the current user or return 404 if not found
        # Use the helper for both user and session carts
        cart = get_cart(request)
        # Create an order from the cart
        order = cart.create_order()

        # Set the order details from the form data
        order.name = name
        order.address_line1 = address_line1
        order.address_line2 = address_line2
        order.address_line3 = address_line3
        order.city = city
        order.postcode = postcode
        order.country = country
        order.save()

        # Create a Stripe Checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "gbp",
                        "product_data": {
                            "name": item.product.name,
                        },
                        "unit_amount": int(item.product.price * 100),
                    },
                    "quantity": item.quantity,
                }
                for item in order.items
            ],
            mode="payment",
            success_url=request.build_absolute_uri(
                reverse("order_confirmation", args=[order.id])
            ),
            cancel_url=request.build_absolute_uri(reverse("view_cart")),
            client_reference_id=order.id,
        )

        # Redirect to the Stripe Checkout page
        return redirect(session.url, code=303)
    return redirect("view_cart")


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    session_id = request.GET.get("session_id")

    if session_id:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == "paid":
            order.paid = True
            order.save()

    return render(request, "cart/order_confirmation.html", {"order": order})


# View to handle getting the cart
def get_cart(request):
    # If the user is authenticated, get or create a cart associated with the
    # user
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # For anonymous users, use session to track their cart
        cart_id = request.session.get("cart_id")
        if cart_id:
            # Try to retrieve an existing cart with this session cart_id and
            # no user
            cart = Cart.objects.filter(id=cart_id, user__isnull=True).first()
            if not cart:
                # If not found, create a new cart and store its id in the
                # session
                cart = Cart.objects.create()
                request.session["cart_id"] = cart.id
        else:
            # If no cart_id in session, create a new cart and store its id in
            # the session
            cart = Cart.objects.create()
            request.session["cart_id"] = cart.id
    # Return the cart instance (either existing or newly created)
    return cart
