from django.shortcuts import render, redirect, HttpResponse
from web.forms.account import RegisterView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from web.forms.account import SendSmsForm, LoginSmsForm, LoginForm
from web.models import UserInfo
from web.util.image_code import check_code
from django.db.models import Q
from web.forms.project import ProjectModelForm


@csrf_exempt
def project_list(request):
    if request.method =="GET":
        forms = ProjectModelForm({})
        return render(request,'project_list.html',{"form": forms})
    else:
        forms = ProjectModelForm(request, data=request.POST)
        if forms.is_valid():
            forms.instance.creator = request.transaction.user  # 获取当前用户
            forms.save()
            return JsonResponse({"status": True, "msg": "创建成功"})
            # return redirect('/project/list/')
        for i in forms.errors.values():
            return JsonResponse({"status": False, "msg": i[0]})

