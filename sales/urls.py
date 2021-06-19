from django.urls import re_path
from sales.views import customer_views,login_views

app_name = 'sales'   #声明namesapce为app01


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

]
