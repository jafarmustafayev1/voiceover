from django.db import models
from django.conf import settings


def audio_upload_path(instance, filename):
    return f'audio/{instance.user.username}/{filename}'


class VoiceActorProfile(models.Model):

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
        ('ar', 'Arabic'),
        ('zh', 'Chinese'),
    ]

    CATEGORY_CHOICES = [
        ('corporate', 'Corporate'),
        ('commercial', 'Commercial'),
        ('audiobook', 'Audiobook'),
        ('animation', 'Animation'),
        ('elearning', 'E-Learning'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='voice_profile'
    )
    bio = models.TextField(max_length=500, blank=True)
    language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='en'
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='corporate'
    )
    price_per_word = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        default=0.010
    )
    audio_sample = models.FileField(
        upload_to=audio_upload_path,
        blank=True,
        null=True
    )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_language_display()}"