from django.shortcuts import render, redirect, HttpResponse
from web.forms.account import RegisterView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from web.forms.account import SendSmsForm

"""
    账户相关视图
"""


@csrf_exempt
def register(request):
    form = RegisterView()
    return render(request, "register.html", {"form": form})


@csrf_exempt
def send_sms(request):
    form = SendSmsForm(request, data=request.POST)  # 向SendSmsForm传递request对象，以便在form中获取到request对象
    if form.is_valid():  # 判断是否通过验证
        return JsonResponse({"status": True, "msg": "发送成功"})
    for i in form.errors.values():
        return JsonResponse({"status": False, "msg": i[0]})

