from django.contrib import admin

# Register your models here.
from sales import models

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['id','username','telephone']

class CourseRecordAdmin(admin.ModelAdmin):
    list_display = ['id','day_num','course_title','re_class','teacher']
    list_editable = ['day_num','course_title','re_class','teacher']

class StudentRecordAdmin(admin.ModelAdmin):
    list_display = ['id','attendance','score','student',]
    list_editable = ['attendance','score','student',]


admin.site.register(models.UserInfo,UserInfoAdmin)
admin.site.register(models.Department)
admin.site.register(models.ClassList)
admin.site.register(models.Campuses)
admin.site.register(models.Customer)

admin.site.register(models.ConsultRecord)
admin.site.register(models.Enrollment)    # 报名表
admin.site.register(models.CourseRecord,CourseRecordAdmin)
admin.site.register(models.StudyRecord,StudentRecordAdmin)
