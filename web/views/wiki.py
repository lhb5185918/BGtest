from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from web.forms.wiki import WikiForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from web.models import Wiki


@csrf_exempt
def manage_wiki(request, project_id):
    """
    项目wiki管理
    :param request:
    :param project_id:
    :return:
    """
    wiki_id = request.GET.get("wiki_id")
    if not wiki_id or not wiki_id.isdecimal():
        return render(request, "manage_wiki.html")
    wiki_object = Wiki.objects.filter(id=wiki_id, project_id=request.project.id).first()
    return render(request, "manage_wiki.html", {"wiki_object": wiki_object})


@csrf_exempt
def wiki_add(request, project_id):
    """
    添加wiki
    :param request:
    :param project_id:
    :return:
    """
    if request.method == 'GET':
        form = WikiForm({})
        return render(request, "wiki_add.html", {"form": form})

    form = WikiForm(request, request.POST)
    if form.is_valid():
        if form.instance.parent:  # 如果有父级目录,排序+1
            form.instance.depth = form.instance.parent.depth + 1
        else:
            form.instance.depth = 1
        form.instance.project = request.project
        form.save()
        url = reverse("manage_wiki", kwargs={"project_id": project_id})
        return redirect(url)
    else:
        print(form.errors)
    return redirect("manage_wiki", project_id=project_id)


@csrf_exempt
def wiki_catalog(request, project_id):
    """
    wiki目录
    :param request:
    :param project_id:
    :return:
    """
    # 通过values方法获取指定字段的数据并返回字典，不需要使用values_list方法，因为values_list返回的是元组
    data = list(Wiki.objects.filter(project=request.project).values('id', 'title', "parent_id").order_by('depth', 'id'))

    return JsonResponse({"status": True, "data": data})


