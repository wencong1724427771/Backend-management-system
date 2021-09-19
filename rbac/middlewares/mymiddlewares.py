import re
from django.utils.deprecation import MiddlewareMixin

# 需要先注册中间件才能使用
from django.urls import reverse
from django.shortcuts import redirect,HttpResponse
from rbac import models


class Auth(MiddlewareMixin):
    # 登录认证白名单  通过访问路径来放行
    white_list = [reverse('sales:login'),reverse('sales:register'),'/']

    def process_request(self,request):
        path = request.path    # /sales/editcustomer/2/

        if path not in self.white_list:
            # 登录成功
            status = request.session.get('account')
            if not status:
                return redirect('sales:login')

            # 权限认证
            '''
            [
              {'permissions__url': '/customers/'},
              {'permissions__url': '/mycustomers/'},
              {'permissions__url': '/editcustomer/(\\d+)/'}, 
              {'permissions__url': '/addcustomer/'}
              ]
            '''
            # 权限认证白名单
            permission_white_list = [reverse('sales:home'),'/admin/*',reverse('sales:logout')]   # '.*' 不走权限认证

            # permission_list = request.session.get("permission_list")
            permission_dict = request.session.get("permission_dict")

            # 往request类里面添加变量
            request.pid = None
            bread_crumb = [
                {'url':reverse('sales:home'),'title':'首页'},
                # {'url':'/sales/home/','title':'首页'},
            ]
            request.bread_crumb = bread_crumb

            for white_path in permission_white_list:
                if re.match(white_path,path):
                    break
            else:
                # for i in permission_list:
                for i in permission_dict.values():
                    # print(permission_list)
                    res = r'^%s$'%i["permissions__url"]    # ^/sales/editcustomer/(\\d+)/$
                    # print(res,path)
                    if re.match(res,path):  # 有当前路径的权限,通过
                        # path = /sales/customer/  -> none
                        # /sales/editcustomer/(\\d+)/$  -> 1
                        pid = i.get('permissions__parent_id')    # menu_dict ->second_menu_id
                        if pid:     # 访问二级菜单下的添加删除功能
                            request.pid = pid
                            # 父级二级菜单对象的信息
                            # parent_permission = models.Permission.objects.get(pk=pid)    # 每次访问子权限都要去访问数据库,效率低
                            # print(i)
                            request.bread_crumb.append(
                                {         # KeyError, str(pid)经过json序列化之后,取出来的字典的键变成字符串
                                 'url': permission_dict[str(pid)]['permissions__url'],
                                 'title': permission_dict[str(pid)]['permissions__title']
                                 }
                            )
                            # 子权限的路径信息
                            request.bread_crumb.append(
                                {'url': i.get('permissions__url'), 'title': i.get('permissions__title')}
                            )
                        else:       # 访问二级菜单
                            request.pid = i.get('permissions__pk')
                            request.bread_crumb.append(
                                {'url': i.get('permissions__url'),'title':i.get('permissions__title')}
                            )
                        break
                else:
                    return HttpResponse("你没有该权限")


