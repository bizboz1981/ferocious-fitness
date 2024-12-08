from django import forms

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
