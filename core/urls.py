from .views import home, register, login_view, chatbot_interview
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('interview/', chatbot_interview, name='chatbot_interview'),
]