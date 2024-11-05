from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Themes


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a signal that will automatically create a Profile
    instance once a user is created ( either superuser or via the register form )
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_migrate)
def create_default_themes(sender, **kwargs):
    """
    Create a signal that will automatically create the default themes ( dark/light )
    """
    required = ['dark', 'light']
    for entry in required:
        try:
            Themes.objects.get(name=entry.lower())
        except ObjectDoesNotExist as e:
            Themes.objects.create(name=entry.lower())
