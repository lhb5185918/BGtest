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
    if request.method == "GET":
        forms = RegisterView({})
        return render(request, "register.html", {"form": forms})
    elif request.method == "POST":
        forms = RegisterView(request,data=request.POST)
        if forms.is_valid():
            #获取表单内容，清洗后写入数据库，密码加密
            instance = forms.save()
            print(forms.cleaned_data)
            return JsonResponse({"status": True, "msg": "注册成功"})
        else:
            print(forms.errors)
            return JsonResponse({"status": False, "msg": "注册失败{}".format(forms.errors)})


@csrf_exempt
def send_sms(request):
    form = SendSmsForm(request, data=request.POST)  # 向SendSmsForm传递request对象，以便在form中获取到request对象
    print(request.POST.get('sms_type'), request.POST.get('phone'))
    if form.is_valid():  # 判断是否通过验证
        return JsonResponse({"status": True, "msg": "发送成功"})
    for i in form.errors.values():
        return JsonResponse({"status": False, "msg": i[0]})

