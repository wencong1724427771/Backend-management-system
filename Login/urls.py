"""Login URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path

from sales import views
urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path('^login/', views.login,name='login'),
    re_path('^register/', views.register,name='register'),
    re_path('^home/$', views.home,name='home'),

    # 客服信息展示
    re_path('^customers/$', views.customers,name='customers'),
    # 添加客户
    re_path('^addcustomer/$', views.addEditCustomer,name='addcustomer'),
    # 编辑客户
    re_path('^editcustomer/(\d+)/$', views.addEditCustomer,name='editcustomer'), #--添加删除使用同一个html页面

]
