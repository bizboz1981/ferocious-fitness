from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def profile_view(request):
    profile = request.user.profile  # Access the profile via the user
    return render(request, "profile.html", {"profile": profile})


def index(request):
    return render(request, "users/index.html")
