from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class PasswordReset(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    datetime = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4(),
    )
    is_done = models.BooleanField(default=False)

    def done(self):
        self.is_done = True
        self.save()

    def __str__(self):
        return self.user.username