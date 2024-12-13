import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import Subscription

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def subscribe(request):
    if request.method == "POST":
        # Create Stripe Checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": "price_1Hh1Y2IyNTgGDV2p9x0z4e5T",  # Replace with your price ID
                    "quantity": 1,
                },
            ],
            mode="subscription",
            success_url=request.build_absolute_uri("/subscriptions/success/"),
            cancel_url=request.build_absolute_uri("/subscriptions/cancel/"),
        )
        return redirect(session.url, code=303)
    return render(request, "subscriptions/subscribe.html")


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({"error": str(e)}, status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user = User.objects.get(email=session["customer_email"])
        Subscription.objects.create(
            user=user,
            stripe_subscription_id=session["subscription"],
            end_date=timezone.now() + timezone.timedelta(days=30),
        )

    return JsonResponse({"status": "success"}, status=200)


@login_required
def success(request):
    return render(request, "subscriptions/success.html")


@login_required
def cancel(request):
    return render(request, "subscriptions/cancel.html")
