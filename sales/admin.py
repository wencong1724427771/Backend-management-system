from django.contrib import admin

# Register your models here.
from sales import models

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['id','username','telephone']


admin.site.register(models.UserInfo,UserInfoAdmin)
admin.site.register(models.Department)
admin.site.register(models.ClassList)
admin.site.register(models.Campuses)
admin.site.register(models.Customer)

admin.site.register(models.ConsultRecord)
admin.site.register(models.Enrollment)    # 报名表
admin.site.register(models.CourseRecord)
admin.site.register(models.StudyRecord)
