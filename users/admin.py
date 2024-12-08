from django.contrib import admin

from .models import Profile


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ["user", "subscription_status", "join_date"]

    # Fields to filter by in the admin list view
    list_filter = ["subscription_status", "join_date"]

    # Fields to search by in the admin search bar
    search_fields = ["user__username", "user__email"]


# Register the Profile model with the ProfileAdmin options
admin.site.register(Profile, ProfileAdmin)
