from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from booking.models import Session

from .models import Profile


class ProfileForm(forms.ModelForm):
    # Optional file field for profile picture
    profile_pic = forms.FileField(required=False)

    class Meta:
        model = Profile
        # Fields to include in the form
        fields = ["bio", "subscription_status"]

    def save(self, commit=True):
        # Save the form data to the Profile instance
        profile = super().save(commit=False)
        # If a profile picture is provided, set it
        if self.cleaned_data["profile_pic"]:
            profile.set_profile_pic(self.cleaned_data["profile_pic"])
        # Save the Profile instance if commit is True
        if commit:
            profile.save()
        return profile


class SessionForm(forms.ModelForm):
    class Meta:
        # Specify the model to use for the form
        model = Session
        # Fields to include in the form
        fields = [
            "title",
            "description",
            "session_type",
            "date",
            "time",
            "location",
            "max_participants",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
        }

    def clean_date(self):
        # Get the date from the cleaned data
        date = self.cleaned_data.get("date")
        # Check if the date is in the past
        if date < timezone.now().date():
            # Raise a validation error if the date is in the past
            raise ValidationError("The date cannot be in the past.")
        # Return the cleaned date
        return date

    def clean_time(self):
        # Get the time from the cleaned data
        time = self.cleaned_data.get("time")
        # Check if the date is today and the time is in the past
        if (
            self.cleaned_data.get("date") == timezone.now().date()
            and time < timezone.now().time()
        ):
            # Raise a validation error if the time is in the past
            raise ValidationError("The time cannot be in the past.")
        # Return the cleaned time
        return time
