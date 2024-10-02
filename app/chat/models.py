import uuid
from random_word import RandomWords
from django.db import models
from django.contrib.auth.models import User
from account.models import Profile, Themes
User._meta.get_field('email')._unique = True


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
    name = models.CharField(
        default='',
        blank=True,
        max_length=254,
    )

    is_public = models.BooleanField(
        default=False
    )

    def save(self, *args, **kwargs):
        if not self.name:
            r = RandomWords()
            self.name = r.get_random_word()
        if not self.uuid_redacted:
            self.uuid_redacted = str(self.uuid).replace('-', '')

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class UserChatRoom(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='chatrooms',
    )
    chat_room = models.ForeignKey(
        to=ChatRoom,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (('user', 'chat_room'),)


class Message(models.Model):
    sender = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    chat_room = models.ForeignKey(
        to=ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.timestamp}"
