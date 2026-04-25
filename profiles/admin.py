from django.contrib import admin
from .models import VoiceActorProfile


@admin.register(VoiceActorProfile)
class VoiceActorProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'language',
        'category',
        'price_per_word',
        'is_available',
        'created_at'
    )
    list_filter = ('language', 'category', 'is_available')
    search_fields = ('user__username', 'bio')