from django.contrib import admin

# Register your models here.
from sales import models

admin.site.register(models.UserInfo)
admin.site.register(models.Department)
admin.site.register(models.ClassList)
admin.site.register(models.Campuses)
admin.site.register(models.Customer)