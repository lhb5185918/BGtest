from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from web.forms.wiki import WikiForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from web.models import Wiki
from web.util.encrypt import uid
from web.util.cos import upload_file


@csrf_exempt
def manage_file(request, project_id):
    """
    上传文件
    :param request:
    :param project_id:
    :return:
    """

    return render(request, 'manage_file.html')


@csrf_exempt
def manage_file_delete(request, project_id, file_id):
    """
    删除文件
    :param request:
    :param project_id:
    :param file_id:
    :return:
    """
    pass


@csrf_exempt
def manage_file_post(request, project_id):
    pass


@csrf_exempt
def manage_file_credential(request, project_id):
    """
    获取上传凭证
    :param request:
    :param project_id:
    :return:
    """
    pass
