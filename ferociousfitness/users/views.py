from booking.models import Booking
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileForm
from .models import Profile


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


def index(request):
    # Render the index page
    return render(request, "users/index.html")
