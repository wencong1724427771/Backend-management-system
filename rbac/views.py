from django.shortcuts import render,redirect,HttpResponse
from rbac import models
from django import forms
# Create your views here.


def role_list(request):
    role_list = models.Role.objects.all()
    return render(request, 'role_list.html',{'role_list':role_list})


class RoleModelForm(forms.ModelForm):
    class Meta:
        model = models.Role
        fields = '__all__'
        exclude = ['permissions', ]

    widgets = {
        'name':forms.TextInput(attrs={'class':'form-control'}),
    }


icon_list = [['fa fa-font-awesome', '<i class="fa fa-font-awesome" aria-hidden="true"></i>'],
             ['fa fa-flag fa-fw', '<i class="fa fa-flag fa-fw" aria-hidden="true"></i>'],
             ['fa fa-wheelchair-alt fa-fw', '<i class="fa fa-wheelchair-alt fa-fw" aria-hidden="true"></i>'],
             ['fa fa-camera-retro fa-fw', '<i class="fa fa-camera-retro fa-fw" aria-hidden="true"></i>'],
             ['fa fa-universal-access fa-fw', '<i class="fa fa-universal-access fa-fw" aria-hidden="true"></i>'],
             ['fa fa-hand-spock-o fa-fw', '<i class="fa fa-hand-spock-o fa-fw" aria-hidden="true"></i>'],
             ['fa fa-ship fa-fw', '<i class="fa fa-ship fa-fw" aria-hidden="true"></i>'],
             ['fa fa-venus fa-fw', '<i class="fa fa-venus fa-fw" aria-hidden="true"></i>'],
             ['fa fa-file-image-o fa-fw', '<i class="fa fa-file-image-o fa-fw" aria-hidden="true"></i>'],
             ['fa fa-spinner fa-fw', '<i class="fa fa-spinner fa-fw" aria-hidden="true"></i>'],
             ['fa fa-check-square fa-fw', '<i class="fa fa-check-square fa-fw" aria-hidden="true"></i>'],
             ['fa fa-credit-card fa-fw', '<i class="fa fa-credit-card fa-fw" aria-hidden="true"></i>'],
             ['fa fa-pie-chart fa-fw', '<i class="fa fa-pie-chart fa-fw" aria-hidden="true"></i>'],
             ['fa fa-won fa-fw', '<i class="fa fa-won fa-fw" aria-hidden="true"></i>'],
             ['fa fa-file-text-o fa-fw', '<i class="fa fa-file-text-o fa-fw" aria-hidden="true"></i>'],
             ['fa fa-arrow-right fa-fw', '<i class="fa fa-arrow-right fa-fw" aria-hidden="true"></i>'],
             ['fa fa-play-circle fa-fw', '<i class="fa fa-play-circle fa-fw" aria-hidden="true"></i>'],
             ['fa fa-facebook-official fa-fw', '<i class="fa fa-facebook-official fa-fw" aria-hidden="true"></i>'],
             ['fa fa-medkit fa-fw', '<i class="fa fa-medkit fa-fw" aria-hidden="true"></i>'],
             ['fa fa-flag', '<i class="fa fa-flag" aria-hidden="true"></i>'],
             ['fa fa-search', '<i class="fa fa-search" aria-hidden="true"></i>'],
             ['fa fa-address-book', '<i class="fa fa-address-book" aria-hidden="true"></i>'],
             ['fa fa-address-book-o', '<i class="fa fa-address-book-o" aria-hidden="true"></i>'],
             ['fa fa-address-card', '<i class="fa fa-address-card" aria-hidden="true"></i>'],
             ['fa fa-address-card-o', '<i class="fa fa-address-card-o" aria-hidden="true"></i>'],
             ['fa fa-bandcamp', '<i class="fa fa-bandcamp" aria-hidden="true"></i>'],
             ['fa fa-bath', '<i class="fa fa-bath" aria-hidden="true"></i>'],
             ['fa fa-bathtub', '<i class="fa fa-bathtub" aria-hidden="true"></i>'],
             ['fa fa-drivers-license', '<i class="fa fa-drivers-license" aria-hidden="true"></i>'],
             ['fa fa-drivers-license-o', '<i class="fa fa-drivers-license-o" aria-hidden="true"></i>'],
             ['fa fa-eercast', '<i class="fa fa-eercast" aria-hidden="true"></i>'],
             ['fa fa-envelope-open', '<i class="fa fa-envelope-open" aria-hidden="true"></i>'],
             ['fa fa-envelope-open-o', '<i class="fa fa-envelope-open-o" aria-hidden="true"></i>'],
             ['fa fa-etsy', '<i class="fa fa-etsy" aria-hidden="true"></i>'],
             ['fa fa-free-code-camp', '<i class="fa fa-free-code-camp" aria-hidden="true"></i>'],
             ['fa fa-grav', '<i class="fa fa-grav" aria-hidden="true"></i>'],
             ['fa fa-handshake-o', '<i class="fa fa-handshake-o" aria-hidden="true"></i>'],
             ['fa fa-id-badge', '<i class="fa fa-id-badge" aria-hidden="true"></i>'],
             ['fa fa-id-card', '<i class="fa fa-id-card" aria-hidden="true"></i>'],
             ['fa fa-id-card-o', '<i class="fa fa-id-card-o" aria-hidden="true"></i>'],
             ['fa fa-imdb', '<i class="fa fa-imdb" aria-hidden="true"></i>'],
             ['fa fa-linode', '<i class="fa fa-linode" aria-hidden="true"></i>'],
             ['fa fa-meetup', '<i class="fa fa-meetup" aria-hidden="true"></i>'],
             ['fa fa-microchip', '<i class="fa fa-microchip" aria-hidden="true"></i>'],
             ['fa fa-podcast', '<i class="fa fa-podcast" aria-hidden="true"></i>'],
             ['fa fa-quora', '<i class="fa fa-quora" aria-hidden="true"></i>'],
             ['fa fa-ravelry', '<i class="fa fa-ravelry" aria-hidden="true"></i>'],
             ['fa fa-s15', '<i class="fa fa-s15" aria-hidden="true"></i>'],
             ['fa fa-shower', '<i class="fa fa-shower" aria-hidden="true"></i>']]

