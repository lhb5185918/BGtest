from django.shortcuts import render, redirect, HttpResponse
from web.forms.account import RegisterView
from django.views.decorators.csrf import csrf_exempt

"""
    账户相关视图
"""


@csrf_exempt
def register(request):
    form = RegisterView(request.POST)
    return render(request, "register.html",{"form": form})


@csrf_exempt
def send_sms(request):
    phone = request.POST.get("phone")
    username = request.POST.get("username")
    print(phone, username)
    return HttpResponse("发送短信成功")
