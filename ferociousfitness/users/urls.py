from django.urls import path

from . import views
from .views import cancel_booking, profile_view

urlpatterns = [
    path("", views.index, name="index"),
    path("index.html", views.index, name="index"),
    path("profile/", profile_view, name="profile"),
    path("cancel_booking/<int:booking_id>/", cancel_booking, name="cancel_booking"),
]