from django.utils.safestring import mark_safe

class MenuModelForm(forms.ModelForm):
    class Meta:
        model = models.Menu
        fields = '__all__'

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'weight':forms.TextInput(attrs={'class':'form-control'}),
            # 'icon':forms.TextInput(attrs={'class':'form-control'}),
            'icon':forms.RadioSelect(choices=([[i[0],mark_safe(i[1])] for i in icon_list]))   # 图标选择
            # (['fa fa-shower', '<i class="fa fa-shower" aria-hidden="true"></i>']) # 提交索引为0的数据,显示索引为1的数据；补充：models中的默认都是第一个，可借助get_xx__display方法取第二个
        }


def role_add_edit(request,n=None):
    role_obj = models.Role.objects.filter(pk=n).first()
    if request.method == 'GET':
        form_obj = RoleModelForm(instance=role_obj)   # instance不为空表示编辑
        return render(request, 'form.html', {'form_obj':form_obj})
    else:
        form_obj = RoleModelForm(request.POST,instance=role_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('rbac:role_list')
        else:
            return render(request, 'form.html', {'form_obj':form_obj})

def role_del(request,n):
    models.Role.objects.filter(pk=n).delete()
    return redirect('rbac:role_list')


from django.db.models import Q


def menu_list(request):
    menu_id = request.GET.get('mid')
    menu_list = models.Menu.objects.all()

    if menu_id:
        permission_list = models.Permission.objects.filter(Q(menus_id=menu_id) | Q(parent__menus_id=menu_id)).values(
            'id', 'title', 'url', 'url_name', 'menus__id',
            'menus__name', 'menus__icon', 'parent_id')
    else:
        permission_list = models.Permission.objects.all().values('id', 'title', 'url', 'url_name', 'menus__id',
                                                                 'menus__name', 'menus__icon', 'parent_id')

    '''


    id  title  menus_id  parent_id
    1   客户展示  1        none
    2   客户添加  none     1
    3   客户编辑  none     1

    id  title  menus_id  parent_id
    1   客户展示  1        none
    2   客户添加  none     1
    3   客户编辑  none     1

    '''

    # print(permission_list)
    permission_dict = {}
    for permission in permission_list:
        pid = permission.get('menus__id')
        if pid:
            permission_dict[permission.get('id')] = permission
            permission_dict[permission.get('id')]['children'] = []
    # print(permission_dict)

    for p in permission_list:
        parent_id = p.get('parent_id')
        if parent_id:  # 1
            permission_dict[parent_id]['children'].append(p)

    # print(permission_dict)
    '''
    {
        pid:{
             'title':'角色展示',
             'url':xx

            'children':[

            ]

        },
        pid:{
             'title':'角色展示',
             'url':xx

            'children':[
                {'title':'角色添加',}
            ]

        }

    }

    '''

    # print('>>>',permission_dict.values())
    # print(menu_list)    # <QuerySet [<Menu: 业务系统>, <Menu: 教务系统>, <Menu: 权限系统>, <Menu: 大锤>]>
    # print(menu_list.values())
    return render(request, 'menu_list.html',
                  {'menu_list': menu_list, 'permission_list': permission_dict.values(), 'menu_id': menu_id})


def menu_add_edit(request, n=None):
    menu_obj = models.Menu.objects.filter(pk=n).first()
    if request.method == 'GET':
        form_obj = MenuModelForm(instance=menu_obj)
        return render(request, 'form.html', {'form_obj': form_obj})
    else:
        form_obj = MenuModelForm(request.POST, instance=menu_obj)
        if form_obj.is_valid():
            # print(form_obj.cleaned_data)
            form_obj.save()
            return redirect('rbac:menu_list')

        else:
            return render(request, 'form.html', {'form_obj': form_obj})


def menu_del(request, n):
    models.Menu.objects.filter(pk=n).delete()
    return redirect('rbac:menu_list')



from django.forms import modelformset_factory, formset_factory
from rbac.utils.routes import get_all_url_dict
from rbac.forms import MultiPermissionForm


# def xx(request):
#     return HttpResponse('xxxxx')


def multi_permissions(request):
    """
    批量操作权限
    :param request:
    :return:
    """

    post_type = request.GET.get('type')  # add

    # 更新和编辑用的
    FormSet = modelformset_factory(models.Permission, MultiPermissionForm, extra=0)
    # 增加用的
    AddFormSet = formset_factory(MultiPermissionForm, extra=0)
    # FormSet(queyset=)
    # 查询数据库所有权限
    permissions = models.Permission.objects.all()

    # 获取路由系统中所有URL
    router_dict = get_all_url_dict(ignore_namespace_list=['admin', ])
    # url_ordered_dict['web:role_list'] = {'name': 'web:role_list', 'url': '/role/list/'}
    '''
    router_dict = {
        'web:role_list':{'name': 'web:role_list', 'url': '/role/list/'},
    }
    '''
    # 数据库中的所有权限的别名
    permissions_name_set = set([i.url_name for i in permissions])

    # 路由系统中的所有权限的别名
    router_name_set = set(router_dict.keys())

    if request.method == 'POST' and post_type == 'add':
        add_formset = AddFormSet(request.POST)
        if add_formset.is_valid():
            # print(add_formset.cleaned_data)

            permission_obj_list = [models.Permission(**i) for i in add_formset.cleaned_data]
            # print(permission_obj_list)
            '''
            [{'title': 'xx', 'url': '/sales/login/', 'url_name': 'sales:login', 'parent': None, 'menus': None},
             {'title': 'xx', 'url': '/sales/logout/', 'url_name': 'sales:logout', 'parent': None, 'menus': None}, 
             {'title': 'xx', 'url': '/sales/register/', 'url_name': 'sales:register', 'parent': None, 'menus': None}, 
             {'title': 'xxx', 'url': '/sales/home/', 'url_name': 'sales:home', 'parent': None, 'menus': None}]
             [<Permission: xx>, <Permission: xx>, <Permission: xx>, <Permission: xxx>]
            '''

            query_list = models.Permission.objects.bulk_create(permission_obj_list)

            for i in query_list:
                permissions_name_set.add(i.url_name)

    add_name_set = router_name_set - permissions_name_set  # 新增的url别名信息

    add_formset = AddFormSet(initial=[row for name, row in router_dict.items() \
                                      if name in add_name_set])
    # print('>>>>>>>>>>',
    #       [row for name, row in router_dict.items() \
    #        if name in add_name_set]
    #       )
    '''
    [{
            'name': 'web:login',
            'url': '/login/'
        }, {
            'name': 'web:index',
            'url': '/index/'
        }, {
            'name': 'rbac:menu_list',
            'url': '/rbac/menu/list/'
        }, {
            'name': 'rbac:menu_add',
            'url': '/rbac/menu/add/'
        }, {
            'name': 'rbac:menu_edit',
            'url': '/rbac/menu/edit/(\\d+)/'
        }, {
            'name': 'rbac:menu_del',
            'url': '/rbac/menu/del/(\\d+)/'
        }, {
            'name': 'rbac:multi_permissions',
            'url': '/rbac/multi/permissions/'
        }, {
            'name': 'xx',
            'url': '/xx'
        }]

    '''
    del_name_set = permissions_name_set - router_name_set  # 要删除的url别名信息
    del_formset = FormSet(queryset=models.Permission.objects.filter(url_name__in=del_name_set))
    # if request.method == 'POST' and post_type == 'delete':
    #     print(request.POST)

    update_name_set = permissions_name_set & router_name_set
    update_formset = FormSet(queryset=models.Permission.objects.filter(url_name__in=update_name_set))

    if request.method == 'POST' and post_type == 'update':
        update_formset = FormSet(request.POST)
        if update_formset.is_valid():
            update_formset.save()

            update_formset = FormSet(queryset=models.Permission. \
                                     objects.filter(url_name__in=update_name_set))

    return render(
        request,
        'multi_permissions.html',
        {
            'del_formset': del_formset,
            'update_formset': update_formset,
            'add_formset': add_formset,
        }
    )


def permission_del(request,n):
    models.Permission.objects.get(pk=n).delete()
    return redirect('rbac:multi_permissions')



from sales.models import UserInfo
def distribute_permission(request):
    '''
    分配权限
    :param request:
    :return:
    '''
    uid = request.GET.get('uid')   # None
    rid = request.GET.get('rid')   # None
    print(rid,uid)
    if request.method == "POST" and request.POST.get('postType') == 'role':
        user = UserInfo.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        user.roles.set(request.POST.getlist('roles'))

    if request.method == "POST" and request.POST.get('postType') == 'permission':
        role = models.Role.objects.filter(id=rid).first()
        if not role:
            return HttpResponse('角色不存在')
        role.permissions.set(request.POST.getlist('permissions'))

    # 获取所有用户
    user_list = UserInfo.objects.all()
    user_has_roles = UserInfo.objects.filter(id=uid).values('id','roles')
    # print(user_has_roles)    # <QuerySet [{'id': 1, 'roles': 2}, {'id': 1, 'roles': 3}]>
    user_has_roles_dict = {item['roles']:None for item in user_has_roles}
    # {1:None,3:None}   用户的对应角色的id值
    '''
    用户拥有的角色id
    user_has_roles_dict = { 角色id :None}
    '''

    # 获取所有角色
    role_list = models.Role.objects.all()

    if rid:
        role_has_permissions = models.Role.objects.filter(id=rid).values('id','permissions')
    elif uid and not rid:
        user = UserInfo.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        role_has_permissions = user.roles.values('id','permissions')
    else:
        role_has_permissions = []
    # print(role_has_permissions)
    role_has_permissions_dict = {item['permissions']:None for item in role_has_permissions}
    '''
    用户拥有的权限id
    role_has_permissions_dict = { 权限id :None}
    '''
    all_menu_list = []    # 保存最终的数据结构
    queryset = models.Menu.objects.values('id','name')   # 一级菜单数据
    # queryset = [{'id':1,'name':'业务系统','child':[]},{'id':2,'name':'教务系统','child':[]}]
    menu_dict = {}
    '''
    menu_dict ={'1': {'id':1,'name': '业务系统', 'children':[]} ,
                '2': {'id':2,'name': '教务系统', 'children':[]} ,
                None:{'id':None,'name':'其他','children':[]}    # 没有分配菜单的权限
                }
    '''
    # print(menu_dict)
    # print(all_menu_list)
    '''
    all_menu_list = {
        {'id':1,'name': '业务系统', 'children':[]} .
        {'id':2,'name': '教务系统', 'children':[]} .
        {'id':None,'name':'其他','children':[]}
    }
    '''
    for item in queryset:
        item['children'] = []   # 放二级菜单父权限
        menu_dict[item['id']] = item
        all_menu_list.append(item)

    other = {'id':None,'name':'其他','children':[]}
    all_menu_list.append(other)
    menu_dict[None] = other

    # 二级菜单权限数据
    root_permission = models.Permission.objects.filter(menus__isnull=False).values('id','title','menus_id')

    root_permission_dict = {}   # 45
    # print(root_permission,'xxxxx')
    '''
    <QuerySet [
    {'id': 1, 'title': '客户管理', 'menus_id': 1}, {'id': 22, 'title': '跟进记录展示', 'menus_id': 1},
     {'id': 54, 'title': '私户信息展示', 'menus_id': 1}, {'id': 5, 'title': '课程记录展示', 'menus_id': 2}, 
    {'id': 10, 'title': '角色展示', 'menus_id': 3}, {'id': 14, 'title': '菜单展示', 'menus_id': 3}]> xxxxx
    '''

    for per in root_permission:
        per['children'] = []  # 放子权限
        nid = per['id']       # 二级菜单id
        menu_id = per['menus_id']           # 一级菜单id
        root_permission_dict[nid] = per
        menu_dict[menu_id]['children'].append(per)

    # 二级菜单的子权限
    node_permission = models.Permission.objects.filter(menus__isnull=True).values('id','title','parent_id')
    for per in node_permission:
        pid = per['parent_id']
        if not pid:
            menu_dict[None]['children'].append(per)
            continue
        root_permission_dict[pid]['children'].append(per)
        # print(all_menu_list,'oooozzozzo')

    return render(
        request,'distribute_permissions.html',
        {
            'user_list':user_list,
            'role_list':role_list,
            'user_has_roles_dict':user_has_roles_dict,
            'role_has_permissions_dict':role_has_permissions_dict,
            'all_menu_list':all_menu_list,
            'uid':uid,
            'rid':rid
        }
    )
    # 1:18:00