from django.contrib import admin

from rbac import models
# Register your models here.

class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id','title','url','menus','parent','url_name']    # 主键必须展示
    list_editable = ['title','url','menus','parent','url_name']


# 权限
# 公户信息和课程记录
admin.site.register(models.Role)
admin.site.register(models.Permission,PermissionAdmin)
admin.site.register(models.Menu)
