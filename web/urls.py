from django.contrib import admin
from django.urls import path
from web.views import account, home, project
urlpatterns = [
    path('register/', account.register, name='register'),
    path('send_sms/', account.send_sms, name='send_sms'),
    path('login/sms/', account.login_sms, name='login_sms'),
    path('login/',account.login, name='login'),
    path('img/code/', account.img_code, name='img_code'),
    path('index/', home.index, name='index'),
    path('logout/', account.logout, name='logout'),
    path('project/list/', project.project_list, name='project_list'),
    path('project/star/(?p<project_type>\w+)/(?p<project_id>\d+)/$', project.project_star, name='project_star'),
    path('project/unstar/(?p<project_type>\w+)/(?p<project_id>\d+)/$', project.project_unstar, name='project_unstar'),

]
