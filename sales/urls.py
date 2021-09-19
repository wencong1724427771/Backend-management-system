from django.urls import re_path
from sales.views import login_views,customer_views

app_name = 'sales'

urlpatterns = [
    # 登录
    re_path('^login/', login_views.login, name='login'),  # url别名
    # 注销登录
    re_path('^logout/', login_views.logout, name='logout'),
    # 注册
    re_path('^register/', login_views.register, name='register'),
    # 主页
    re_path('^home/', customer_views.home, name='home'),


    # 公户信息展示
    re_path(r'^customers/', customer_views.Customers.as_view(), name='customers'),
    # 私户信息展示
    re_path(r'^mycustomers/', customer_views.Customers.as_view(), name='mycustomers'),
    # 添加客户
    re_path(r'^addcustomer/', customer_views.addEditCustomer, name='addcustomer'),
    # 编辑客户
    re_path(r'^editcustomer/(\d+)/', customer_views.addEditCustomer, name='editcustomer'),

    # 跟进记录展示
    re_path('^consultrecords/$', customer_views.ConsultRecord.as_view(),name='consultrecords'),
    # 添加跟进记录
    re_path('^addconsultrecords/$', customer_views.addEditConsultRecord,name='addconsultrecords'),
    # 编辑跟进记录
    re_path('^editconsultrecords/(\d+)/$', customer_views.addEditConsultRecord,name='editconsultrecords'),

    # 报名记录展示
    re_path('^enrollments/$', customer_views.Enrollment.as_view(),name='enrollments'),
    # 添加报名记录
    re_path('^addenrollments/$', customer_views.addEditEnrollment,name='addenrollments'),
    # 编辑报名记录
    re_path('^editenrollments/(\d+)/$', customer_views.addEditEnrollment,name='editenrollments'),

    # 展示课程记录
    re_path('^courserecord/', customer_views.CourseRecord.as_view(),name='courserecord'),
    # 添加课程记录
    re_path('^addcourse_record/$', customer_views.addEditCourseRecord,name='addcourse_record'),
    # 编辑课程记录
    re_path('^editcourse_record/(\d+)', customer_views.addEditCourseRecord,name='editcourse_record'),

    # 学习记录展示
    re_path('^studyrecord/(\d+)', customer_views.StudyRecord.as_view(),name='studyrecord'),
]

