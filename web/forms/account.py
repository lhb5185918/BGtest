import requests
from django.shortcuts import render, HttpResponse
from web import models
from django import forms
from django.core.validators import RegexValidator
from django.core.validators import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection
from web.util.sms import send_sms
import random
import json
from web.util.encrypt import md5
from web.forms.bootstrap import BootStrapForm


# Create your views here.


@csrf_exempt
class RegisterView(forms.ModelForm):
    # 定义一个表单类
    phone = forms.CharField(max_length=11, min_length=11, required=True,
                            validators=[RegexValidator(r'(1[3456789])\d{9}$', '手机号格式错误')],
                            label='手机号')
    email = forms.EmailField(required=True, label='邮箱')
    password = forms.CharField(widget=forms.PasswordInput(), max_length=32, min_length=6, required=True, label='密码')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), max_length=32, min_length=6, required=True,
                                       label='确认密码')
    code = forms.CharField(max_length=4, min_length=4, required=True, label='验证码')

    class Meta:
        model = models.UserInfo
        fields = ['username', 'email', 'password', 'confirm_password', 'phone', 'code']

    def __init__(self, request, *args, **kwargs):
        # 重写初始化方法
        super().__init__(*args, **kwargs)
        for name, fields in self.fields.items():
            fields.widget.attrs['class'] = 'form-control'
            fields.widget.attrs['placeholder'] = '请输入{}'.format(fields.label)

    def clean_username(self):  # 重写clean_username方法,创建一个自定义的验证规则
        username = self.cleaned_data['username']
        exists = models.UserInfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError('用户名已存在')
        return username

    def clean_password(self):
        pwd = self.cleaned_data['password']
        # 对密码进行加密

        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data['password']
        confirm_pwd = self.cleaned_data['confirm_password']
        if pwd != md5(confirm_pwd):
            raise ValidationError('两次密码不一致')
        return confirm_pwd

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        exists = models.UserInfo.objects.filter(phone=phone).exists()
        if exists:
            raise ValidationError('手机号已存在')
        return phone

    def clean_code(self):
        if 'phone' not in self.cleaned_data:
            raise ValidationError('手机号验证失败,请重新输入手机号')
        code = self.cleaned_data['code']
        phone = self.cleaned_data['phone']
        conn = get_redis_connection()
        redis_code = conn.get(phone)

        if not redis_code:
            raise ValidationError('验证码已过期,请重新发送验证码')

        str_code = redis_code.decode('utf-8')

        if code.strip() != str_code:
            raise ValidationError('验证码错误,请重新输入')


@csrf_exempt
class SendSmsForm(forms.Form):  # 用于验证表单
    phone = forms.CharField(label='手机号',
                            validators=[RegexValidator(r'(1[3456789])\d{9}$', '手机号格式错误')])

    def __init__(self, request, *args, **kwargs):  # 重写类的初始化方法，以便在实例化的时候传递request对象
        super().__init__(*args, **kwargs)  # 调用父类的初始化方法
        self.request = request  # 将获取到的request对象赋值给self.request

    def clean_phone(self):  # 重写clean_phone方法
        phone = self.cleaned_data['phone']
        send_type = self.request.POST.get('sms_type')  # 调用request对象的POST方法获取send_type
        user_phone = models.UserInfo.objects.filter(phone=phone)
        if send_type == 'login':
            if not user_phone:
                raise ValidationError('手机号未注册')
        else:
            if user_phone:  # 判断手机号是否已经注册
                raise ValidationError('手机号已经注册')
        code = ''.join(random.sample('0123456789', 4))
        # res = send_sms(phone=phone, sms_code=send_type, code=code)  # 调用send_sms方法发送短信
        # if json.loads(res[0])['Message'] != "OK":
        #     raise ValidationError('短信发送失败{}'.format(json.loads(res[0])['Message']))
        # 短信验证码存入redis 采用django_redis组件
        conn = get_redis_connection()
        conn.set(phone, code, ex=60)  # 将验证码存入redis，有效期60秒
        return phone


@csrf_exempt
class LoginSmsForm(BootStrapForm, forms.Form):
    phone = forms.CharField(label='手机号',
                            validators=[RegexValidator(r'(1[3456789])\d{9}$', '手机号格式错误')])
    code = forms.CharField(max_length=4, min_length=4, required=True, label='验证码')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        user_object = models.UserInfo.objects.exists()
        if not user_object:
            raise ValidationError('手机号未注册')
        return phone

    def clean_code(self):
        code = self.cleaned_data['code']
        if 'phone' not in self.cleaned_data:
            raise ValidationError('手机号验证失败,请重新输入手机号')
        code = self.cleaned_data['code']
        phone = self.cleaned_data['phone']
        conn = get_redis_connection()
        redis_code = conn.get(phone)

        if not redis_code:
            raise ValidationError('验证码已过期,请重新发送验证码')

        str_code = redis_code.decode('utf-8')

        if code.strip() != str_code:
            raise ValidationError('验证码错误,请重新输入')


@csrf_exempt
class LoginForm(BootStrapForm, forms.Form):
    username = forms.CharField(label='邮箱或手机号')
    password = forms.CharField(widget=forms.PasswordInput(), max_length=32, min_length=6, required=True, label='密码')
    code = forms.CharField(label='图片验证码')

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.cleaned = None
        self.request = request

    def clean_code(self):
        code = self.cleaned_data['code']
        # 获取用户输入的验证码
        session_code = self.request.session.get('code')
        print(session_code, code)

        if not session_code:
            raise ValidationError('验证码已过期')

        if code.strip().upper() != session_code.upper():
            raise ValidationError('验证码输入错误')
        return code

    def clean_password(self):
        pwd = self.cleaned_data['password']
        return md5(pwd)


@csrf_exempt
class ForgetPasswordForm(BootStrapForm, forms.Form):
    username = forms.CharField(label='邮箱或手机号')
    new_password = forms.CharField(widget=forms.PasswordInput(), max_length=32, min_length=6, required=True,
                                   label='新密码')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), max_length=32, min_length=6, required=True,
                                       label='确认密码')
    phone = forms.CharField(label='手机号', max_length=11, min_length=11, required=True)
    code = forms.CharField(max_length=4, min_length=4, required=True, label='手机验证码')

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.request = request

    def clean_username(self):
        username = self.cleaned_data['username']
        exists = models.UserInfo.objects.filter(email=username).exists() or models.UserInfo.objects.filter(
            phone=username).exists()
        if not exists:
            raise ValidationError('用户未注册')
        return username

    def clean_new_password(self):
        pwd = self.cleaned_data['new_password']
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data['new_password']
        confirm_pwd = self.cleaned_data['confirm_password']
        if pwd != md5(confirm_pwd):
            raise ValidationError('两次密码不一致')
        return confirm_pwd

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        exists = models.UserInfo.objects.filter(phone=phone).exists()
        if not exists:
            raise ValidationError('手机号未注册')
        return phone

    def clean_code(self):
        if 'phone' not in self.cleaned_data:
            raise ValidationError('手机号验证失败,请重新输入手机号')
        code = self.cleaned_data['code']
        phone = self.cleaned_data['phone']
        conn = get_redis_connection()
        redis_code = conn.get(phone)

        if not redis_code:
            raise ValidationError('验证码已过期,请重新发送验证码')

        str_code = redis_code.decode('utf-8')

        if code.strip() != str_code:
            raise ValidationError('验证码错误,请重新输入')
