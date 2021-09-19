# -*- coding = utf-8 -*-
# @Time: 2021/8/30 17:07
# @Author: Bon
# @File: mytag.py
# @Software: PyCharm
import re
from django import template



register = template.Library()

@register.inclusion_tag('menu.html')   # 返回html片段
def menu(request):
    menu_dict = request.session.get('menu_dict')
    # print(menu_dict)
    # path = request.path
    for k,v in menu_dict.items():
        v['class'] = ''
        for i in v['children']:
            # res = '/sales'+i['url']     # 处理命名空间sales和存储在数据库的url不一致问题
            # if re.match(res,path):      # 如果是二级菜单路径或二级菜单下的url
            # print(request.session.get('pid'),i['second_menu_id'],'oooxxx')
            if request.pid == i['second_menu_id']:      # 如果是二级菜单路径或二级菜单下的url
                v['class'] = 'show'
                v['class1'] = 'menu-open'    # 根据自带折叠二级菜单属性添加类值
                i['class'] = 'active'        # 二级菜单选中效果

    menu_data = {'menu_dict':menu_dict}
    return menu_data     # 把数据传给menu.html页面


@register.inclusion_tag('breadcrumb.html')
def breadcrumb(request):
    bread_crumb = request.bread_crumb
    data = {'bread_crumb':bread_crumb}
    return data


# 精确到按钮级别
@register.filter
def has_permission(request,permission):
    if permission in request.session.get('url_name'):
        return True


@register.simple_tag
def gen_role_url(request,rid):
    params = request.GET.copy()
    params._mutable = True
    params['rid'] = rid
    # print(params,'xxx')    # <QueryDict: {'uid': ['2'], 'rid': [1]}> xxx
    # print(request.GET)     # <QueryDict: {'uid': ['2'], 'rid': [1]}>
    # print(params.urlencode())
    return params.urlencode()


# @register.filter
# def menu(request):
#     menu_list = request.session.get('menu_list')
#     print(menu_list,'xxxx')
#     '''
#     [{'permissions__url': '/customers/', 'permissions__menu': True, 'permissions__icon': 'fa-address-card-o'},'permissions__title': '客户信息'}
#     {'permissions__url': '/mycustomers/', 'permissions__menu': True, 'permissions__icon': 'fa-user-circle-o'},'permissions__title': '私户信息']
#     '''
#     return menu_list

# @register.filter
# def add_prefix(url):
#     menu_url_path='/sales' + url
#     # print(menu_url_path,'ooo')
#     return menu_url_path