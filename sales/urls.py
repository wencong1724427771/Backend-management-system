from django.urls import re_path
from sales.views import customer_views,login_views

app_name = 'sales'


urlpatterns = [
    # 登录
    re_path('^login/', login_views.login, name='login'),
    # 注销
    re_path('^logout/', login_views.logout, name='logout'),
    # 注册
    re_path('^register/', login_views.register, name='register'),
    # 首页
    re_path('^home/$', customer_views.home, name='home'),
    # 用于测试
    re_path('^test/$', customer_views.test, name='test'),

    # 公户信息展示
    re_path('^customers/$', customer_views.Customers.as_view(),name='customers'),
    # 私户信息展示
    re_path('^mycustomers/$',customer_views.Customers.as_view(),name='mycustomers'),
    # 添加客户
    re_path('^addcustomer/$',customer_views.addEditCustomer,name='addcustomer'),
    # 编辑客户
    re_path('^editcustomer/(\d+)/', customer_views.addEditCustomer,name='editcustomer'),

    # 跟进记录展示
    re_path('^consultrecords/$', customer_views.ConsultRecord.as_view(),name='consultrecords'),
    # 添加跟进记录
    re_path('^addconsult_record/$',customer_views.addEditConsultRecord,name='addconsult_record'),
    # 编辑跟进记录
    re_path('^editconsult_record/(\d+)/', customer_views.addEditConsultRecord,name='editconsult_record'),

    # 展示报名信息
    re_path('^enrollment/', customer_views.Enrollment.as_view(),name='enrollment'),
    # 添加报名信息
    re_path('^addenrollment/$', customer_views.addEditEnrollment,name='addenrollment'),
    # 编辑报名信息
    re_path('^editenrollment/(\d+)', customer_views.addEditEnrollment,name='editenrollment'),

    # 展示课程记录
    re_path('^courserecord/', customer_views.CourseRecord.as_view(),name='courserecord'),
    # 添加课程记录
    re_path('^addcourse_record/$', customer_views.addEditCourseRecord,name='addcourse_record'),
    # 编辑课程记录
    re_path('^editcourse_record/(\d+)', customer_views.addEditCourseRecord,name='editcourse_record'),

    # 学习记录展示
    re_path('^studyrecord/(\d+)', customer_views.StudyRecord.as_view(),name='studyrecord'),
]
