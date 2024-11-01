import io

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image


# Create your models here.
class Profile(models.Model):
    # Link the profile to a user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # A short bio for the user
    bio = models.TextField(max_length=500, blank=True, null=True)
    # Store the profile picture as binary data
    profile_pic = models.BinaryField(blank=True, null=True)
    # Subscription status of the user
    subscription_status = models.BooleanField(default=False)
    # The date when the user joined
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Return a string representation of the profile
        return f"{self.user.username}'s profile"

    def get_profile_pic(self):
        # Return the profile picture if it exists
        if self.profile_pic:
            return self.profile_pic
        return None

    def set_profile_pic(self, image):
        # Set the profile picture from an image file
        if image:
            img = Image.open(image)
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format=img.format)
            self.profile_pic = img_byte_arr.getvalue()


# Automatically create a profile for each user when they are created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# Automatically save the profile when the user is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
