import uuid
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True)

    def __str__(self):
        return f'{self.user.username}'


class ChatRoom(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        blank=False,
        null=False,
        unique=True,
        editable=False
    )
    uuid_redacted = models.CharField(
        default='',
        blank=True,
        null=True,
        editable=False
    )


class UserChatRoom(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    chat_room = models.ForeignKey(
        to=ChatRoom,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (('user', 'chat_room'),)