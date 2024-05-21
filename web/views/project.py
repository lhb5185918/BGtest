from django.shortcuts import render, redirect, HttpResponse
from web.forms.account import RegisterView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from web.forms.account import SendSmsForm, LoginSmsForm, LoginForm
from web.models import UserInfo
from web.util.image_code import check_code
from django.db.models import Q


def project_list(request):
    return render(request,'project_list.html')