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
            # 创建交易记录
            instance = forms.save()
            price = PricePolicy.objects.get(category=1, title='个人免费版')
            Transaction.objects.create(status=2, order=str(uuid.uuid4()), user=instance, price_policy=price,
                                       count=0, price=0, start_datetime=datetime.datetime.now())
            return JsonResponse({"status": True, "msg": "注册成功", "data": "/login/"})
        else:
            for i in forms.errors.values():
                return JsonResponse({"status": False, "msg": i[0]})


@csrf_exempt
def send_sms(request):
    form = SendSmsForm(request, data=request.POST)
    # 向SendSmsForm传递request对象，以便在form中获取到request对象
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
            userinfo = UserInfo.objects.filter(phone=forms.cleaned_data.get('phone')).first()
            request.session['user_id'] = userinfo.user_id
            request.session.set_expiry(60 * 60 * 24 * 14)
            return JsonResponse({"status": True, "msg": "登录成功{}".format(userinfo.username), "data": "/index/"})
        for i in forms.errors.values():
            return JsonResponse({"status": False, "msg": i[0]})
    else:
        forms = LoginSmsForm({})
    return render(request, "login_sms.html", {"form": forms})


@csrf_exempt
def login(request):
    if request.method == "GET":
        forms = LoginForm(request, {})
        return render(request, "login.html", {"form": forms})
    else:
        forms = LoginForm(request, data=request.POST)
        if forms.is_valid():
            username = forms.cleaned_data.get('username')
            password = forms.cleaned_data.get('password')
            # user = UserInfo.objects.filter(username=username, password=password).first()
            user_object = UserInfo.objects.filter(Q(email=username) |
                                                  Q(phone=username)).filter(password=password).first()
            # 通过Q对象实现或查询表达的是或的关系
            if user_object:
                #  登录成功后，将用户id存入session
                request.session['user_id'] = user_object.user_id
                request.session.set_expiry(60 * 60 * 24 * 14)
                return JsonResponse({"status": True, "msg": "登录成功", "data": "/index/"})
            forms.add_error("username", "用户名或密码错误")
        for i in forms.errors.values():
            return JsonResponse({"status": False, "msg": i[0]})
    return render(request, "login.html", {"form": forms})


@csrf_exempt
def img_code(request):
    from io import BytesIO
    # 调用 check_code 函数生成验证码图片对象和验证码字符串
    image_object, code = check_code()
    # 将验证码字符串存入 session，以便后续验证用户输入的验证码是否正确
    request.session['code'] = code
    # 设置验证码图片的过期时间
    request.session.set_expiry(60)
    # 创建一个 BytesIO 对象，用于在内存中存储图片数据
    stream = BytesIO()
    image_object.save(stream, 'png')
    stream.getvalue()

    return HttpResponse(stream.getvalue())


@csrf_exempt
def logout(request):
    # 退出登录，清除session
    request.session.flush()
    return redirect("/index/")


@csrf_exempt
def forget_password(request):
    if request.method == "GET":
        forms = ForgetPasswordForm({})
        return render(request, "forget_password.html", {"form": forms})
    else:
        forms = ForgetPasswordForm(request, data=request.POST)
        if forms.is_valid():
            phone = forms.cleaned_data.get("phone")
            password = forms.cleaned_data.get("new_password")
            user_object = UserInfo.objects.filter(phone=phone).first()
            if user_object:
                user_object.password = password
                user_object.save()
                return JsonResponse({"status": True, "msg": "密码修改成功", "data": "/login/"})
            forms.add_error("phone", "手机号不存在")
        for i in forms.errors.values():
            return JsonResponse({"status": False, "msg": i[0]})
        return JsonResponse({"status": False, "msg": "未知错误"})
