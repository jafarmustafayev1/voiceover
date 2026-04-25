from django import forms
from .models import VoiceActorProfile


class VoiceActorProfileForm(forms.ModelForm):

    class Meta:
        model = VoiceActorProfile
        fields = (
            'bio',
            'language',
            'category',
            'price_per_word',
            'audio_sample',
            'is_available'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'