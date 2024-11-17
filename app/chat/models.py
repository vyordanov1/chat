import uuid
from wonderwords import RandomWord
from django.db import models
from django.contrib.auth.models import User
from account.models import Profile, Themes
from .secure_messages import encrypt_text, decrypt_text
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
            r = RandomWord()
            self.name = r.word()
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


class OffensiveWords(models.Model):
    word = models.CharField(
        max_length=254,
        unique=True,
    )


class EncryptedTextField(models.TextField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return decrypt_text(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return encrypt_text(value)


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
    # content = models.TextField()
    content = EncryptedTextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        offensive_words = OffensiveWords.objects.all()
        detected_bad_words = [word.word for word in offensive_words if word.word.lower() in self.content.lower()]

        for word in detected_bad_words:
            AbuseReport.objects.create(
                message=self,
                bad_word=word,
                type=AbuseReport.ReportChoices.AUTOMATIC
            )

    def __str__(self):
        return f"{self.sender.username}: {self.timestamp}"


class AbuseReport(models.Model):
    class ReportChoices(models.TextChoices):
        AUTOMATIC = ("AUTOMATIC", "Automatic")
        MANUAL = ("MANUAL", "Manual")

    message = models.ForeignKey(
        to=Message,
        on_delete=models.CASCADE,
    )
    bad_word = models.CharField(
        max_length=254,
        blank=True,
        null=True,
    )
    type = models.CharField(
        max_length=100,
        choices=ReportChoices.choices,
        default=ReportChoices.AUTOMATIC,
        blank=False,
        null=False,
    )
    report_date = models.DateTimeField(
        auto_now_add=True
    )
    processed = models.BooleanField(
        default=False
    )
    processed_date = models.DateTimeField(
        auto_now_add=False,
        blank=True,
        null=True
    )

