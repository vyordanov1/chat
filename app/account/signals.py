from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a signal that will automatically create a Profile
    instance once a user is created ( either superuser or via the register form )
    """
    if created:
        Profile.objects.create(user=instance)