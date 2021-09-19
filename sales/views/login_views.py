# -*- coding = utf-8 -*-
# @Time: 2021/8/6 10:15
# @Author: Bon
# @File: login_views.py
# @Software: PyCharm
from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse
from rbac.utils.permission_injection import init_permission


from sales import models
from sales.models import UserInfo
from rbac import models
from utils import md5_func
from sales.myForms import RegisterForm


# 注销登录
def logout(request):
    request.session.flush()   # 清除cookie,删除session
    return redirect('sales:login')

# 登录
def login(request):
    res_dict = {'status':None,'home':None,'msg':None}
    if request.method == 'GET':
        return render(request, 'login/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_objs = UserInfo.objects.filter(username=username,password=md5_func.mkMd5(password))

        if user_objs:
            user_obj = user_objs.first()   # 拿到对象
            # 保存当前用户名,登录认证表示
            request.session['account'] = username

            # 把用户权限等相关信息注入到session
            init_permission(request,user_obj)
            # init_permission(request,user_objs.first())

            return redirect('sales:home')


            # res_dict['status'] = 1         # type=submit  前端代码改了，没有用ajax
            # res_dict['home'] = reverse('sales:home')  # '/sales/home/'
            # return JsonResponse(res_dict)
        else:
            res_dict['status'] = 0
            res_dict['msg'] = '用户名或密码错误'
            return JsonResponse(res_dict)

# 注册
def register(request):
    if request.method == 'GET':
        register_obj =RegisterForm()

        context = {
            'register_obj':register_obj
        }
        return render(request, 'Login/register.html',context=context)
    if request.method == 'POST':
        register_obj = RegisterForm(request.POST)    # <class 'django.http.request.QueryDict'>
        if register_obj.is_valid():
            # print(register_obj.cleaned_data['username'])
            # {'username': '初学者', 'password': '123456', 'r_password': '123456', 'telephone': '18370029122', 'email': '1724427771@qq.com'} <class 'dict'>
            password = register_obj.cleaned_data.pop('r_password')   # 数据清洗
            md5_pwd = md5_func.mkMd5(password)
            data = register_obj.cleaned_data
            data.update({'password': md5_pwd})
            # 保存数据
            models.UserInfo.objects.create(
                **data
            )
            return redirect('sales:login')   # 重定向
        else:
            context = {
                'register_obj': register_obj
            }
            return render(request,'Login/register.html',context=context)