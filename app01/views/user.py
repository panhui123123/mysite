from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from app01.utils.form import UserModelForm, PrettyModelForm, PrettyEditModelForm


# 展示用户信息
def user_list(request):
    queryset = models.UserInfo.objects.all()
    print(queryset)
    return render(request, 'user_list.html', {'queryset': queryset})


# 用户添加
def user_add(request):
    context = {
        'gender_choice': models.UserInfo.gender_choice,
        'depart': models.Department.objects.all()
    }
    # 如果当前请求为get，直接返回页面
    if request.method == 'GET':
        return render(request, 'user_add.html', context)
    # 否则，获取提交的值
    name = request.POST.get('name')
    password = request.POST.get('password')
    age = request.POST.get('age')
    account = request.POST.get('account')
    create_time = request.POST.get('create_time')
    gender = request.POST.get('gender')
    depart_id = request.POST.get('depart_id')
    # 数据库创建数据
    models.UserInfo.objects.create(name=name, password=password, age=age, account=account, create_time=create_time,
                                   gender=gender, depart_id=depart_id)
    # 重定向到部门列表页面
    return redirect('/user/list/')


# ModelForm视图函数
def user_add_bymf(request):
    # 如果是get请求，创建一个UserModelForm对象，直接返回form
    if request.method == "GET":
        form = UserModelForm
        return render(request, 'user_model_form_add.html', {'form': form})
    # 如果是post请求，在创建UserModelForm对象时需要传入request.POST参数
    form = UserModelForm(data=request.POST)
    # 校验数据
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request, 'user_model_form_add.html', {'form': form})


# 用户删除
def user_delete(request):
    nid = request.GET.get('nid')
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


# 用户编辑，modelform方式
def user_edit(request, nid):
    # 先确定要操作的那一条数据（对象）
    row_obj = models.UserInfo.objects.filter(id=nid).first()
    # 如果是get请求，先把url里面nid拿过来，通过这个nid筛选到那条数据，
    # 然后创建modelform对象（以筛选出来的数据为参数），返回render对象
    if request.method == "GET":
        form = UserModelForm(instance=row_obj)
        return render(request, 'user_edit.html', {'form': form})
    # 如果是post请求，在创建UserModelForm对象时需要传入request.POST参数和instance=row_obj
    form = UserModelForm(data=request.POST, instance=row_obj)
    # 数据校验
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request, "user_edit.html", {'form': form})