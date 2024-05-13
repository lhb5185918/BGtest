from django.urls import path
from app01 import views
app_name = 'app01'
urlpatterns = [
    path('register/', views.register),
    path('sms/', views.get_sms),
]
