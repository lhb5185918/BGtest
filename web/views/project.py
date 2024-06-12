from django.shortcuts import render, redirect, HttpResponse
from web.forms.account import RegisterView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from web.forms.account import SendSmsForm, LoginSmsForm, LoginForm
from web.models import UserInfo
from web.util.image_code import check_code
from django.db.models import Q
from web.forms.project import ProjectModelForm
from web.models import Project, ProjectUser


@csrf_exempt
def project_list(request):
    if request.method == "GET":
        project_dict = {"star": [], "my": [], "join": []}
        my_project = Project.objects.filter(creator=request.transaction.user)  # 获取当前用户的项目
        for row in my_project:
            if row.star:
                project_dict['star'].append({"value": row, "type": "my"})
            else:
                project_dict['my'].append(row)
        join_project = ProjectUser.objects.filter(user=request.transaction.user)  # 获取当前用户参与的项目
        for item in join_project:
            if item.star:
                project_dict['star'].append({"value": item.project, "type": "join"})
            else:
                project_dict['join'].append(item.project)
        forms = ProjectModelForm({})
        return render(request, 'project_list.html', {"form": forms, "project_dict": project_dict})
    else:
        forms = ProjectModelForm(request, data=request.POST)
        if forms.is_valid():
            forms.instance.creator = request.transaction.user  # 获取当前用户
            forms.save()
            return JsonResponse({"status": True, "msg": "创建成功"})
            # return redirect('/project/list/')
        for i in forms.errors.values():
            return JsonResponse({"status": False, "msg": i[0]})


@csrf_exempt
def project_star(request, project_type, project_id):
    if project_type == 'my':
        Project.objects.filter(id=project_id, creator=request.transaction.user).update(star=True)
        return redirect('project_list')
    elif project_type == 'join':
        ProjectUser.objects.filter(project_id=project_id, user=request.transaction.user).update(star=True)
    return JsonResponse("ok", safe=False)


@csrf_exempt
def project_unstar(request, project_type, project_id):
    if project_type == 'my':
        Project.objects.filter(id=project_id, creator=request.transaction.user).update(star=False)
        return redirect('project_list')
    elif project_type == 'join':
        ProjectUser.objects.filter(project_id=project_id, user=request.transaction.user).update(star=False)
    return JsonResponse("ok", safe=False)
