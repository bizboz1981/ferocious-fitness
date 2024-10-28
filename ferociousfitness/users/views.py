from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Profile


@login_required
def profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    return render(request, "users/profile.html", {"profile": profile})


def index(request):
    return render(request, "users/index.html")
