from django.shortcuts import render, redirect
from django import forms
from app01 import models
from app01.utils.encrypt import md5
from app01.utils.bootstrap import BootStrapForm


class LoginForm(BootStrapForm):
    username = forms.CharField(label='用户名', widget=forms.TextInput, required=True)
    password = forms.CharField(label='密码', widget=forms.PasswordInput(render_value=True), required=True)

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        admin_obj = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_obj:
            form.add_error("password", "用户名或者密码错误")
            return render(request, 'login.html', {'form': form})
        request.session['info'] = {'id': admin_obj.id, 'name': admin_obj.username}
        
        return redirect('/admin/list/')
    return render(request, 'login.html', {'form': form})