from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from app01.utils.form import PrettyModelForm, PrettyEditModelForm
from app01.utils.pagination import Pagination


# 靓号列表
def pretty_list(request):
    data = {}
    # 获取前端传的query参数，如果没有就空字符串
    search_data = request.GET.get("query", "")
    # 如果参数不为空，则传入字典，mobile__contains是固定写法，表示我的搜索是包含搜索
    if search_data:
        data["mobile__contains"] = search_data
    # 注意，我们获取queryset的时候可以排序，加-表示倒叙排列，不加-表示正序排列
    queryset = models.PrettyNum.objects.filter(**data)
    # 创建一个分页插件类
    page = Pagination(request, queryset, page_param="page", page_size=10, plus=3)
    context = {
        "queryset": page.page_queryset,  # 分完页的数据（当前页）
        "page_string": page.html(),  # 页码显示
        "search_data": search_data
    }

    # 返回的时候返回search_data，因为前端页面要展示
    return render(request, "pretty_list.html", context)


# 靓号添加
def pretty_add(request):
    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, "pretty_add.html", {"form": form})
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_add.html', {'form': form})


# 靓号编辑
def pretty_edit(request, nid):
    row_obj = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_obj)
        return render(request, 'pretty_edit.html', {'form': form})
    form = PrettyEditModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_edit.html', {'form': form})


# 靓号删除
def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')

