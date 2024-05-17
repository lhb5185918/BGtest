from django.contrib import admin
from django.urls import path
from web.views import account,home
urlpatterns = [
    path('register/', account.register, name='register'),
    path('send_sms/', account.send_sms, name='send_sms'),
    path('login/sms/', account.login_sms, name='login_sms'),
    path('login/',account.login, name='login'),
    path('img/code/', account.img_code, name='img_code'),
    path('index/', home.index, name='index'),
    path('logout/', account.logout, name='logout'),
]
