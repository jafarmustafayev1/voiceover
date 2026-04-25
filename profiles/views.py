from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import VoiceActorProfile
from .forms import VoiceActorProfileForm


@login_required
def profile_view(request):
    if not request.user.is_voice_actor():
        messages.error(request, 'Bu sahifa faqat voice actor lar uchun!')
        return redirect('home')

    profile, created = VoiceActorProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        form = VoiceActorProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil saqlandi!')
            return redirect('profile')
    else:
        form = VoiceActorProfileForm(instance=profile)

    return render(request, 'profiles/profile.html', {'form': form, 'profile': profile})


def actor_list(request):
    actors = VoiceActorProfile.objects.filter(
        is_available=True
    ).select_related('user')

    language = request.GET.get('language')
    category = request.GET.get('category')

    if language:
        actors = actors.filter(language=language)
    if category:
        actors = actors.filter(category=category)

    return render(request, 'profiles/actor_list.html', {
        'actors': actors,
        'language_choices': VoiceActorProfile.LANGUAGE_CHOICES,
        'category_choices': VoiceActorProfile.CATEGORY_CHOICES,
    })