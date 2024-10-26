from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )  # links profile to specific user
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    subscription_status = models.BooleanField(default=False)  # is user subscroibed?
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


# Automatically create a profile for each user when they are created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# Automatically save the profile when the user is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
