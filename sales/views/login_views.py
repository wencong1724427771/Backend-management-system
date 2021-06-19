from django.shortcuts import render,redirect
from sales import models
from django.http import JsonResponse
from utils.md5_func import md5_function
from django.urls import reverse
from sales.myforms import RegisterForm
# Create your views here.



# 注销登录
def logout(request):
    request.session.flush()   # 清除cookie,删除session
    return redirect('sales:login')

def login(request):
    res_dict = {'status':None,'home':None,'msg':None}
    if request.method == 'GET':
        return render(request, 'login/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        print(username,password)
        user_objs = models.UserInfo.objects.filter(username=username,password=md5_function(password))

        if user_objs:
            # 保存当前用户名
            request.session['account'] = username

            res_dict['status'] = 1
            res_dict['home'] = reverse('sales:home')  # '/home/'
            return JsonResponse(res_dict)
        else:
            res_dict['status'] = 0
            res_dict['msg'] = '用户名或密码错误'
            return JsonResponse(res_dict)


def register(request):
    if request.method=='GET':
        register_obj = RegisterForm()
        return render(request, 'login/register.html', {'register_obj':register_obj})
    else:
        register_obj = RegisterForm(request.POST)
        print(request.POST)
        if register_obj.is_valid():
            print(register_obj.cleaned_data)
            register_obj.cleaned_data.pop('r_password')
            md5_password = md5_function(register_obj.cleaned_data.get('password'))
            register_obj.cleaned_data.update({'password':md5_password})   # ***********
            models.UserInfo.objects.create(
                **register_obj.cleaned_data
            )
            return redirect('sales:login')
        else:
            return render(request, 'login/register.html', {'register_obj':register_obj})