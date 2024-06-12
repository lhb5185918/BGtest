from django.shortcuts import render, redirect, HttpResponse
from web.forms.account import RegisterView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from web.forms.account import SendSmsForm, LoginSmsForm, LoginForm, ForgetPasswordForm
from web.models import UserInfo, PricePolicy, Transaction, Project, ProjectUser
from web.util.image_code import check_code
from django.db.models import Q
import uuid
import datetime


def manage_dashboard(request, project_id):
    """
    项目管理首页
    :param request:
    :param project_id:
    :return:
    """
    print(project_id)
    return render(request, "manage_dashboard.html")


def manage_issues(request, project_id):
    """
    项目问题管理
    :param request:
    :param project_id:
    :return:
    """
    return render(request, "manage_issues.html")


def manage_statistics(request, project_id):
    """
    项目统计管理
    :param request:
    :param project_id:
    :return:
    """
    return render(request, "manage_statistics.html")


def manage_file(request, project_id):
    """
    项目文件管理
    :param request:
    :param project_id:
    :return:
    """
    return render(request, "manage_file.html")





def manage_setting(request, project_id):
    """
    项目设置管理
    :param request:
    :param project_id:
    :return:
    """
    return render(request, "manage_setting.html")
