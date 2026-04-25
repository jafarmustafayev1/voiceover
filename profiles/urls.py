from django.urls import path
from . import views

urlpatterns = [
    path('', views.actor_list, name='actor_list'),
    path('profile/', views.profile_view, name='profile'),
]