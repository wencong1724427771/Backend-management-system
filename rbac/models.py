from django.db import models

# Create your models here.


class Role(models.Model):
    name = models.CharField(max_length=16)
    permissions = models.ManyToManyField("Permission")
    def __str__(self):
        return self.name


class Permission(models.Model):
    title = models.CharField(max_length=32,null=True,blank=True)
    url = models.CharField(max_length=32)
    menus = models.ForeignKey("Menu",null=True,blank=True,on_delete=models.CASCADE)
    parent = models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE)   # 自关联
    url_name = models.CharField(max_length=32, null=True, blank=True)      # url别名
    # menu = models.BooleanField(default=False)      # 新增字段需要给默认值

    def __str__(self):
        return self.title


# 用户表
class UserInfo(models.Model):
    roles = models.ManyToManyField(Role)
    class Meta:
        abstract = True


# 一级菜单数据表
class Menu(models.Model):
    name = models.CharField(max_length=32)
    weight = models.IntegerField(default=100)         # 菜单排序,,权重值越大越靠前
    icon = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        return self.name


'''
一级菜单
id  name     icon
1   业务系统  
2   教务系统

权限表
id    title   url             menus_id
1     客户展示  /customer/      1
2     客户添加  /customer_add/  None
3     私户信息  /mycustomer/    1
3     课程记录  /course_list/   2
3     课程添加  /course_add/    None
'''



