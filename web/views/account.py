from django.shortcuts import render, redirect, HttpResponse


"""
    账户相关视图
"""


def register(request):
    return render(request, "web/../templates/register.html")
