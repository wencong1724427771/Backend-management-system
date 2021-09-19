from collections import OrderedDict   # 3.6之后默认有序

from rbac import models


# 往session中注入数据
def init_permission(request,user_obj):
    # 登录成功之后，注入用户权限
    permission_list = models.Role.objects.filter(userinfo__username=user_obj.username). \
        values('permissions__url',
               'permissions__title',
               'permissions__menus__icon',
               'permissions__menus__pk',
               'permissions__menus__name',
               'permissions__menus__weight',
               'permissions__parent_id',
               'permissions__pk',
               'permissions__url_name',        # 别名
               ).distinct()                   # 去重，身兼多职的情况
    # request.session["permission_list"] = list(permission_list)        # Object of type QuerySet is not JSON serializable
    # 构建新的数据类型permission_dict字典,键为permissions__pk,值还是为原来permission_list的字典;
    # 目的:优化处理面包屑二级菜单子权限按钮时,需要频繁访问数据库的问题。
    permission_dict={}

    # url别名,控制二级菜单子权限按钮的显示和隐藏
    url_names = []  # url别名

    # print(permission_list)
    '''
       <QuerySet     # 用户登录后拥有的权限路径
       [{'permissions__url': '/customers/', 'permissions__title': '客户管理', 'permissions__menus__icon': 'fa-address-card-o', 'permissions__menus__pk': 1, 'permissions__menus__name': '业务系统'},
        {'permissions__url': '/mycustomers/', 'permissions__title': '私户信息展示', 'permissions__menus__icon': 'fa-address-card-o', 'permissions__menus__pk': 1, 'permissions__menus__name': '业务系统'},
         {'permissions__url': '/editcustomer/(\\d+)/', 'permissions__title': '编辑客户', 'permissions__menus__icon': None, 'permissions__menus__pk': None, 'permissions__menus__name': None},
          {'permissions__url': '/addcustomer/', 'permissions__title': '添加客户', 'permissions__menus__icon': None, 'permissions__menus__pk': None, 'permissions__menus__name': None}, 
          {'permissions__url': '/courserecord/', 'permissions__title': '课程记录展示', 'permissions__menus__icon': 'fa-user-circle-o', 'permissions__menus__pk': 2, 'permissions__menus__name': '教务系统'}, 
          {'permissions__url': '/addcourse_record/', 'permissions__title': '添加课程记录', 'permissions__menus__icon': None, 'permissions__menus__pk': None, 'permissions__menus__name': None}, 
          {'permissions__url': '/editcourse_record/(\\d+)', 'permissions__title': '编辑课程记录', 'permissions__menus__icon': None, 'permissions__menus__pk': None, 'permissions__menus__name': None}
        ]>
    '''

    # 构造左侧菜单数据结构
    menu_dict = {}
    for i in permission_list:
        permission_dict[i.get('permissions__pk')] = i
        url_names.append(i.get('permissions__url_name'))  # 添加url别名
        if i.get('permissions__menus__pk'):
        # 如果permission__menu__pk已经在menu_dict中存在,只需在children中添加对应的二级菜单就行.
        # 如果permission__menu__pk不存在于menu_dict中,生成新的键值对数据
            if i.get('permissions__menus__pk') in menu_dict:
                menu_dict[i.get('permissions__menus__pk')]['children'].append(
                    {'title': i.get('permissions__title'), 'url': i.get('permissions__url'),
                     'second_menu_id':i.get('permissions__pk')},
                )
            else:
                menu_dict[i.get('permissions__menus__pk')] = {
                    'name':i.get('permissions__menus__name'),
                    'icon':i.get('permissions__menus__icon'),
                    'weight':i.get('permissions__menus__weight'),
                    'children':[
                        {'title':i.get('permissions__title'),
                         'url':i.get('permissions__url'),
                         'second_menu_id':i.get('permissions__pk')
                         },
                    ],
                }
    # print(menu_dict)
    # request.session["menu_dict"] = menu_dict   # 把构造好的数据结构注入到session中
    '''
     { # 1是一级菜单的id
        1: {
            'name': '业务系统',
            'icon': 'fa-address-card-o',
            'weight': '100',
            'children': [{
                'title': '客户管理',
                'url': '/customers/'
            }, {
                'title': '私户信息展示',
                'url': '/mycustomers/'
                }]
            },
        2: {
            'name': '教务系统',
            'icon': 'fa-user-circle-o',
            'weight': '90',
            'children': [{
                'title': '课程记录展示',
                'url': '/courserecord/'
            }]
        }
    '''
    # 有序字典,按权重排序
    sort_d1 = sorted(menu_dict, key=lambda x: menu_dict[x]['weight'], reverse=True)  # x是字典的键

    order_dict = OrderedDict()
    for key in sort_d1:
        order_dict[key] = menu_dict[key]

    request.session["permission_dict"] = permission_dict    # 新的字典类型的权限数据结构｛1:{},2:{}｝
    request.session["menu_dict"] = order_dict   # 把排序好的数据结构注入到session中
    request.session["url_names"] = url_names   # 把url别名注入到session中,在控制子权限按钮时使用




