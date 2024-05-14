from django.contrib import admin
from django.urls import path
from web.views import account
urlpatterns = [
    path('register/', account.register, name='register'),
    path('send_sms/', account.send_sms, name='send_sms'),
]
