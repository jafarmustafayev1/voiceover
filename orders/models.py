from django.db import models
from django.conf import settings
from profiles.models import VoiceActorProfile


class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('accepted', 'Qabul qilindi'),
        ('in_progress', 'Jarayonda'),
        ('delivered', 'Topshirildi'),
        ('completed', 'Yakunlandi'),
        ('cancelled', 'Bekor qilindi'),
    ]

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_orders'
    )
    actor = models.ForeignKey(
        VoiceActorProfile,
        on_delete=models.CASCADE,
        related_name='actor_orders'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    word_count = models.PositiveIntegerField()
    deadline = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    delivered_file = models.FileField(
        upload_to='deliveries/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_price = self.word_count * self.actor.price_per_word
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client.username} → {self.actor.user.username} | {self.title}"