from django.shortcuts import render, redirect, HttpResponse
from app01 import models


# 展示部门信息
def depart_list(request):
    # 获取部门模块的数据，然后返回
    queryset = models.Department.objects.all()
    return render(request, 'depart_list.html', {'queryset': queryset})


# 部门添加
def depart_add(request):
    # 如果当前请求为get，直接返回页面
    if request.method == 'GET':
        return render(request, 'depart_add.html')
    # 否则，获取提交的title值
    title = request.POST.get('title')
    # 数据库创建数据
    models.Department.objects.create(title=title)
    # 重定向到部门列表页面
    return redirect('/depart/list/')


# 部门删除
def depart_delete(request):
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect('/depart/list/')


# 部门编辑
def depart_edit(request, nid):
    if request.method == 'GET':
        row_obj = models.Department.objects.filter(id=nid).first()

        return render(request, 'depart_edit.html', {'row_obj': row_obj})
    title = request.POST.get('title')
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect('/depart/list/')