from django.db import models


# Create your models here.
class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name='部门', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name='姓名', max_length=10)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    # 薪水，整数位10，小数位2，默认值0
    account = models.DecimalField(verbose_name='薪资', max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name='入职时间')
    # 外键，关联部门表里面的id,级联删除，如果部门表里面该id被删除，则删除员工表对应数据
    depart = models.ForeignKey(verbose_name='部门', to='Department', to_field='id', on_delete=models.CASCADE)
    # # 如果部门表里面该id被删除，则对应表里面字段置空
    # depart = models.ForeignKey(to='Department', to_field='id', null=True, blank=True, on_delete=models.SET_NULL)

    # django约束
    gender_choice = (
        (1, '男'),
        (2, '女')
    )
    # 男或者女，int类型
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choice)


class PrettyNum(models.Model):
    """ 靓号表 """
    # 号码
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    # 价格
    price = models.IntegerField(verbose_name="价格")
    # 等级
    level_choice = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choice, default=1)
    # 状态
    status_choice = (
        (1, "已占用"),
        (2, "未使用")
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choice, default=2)