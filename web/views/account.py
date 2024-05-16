from django.shortcuts import render, redirect, HttpResponse
from web.forms.account import RegisterView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from web.forms.account import SendSmsForm, LoginSmsForm

"""
    账户相关视图
"""


@csrf_exempt
def register(request):
    if request.method == "GET":
        forms = RegisterView({})
        return render(request, "register.html", {"form": forms})
    elif request.method == "POST":
        forms = RegisterView(request, data=request.POST)
        if forms.is_valid():
            # 获取表单内容，清洗后写入数据库，密码加密
            forms.save()
            return JsonResponse({"status": True, "msg": "注册成功", "data": "/login/sms/"})
        else:
            for i in forms.errors.values():
                return JsonResponse({"status": False, "msg": i[0]})


@csrf_exempt
def send_sms(request):
    form = SendSmsForm(request, data=request.POST)  # 向SendSmsForm传递request对象，以便在form中获取到request对象
    print(request.POST.get('sms_type'), request.POST.get('phone'))
    if form.is_valid():  # 判断是否通过验证
        return JsonResponse({"status": True, "msg": "短信发送成功"})
    for i in form.errors.values():
        return JsonResponse({"status": False, "msg": i[0]})


@csrf_exempt
def login_sms(request):
    if request.method == 'POST':
        forms = LoginSmsForm(request, data=request.POST)
        if forms.is_valid():
            userinfo = forms.cleaned_data.get('phone')
            return JsonResponse({"status": True, "msg": "登录成功{}", "data": "/index/".format(userinfo.username)})
        for i in forms.errors.values():
            return JsonResponse({"status": False, "msg": i[0]})
    else:
        forms = LoginSmsForm({})
    return render(request, "login_sms.html", {"form": forms})
