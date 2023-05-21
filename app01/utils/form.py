from app01 import models
from django import forms
import re
from django.core.exceptions import ValidationError
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.encrypt import md5


# 创建一个UserModelForm类，把UserInfo这张表里面的所有数据库字段封装起来，方便后续使用
class UserModelForm(BootStrapModelForm):
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
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # 遍历每一个字段，自动加上样式
    #     for name, field in self.fields.items():
    #         # 如果是密码，则把输入样式改为密码框
    #         if name == "password":
    #             field.widget.input_type = "password"
    #         field.widget.attrs = {"class": "form-control", "placeholder": "请输入" + field.label}


class PrettyModelForm(BootStrapModelForm):
    # 验证输入字段方式1：为每个数据库字段设置正则
    # mobile = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    # )

    class Meta:
        model = models.PrettyNum
        fields = "__all__"

    # 重写init方法，会把每个字段在显示的时候给自定义样式
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # 遍历每一个字段，自动加上样式
    #     for name, field in self.fields.items():
    #         field.widget.attrs = {"class": "form-control", "placeholder": "请输入" + field.label}

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


class PrettyEditModelForm(BootStrapModelForm):
    # 重定义mobile字段，编辑页面不允许编辑手机号
    mobile = forms.CharField(disabled=True, label='手机号')

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]

    # 重写init方法，会把每个字段在显示的时候给自定义样式
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # 遍历每一个字段，自动加上样式
    #     for name, field in self.fields.items():
    #         field.widget.attrs = {"class": "form-control", "placeholder": "请输入" + field.label}


class AdminModelForm(BootStrapModelForm):
    # 重新定义一个确认密码字段
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput
        }

    # 利用钩子函数加密,使存在数据库中的信息为密文
    def clean_password(self):
        password = self.cleaned_data.get("password")
        return md5(password)

    # 钩子函数,用来校验密码和确认密码是否一致
    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = md5(self.cleaned_data.get("confirm_password"))
        if password != confirm_password:
            raise ValidationError("两次输入密码不一致")
        return confirm_password


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]


class AdminResetModelForm(BootStrapModelForm):
    username = forms.CharField(disabled=True, label='正在要被重置的用户名')
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput,
        }

    # 利用钩子函数加密,使存在数据库中的信息为密文
    def clean_password(self):
        password = self.cleaned_data.get("password")
        password_md5 = md5(password)
        exists = models.Admin.objects.filter(id=self.instance.pk, password=password_md5).exists()
        if exists:
            raise ValidationError("密码不能与上一次一样")
        return password_md5

    # 钩子函数,用来校验密码和确认密码是否一致
    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = md5(self.cleaned_data.get("confirm_password"))
        if password != confirm_password:
            raise ValidationError("两次输入密码不一致")
        return confirm_password

