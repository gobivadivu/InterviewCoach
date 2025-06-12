from .views import home, register, login_view, audio_input
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('upload/', audio_input, name='audio_upload'),
]