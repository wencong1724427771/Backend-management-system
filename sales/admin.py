from django.contrib import admin

from sales import models
# Register your models here.


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['id','username','telephone']


class ConsultRecordAdmin(admin.ModelAdmin):
    exclude = ['delete_status']


class CourseRecordAdmin(admin.ModelAdmin):
    list_display = ['id','day_num','course_title','re_class','teacher']
    list_editable = ['day_num','course_title','re_class','teacher']


admin.site.register(models.UserInfo,UserInfoAdmin)
admin.site.register(models.Department)
admin.site.register(models.ClassList)
admin.site.register(models.Campuses)
admin.site.register(models.Customer)
admin.site.register(models.Enrollment)
admin.site.register(models.ConsultRecord,ConsultRecordAdmin)
admin.site.register(models.CourseRecord,CourseRecordAdmin)
admin.site.register(models.StudyRecord)


# 权限
# 公户信息和课程记录
# admin.site.register(models.Role)
# admin.site.register(models.Permission)
