import uuid
from django.db import models
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True

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
    name = models.CharField(
        blank=True,
        max_length=254,
    )
    is_public = models.BooleanField(
        default=False
    )

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


class Themes(models.Model):
    name = models.CharField(
        max_length=25,
        blank=False,
        null=False,
        default='light',
    )

    def __str__(self):
        return self.name


# class PasswordReset(models.Model):
#     user = models.ForeignKey(
#         to=User,
#         on_delete=models.CASCADE,
#     )
#     datetime = models.DateTimeField(auto_now_add=True)
#     uuid = models.UUIDField(
#         unique=True,
#         default=uuid.uuid4(),
#     )
#     is_done = models.BooleanField(default=False)
#
#     def done(self):
#         self.is_done = True
#         self.save()
#
#     def __str__(self):
#         return self.user.username