from django.shortcuts import render, redirect, HttpResponse
from django.http.response import JsonResponse
import time
from app01 import models
from faker import Faker
from django import forms
import re
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01.utils.pagination import Pagination


# Create your views here.
def index(request):
    fk = Faker(locale='zh-CN')
    name = fk.name()
    return render(request, 'index.html', {'name': name})


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


# 展示用户信息
def user_list(request):
    queryset = models.UserInfo.objects.all()
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


# 创建一个UserModelForm类，把UserInfo这张表里面的所有数据库字段封装起来，方便后续使用
class UserModelForm(forms.ModelForm):
    class Meta:
        # 创建一个model对象
        model = models.UserInfo
        # 取出相应的数据库字段
        fields = ['name', 'password', 'age', 'account', 'create_time', 'depart', 'gender']
        # fields = "__all__"
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        #     "account": forms.TextInput(attrs={"class": "form-control"}),
        #     "create_time": forms.TextInput(attrs={"class": "form-control"}),
        #     "depart": forms.TextInput(attrs={"class": "form-control"}),
        #     "gender": forms.TextInput(attrs={"class": "form-control"}),
        # }

    # 重写init方法，会把每个字段在显示的时候给自定义样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 遍历每一个字段，自动加上样式
        for name, field in self.fields.items():
            # 如果是密码，则把输入样式改为密码框
            if name == "password":
                field.widget.input_type = "password"
            field.widget.attrs = {"class": "form-control", "placeholder": "请输入" + field.label}


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


# 靓号列表
def pretty_list(request):
    data = {}
    # 获取前端传的query参数，如果没有就空字符串
    search_data = request.GET.get("query", "")
    # 如果参数不为空，则传入字典，mobile__contains是固定写法，表示我的搜索是包含搜索
    if search_data:
        data["mobile__contains"] = search_data
    # 注意，我们获取queryset的时候可以排序，加-表示倒叙排列，不加-表示正序排列
    queryset = models.PrettyNum.objects.filter(**data).order_by("-level")
    # 创建一个分页插件类
    page = Pagination(request, queryset, page_param="page", page_size=10, plus=3)
    context = {
        "queryset": page.page_queryset,  # 分完页的数据（当前页）
        "page_string": page.html(),  # 页码显示
        "search_data": search_data
    }

    # 返回的时候返回search_data，因为前端页面要展示
    return render(request, "pretty_list.html", context)


class PrettyModelForm(forms.ModelForm):
    # 验证输入字段方式1：为每个数据库字段设置正则
    # mobile = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    # )

    class Meta:
        model = models.PrettyNum
        fields = "__all__"

    # 重写init方法，会把每个字段在显示的时候给自定义样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 遍历每一个字段，自动加上样式
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": "请输入" + field.label}

    # 验证方式2：钩子方法
    def clean_mobile(self):
        # 获取用户输入
        mobile_txt = self.cleaned_data['mobile']
        # 正则匹配，不成功报错
        if not re.match(r'^1[3-9]\d{9}$', mobile_txt):
            raise ValidationError("手机号格式错误")
        # 不允许重复添加手机号
        if models.PrettyNum.objects.filter(mobile=mobile_txt).exists():
            raise ValidationError("手机号已存在")
        # 成功直接返回值
        return mobile_txt


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


class PrettyEditModelForm(forms.ModelForm):
    # 重定义mobile字段，编辑页面不允许编辑手机号
    mobile = forms.CharField(disabled=True, label='手机号')
    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]

    # 重写init方法，会把每个字段在显示的时候给自定义样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 遍历每一个字段，自动加上样式
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": "请输入" + field.label}


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