from django.urls import path

from . import views

urlpatterns = [
    path("", views.booking_page, name="booking_page"),
    path("book/<int:session_id>/", views.book_session, name="book_session"),
]
