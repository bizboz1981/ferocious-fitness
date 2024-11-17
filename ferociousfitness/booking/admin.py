from django.contrib import admin

from .models import Booking, ClassType, Session


# Register your models here.
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "session_type",
        "date",
        "time",
        "location",
        "max_participants",
        "current_participants",
    ]


@admin.register(ClassType)
class ClassTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["session", "user", "booking_date"]
