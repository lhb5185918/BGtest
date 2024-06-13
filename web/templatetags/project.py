from django.template import Library
from web import models
from django.urls import reverse  # 反向解析

register = Library()


@register.inclusion_tag('inclusion/all_project_list.html')
def all_project_list(request):
    # 获取我创建的项目
    my_project_list = models.Project.objects.filter(creator=request.transaction.user)
    # 获取我参与的项目
    join_project_list = models.ProjectUser.objects.filter(user=request.transaction.user)
    return {"my": my_project_list, "join": join_project_list, "request": request}


@register.inclusion_tag('inclusion/manage_menu_list.html')
def manage_menu_list(request):
    datalist = [
        {"title": "概览", "url": reverse("manage_dashboard", kwargs=({"project_id": request.project.id}))},
        {"title": "问题", "url": reverse("manage_issues", kwargs=({"project_id": request.project.id}))},
        {"title": "统计", "url": reverse("manage_statistics", kwargs=({"project_id": request.project.id}))},
        {"title": "wiki", "url": reverse("manage_wiki", kwargs=({"project_id": request.project.id}))},
        {"title": "文件", "url": reverse("manage_file", kwargs=({"project_id": request.project.id}))},
        {"title": "设置", "url": reverse("manage_setting", kwargs=({"project_id": request.project.id}))},

    ]
    for item in datalist:
        if request.path_info.startswith(item["url"]):
            item["class"] = "active"
    return {"data": datalist}
