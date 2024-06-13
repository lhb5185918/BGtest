from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from web.forms.wiki import WikiForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from web.models import Wiki
from web.util.encrypt import uid
from web.util.cos import upload_file


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


@csrf_exempt
def wiki_delete(request, project_id, wiki_id):
    Wiki.objects.filter(project_id=request.project.id, id=wiki_id).delete()
    url = reverse("manage_wiki", kwargs={"project_id": project_id})
    return redirect(url)


@csrf_exempt
def wiki_edit(request, project_id, wiki_id):
    wiki_object = Wiki.objects.filter(project_id=request.project.id, id=wiki_id).first()
    if not wiki_object:
        return redirect("manage_wiki", project_id=project_id)
    if request.method == "GET":
        form = WikiForm(request, instance=wiki_object)
        return render(request, "wiki_add.html", {"form": form})
    form = WikiForm(request, request.POST, instance=wiki_object)
    if form.is_valid():
        form.save()
        url = reverse("manage_wiki", kwargs={"project_id": project_id})
        cat_url = "{0}?wiki_id={1}".format(url, wiki_id)
        return redirect(cat_url)


@csrf_exempt
def wiki_upload(request, project_id):
    """ markdown插件上传图片 """
    result = {
        'success': 0,
        'message': None,
        'url': None
    }

    image_object = request.FILES.get('editormd-image-file')
    if not image_object:
        result['message'] = "文件不存在"
        return JsonResponse(result)
    image_object = request.FILES.get('editormd-image-file')
    ext = image_object.name.rsplit('.')[-1]
    key = "{}.{}".format(uid(request.tracer.phone), ext)
    image_url = upload_file(
        request.project.bucket,
        request.project.region,
        image_object,
        key
    )
    result['success'] = 1
    result['url'] = image_url
    print(result)
    return JsonResponse(result)
