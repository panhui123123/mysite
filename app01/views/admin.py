from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm
from app01.utils.pagination import Pagination


# 管理员列表
def admin_list(request):
    data = {}
    # 获取前端传的query参数，如果没有就空字符串
    search_data = request.GET.get("query", "")
    # 如果参数不为空，则传入字典，mobile__contains是固定写法，表示我的搜索是包含搜索
    if search_data:
        data["username__contains"] = search_data
    # 注意，我们获取queryset的时候可以排序，加-表示倒叙排列，不加-表示正序排列
    queryset = models.Admin.objects.filter(**data)
    # 创建一个分页插件类
    page = Pagination(request, queryset, page_param="page", page_size=10, plus=3)
    context = {
        "queryset": page.page_queryset,  # 分完页的数据（当前页）
        "page_string": page.html(),  # 页码显示
        "search_data": search_data
    }

    # 返回的时候返回search_data，因为前端页面要展示
    return render(request, "admin_list.html", context)


def admin_add(request):
    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, "admin_add.html", {"form": form})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'admin_add.html', {'form': form})


def admin_edit(request, nid):
    row_obj = models.Admin.objects.filter(id=nid).first()
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_obj)
        return render(request, 'admin_edit.html', {'form': form})
    form = AdminEditModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'admin_edit.html', {'form': form})


def admin_delete(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


def admin_reset(request, nid):
    row_obj = models.Admin.objects.filter(id=nid).first()
    if request.method == "GET":
        form = AdminResetModelForm(instance=row_obj)
        return render(request, 'admin_reset.html', {'form': form})
    form = AdminResetModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'admin_reset.html', {'form': form})