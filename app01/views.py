from django.shortcuts import render, HttpResponse
from django import forms
from django.core.validators import RegexValidator
from django.core.validators import ValidationError
import redis
from app01.models import UserInfo


# Create your views here.


class RegisterView(forms.ModelForm):
    # 定义一个表单类
    phone = forms.CharField(max_length=11, min_length=11, required=True,
                            validators=[RegexValidator(r'(1[3][4][5][6][7][8][9])\d{9}$', '手机号格式错误')],
                            label='手机号')
    email = forms.EmailField(required=True, label='邮箱')
    password = forms.CharField(widget=forms.PasswordInput(), max_length=32, min_length=6, required=True, label='密码')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), max_length=32, min_length=6, required=True,
                                       label='确认密码')
    code = forms.CharField(max_length=6, min_length=6, required=True, label='验证码')

    class Meta:
        model = UserInfo
        fields = ['username', 'password', 'confirm_password', 'phone', 'code', 'email']

    def __init__(self, *args, **kwargs):
        # 重写初始化方法
        super().__init__(*args, **kwargs)
        for name, fields in self.fields.items():
            fields.widget.attrs['class'] = 'form-control'
            fields.widget.attrs['placeholder'] = '请输入{}'.format(fields.label)


def register(request):
    form = RegisterView()
    return render(request, 'register.html', {"form": form})


def get_sms(requests):
    return HttpResponse('发送短信成功')
