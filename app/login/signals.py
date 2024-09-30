from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import PasswordReset


@receiver(pre_save, sender=PasswordReset)
def close_active_requests(sender, instance, **kwargs):
    PasswordReset.objects.filter(
        is_active=True,
        is_done=False,
        user=instance.user
    ).update(
        is_active=False,
    )
