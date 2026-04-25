from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    CLIENT = 'client'
    VOICE_ACTOR = 'voice_actor'

    ROLE_CHOICES = [
        (CLIENT, 'Client'),
        (VOICE_ACTOR, 'Voice Actor'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=CLIENT
    )

    def is_voice_actor(self):
        return self.role == self.VOICE_ACTOR

    def is_client(self):
        return self.role == self.CLIENT