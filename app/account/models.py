from django.db import models
import uuid
from django.db import models
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True)

    theme_preference = models.ForeignKey(
        to="Themes",
        null=True,
        on_delete=models.SET_NULL,
    )

    image = models.ImageField(
        upload_to='images/',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.user.username}'


class Admins(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        unique=True,
        related_name='admins',
    )
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Themes(models.Model):
    name = models.CharField(
        max_length=25,
        blank=False,
        null=False,
        default='light',
    )

    def __str__(self):
        return self.name