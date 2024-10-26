from django.urls import path

from . import views

# Create your views here.
urlpatterns = [
    path("profile/", views.profile_view, name="profile"),
]
