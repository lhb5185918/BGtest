from django.contrib import admin
from django.urls import path, include
from web.views import account, home, project, manage, wiki

# urlpatterns = [
#     path('register/', account.register, name='register'),
#     path('send_sms/', account.send_sms, name='send_sms'),
#     path('login/sms/', account.login_sms, name='login_sms'),
#     path('login/', account.login, name='login'),
#     path('img/code/', account.img_code, name='img_code'),
#     path('index/', home.index, name='index'),
#     path('logout/', account.logout, name='logout'),
#     path('project/list/', project.project_list, name='project_list'),
#     path('forget/', account.forget_password, name='forget_password'),
#     path('project/star/(?p<project_type>\w+)/(?p<project_id>\d+)/$', project.project_star, name='project_star'),
#     path('project/unstar/(?p<project_type>\w+)/(?p<project_id>\d+)/$', project.project_unstar, name='project_unstar'),
#     # path('manage/(?p<project_id>/dashboard/$', project.manage_dashboard, name='manage_dashboard'),
#     # path('manage/(?p<project_id>/issues/$', project.manage_issues, name='manage_issues'),
#     # path('manage/(?p<project_id>/statistics/$', project.manage_statistics, name='manage_statistics'),
#     # path('manage/(?p<project_id>/file/$', project.manage_file, name='manage_file'),
#     # path('manage/(?p<project_id>/wiki/$', project.manage_wiki, name='manage_wiki'),
#     # path('manage/(?p<project_id>/setting/$', project.manage_setting, name='manage_setting'),
#     path("manage/<int:project_id>/", include([
#         path('dashboard/$', manage.manage_dashboard, name='manage_dashboard'),
#         path('issues/$', manage.manage_issues, name='manage_issues'),
#         path('statistics/$', manage.manage_statistics, name='manage_statistics'),
#         path('file/$', manage.manage_file, name='manage_file'),
#         path('wiki/$', wiki.manage_wiki, name='manage_wiki'),
#         path('setting/$', manage.manage_setting, name='manage_setting'),
#         path('wiki/add/$', wiki.wiki_add, name='wiki_add'),
#     ]))  # include可以读取字符串，指定文件路径，也可以读取列表中的元组，指定多个文件路径
#
#
# ]


from django.contrib import admin
from django.urls import path, include, re_path
from web.views import account, home, project, manage, wiki

urlpatterns = [
    path('register/', account.register, name='register'),
    path('send_sms/', account.send_sms, name='send_sms'),
    path('login/sms/', account.login_sms, name='login_sms'),
    path('login/', account.login, name='login'),
    path('img/code/', account.img_code, name='img_code'),
    path('index/', home.index, name='index'),
    path('logout/', account.logout, name='logout'),
    path('project/list/', project.project_list, name='project_list'),
    path('forget/', account.forget_password, name='forget_password'),
    re_path(r'project/star/(?P<project_type>\w+)/(?P<project_id>\d+)/', project.project_star, name='project_star'),
    re_path(r'project/unstar/(?P<project_type>\w+)/(?P<project_id>\d+)/', project.project_unstar, name='project_unstar'),
    path("manage/<int:project_id>/", include([
        path('dashboard/', manage.manage_dashboard, name='manage_dashboard'),
        path('issues/', manage.manage_issues, name='manage_issues'),
        path('statistics/', manage.manage_statistics, name='manage_statistics'),
        path('file/', manage.manage_file, name='manage_file'),
        path('wiki/', wiki.manage_wiki, name='manage_wiki'),
        path('setting/', manage.manage_setting, name='manage_setting'),
        path('wiki/add/', wiki.wiki_add, name='wiki_add'),
        path('wiki/catalog/', wiki.wiki_catalog, name='wiki_catalog'),
        path(r'wiki/delete/(?p<wiki_id>\d+)', wiki.wiki_delete, name='wiki_delete'),
        path(r'wiki/edit/(?p<wiki_id>\d+)', wiki.wiki_edit, name='wiki_edit'),
        path('wiki/upload/', wiki.wiki_upload, name='wiki_upload'),
    ]))  # include可以读取字符串，指定文件路径，也可以读取列表中的元组，指定多个文件路径
]
