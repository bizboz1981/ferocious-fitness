from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone

from booking.models import Booking, Session

from .forms import ProfileForm, SessionForm
from .models import Profile


def index(request):
    # Render the index page
    return render(request, "users/index.html")


@login_required
def profile_view(request):
    # Get the current logged-in user
    user = request.user

    # Get or create a profile for the user
    profile, created = Profile.objects.get_or_create(user=user)

    # Get the user's bookings
    bookings = Booking.objects.filter(user=user).order_by("session__date")

    if request.method == "POST":
        # If the request is a POST, create a form instance
        # with the POST data and files
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        # Check if the form is valid
        if form.is_valid():
            # Save the form and redirect to the profile page
            form.save()
            return redirect("profile")
    else:
        # If the request is not a POST, create a form instance
        # with the existing profile data
        form = ProfileForm(instance=profile)

    # Render the profile page with the profile and form data
    return render(
        request,
        "users/profile.html",
        {"profile": profile, "form": form, "bookings": bookings},
    )


@login_required
def cancel_booking(request, booking_id):
    # Get the booking with the given ID
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    # Delete the booking
    booking.delete()
    # flash message confirming the cancellation
    messages.success(
        request,
        f"Booking for {booking.session.title} on {booking.session.date.strftime('%d/%m/%Y')} cancelled successfully.",
    )
    # Redirect to the profile page
    return redirect("profile")


def is_staff(user):
    # Check if the user is a staff member and not a superuser
    return user.is_staff and not user.is_superuser


@user_passes_test(is_staff, login_url=reverse_lazy("login"))
def add_session(request):
    if request.method == "POST":
        # If the request is a POST, create a form instance with the POST data
        form = SessionForm(request.POST)
        if form.is_valid():
            # If the form is valid, save the new session
            form.save()
            # Display a success message
            messages.success(request, "Session added successfully.")
            # Redirect to the add session page
            return redirect("add_session")
    else:
        # If the request is not a POST, create an empty form instance
        form = SessionForm()

    # Get the list of upcoming sessions
    upcoming_sessions = Session.objects.filter(
        date__gte=timezone.now().date()
    ).order_by("date", "time")
    # Render the add session page with the form data
    return render(
        request,
        "users/add_session.html",
        {"form": form, "upcoming_sessions": upcoming_sessions},
    )
