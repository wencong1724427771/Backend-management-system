from django.urls import re_path
from rbac import views

app_name = 'rbac'

urlpatterns = [

    # rbac应用的路由
    # 角色管理
    re_path('^role/list/',views.role_list,name='role_list'),
    re_path('^role/add/',views.role_add_edit,name='role_add'),
    re_path(r'^role/edit/(\d+)/', views.role_add_edit,name='role_edit'),    #/rbac/customer/
    re_path(r'^role/del/(\d+)/', views.role_del,name='role_del'),    #/rbac/customer/

    # 菜单管理
    re_path(r'^menu/list/', views.menu_list, name='menu_list'),
    re_path(r'^menu/add/', views.menu_add_edit, name='menu_add'),
    re_path(r'^menu/edit/(\d+)/', views.menu_add_edit, name='menu_edit'),
    re_path(r'^menu/del/(\d+)/', views.menu_del, name='menu_del'),

    # 批量操作权限
    re_path(r'^multi/permissions/$', views.multi_permissions, name='multi_permissions'),
    re_path(r'^permission/del/(\d+)/$', views.permission_del, name='permission_del'),

    # 权限分配
    re_path(r'^distribute/permission/$', views.distribute_permission, name='distribute/permission'),
]
