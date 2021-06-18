import copy

from django.shortcuts import render,redirect,HttpResponse
from django import forms
from sales import models
from django.http import JsonResponse
from utils.md5_func import md5_function
from django.urls import reverse
from sales import myforms   # 添加实现编辑页面
from utils.page_func import Paging
from django.conf import settings
from django.db.models import Q
from django.views import View
# Create your views here.


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        min_length=3,
        error_messages={
            'max_length':'太长了',
            'min_length':'太短了',
            'required':'不能为空',
        },
        widget=forms.TextInput(attrs={'class':'username','placeholder':'用户名',
                                      'autocomplete':'off'})
    )
    password = forms.CharField(
        max_length=32,
        min_length=4,
        error_messages={
            'max_length': '太长了',
            'min_length': '太短了',
            'required': '不能为空',
        },
        widget=forms.PasswordInput(attrs={'class':'password','placeholder':'输入密码',
                                          'oncontextmenu':'return false','onpaste':'return false'}),
    )
    r_password = forms.CharField(
        max_length=32,
        min_length=4,
        error_messages={
            'max_length': '太长了',
            'min_length': '太短了',
            'required': '不能为空',
        },
        widget=forms.PasswordInput(attrs={'class':'r_password','placeholder':'确认密码',
                                          'oncontextmenu':'return false','onpaste':'return false'}),
    )
    telephone = forms.CharField(
        max_length=11,
        min_length=11,
        error_messages={
            'max_length': '太长了',
            'min_length': '太短了',
            'required': '不能为空',
        },
        widget = forms.TextInput(attrs={'class':'phone_number','placeholder':'输入手机号码',
                                        'autocomplete':'off','id':'number'})
    )
    email = forms.EmailField(
        error_messages={
            'invalid':'必须是邮箱格式',
            'required': '不能为空',
        },
        widget=forms.EmailInput(attrs={'class':'email','placeholder':'输入邮箱地址','oncontextmenu':'return false',
                   'onpaste':'return false'})
    ) # xx@xx

    def clean(self):
        password = self.cleaned_data.get('password')
        r_password = self.cleaned_data.get('r_password')
        if password == r_password:
            return self.cleaned_data
        else:
            self.add_error('r_password','两次密码不一致！')

# 注销登录
def logout(request):
    request.session.flush()   # 清除cookie,删除session
    return redirect('/login/')

def login(request):
    res_dict = {'status':None,'home':None,'msg':None}
    if request.method == 'GET':
        return render(request, 'login/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        print(username,password)
        user_objs = models.UserInfo.objects.filter(username=username,password=md5_function(password))
        print(user_objs,password)
        print(reverse('home'))
        if user_objs:
            # 保存当前用户名
            request.session['account'] = username

            res_dict['status'] = 1
            res_dict['home'] = reverse('home')  # '/home/'
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
            return redirect('login')
        else:
            return render(request, 'login/register.html', {'register_obj':register_obj})


def home(request):
    return render(request,'customer/home.html')


#CBV
class Customers(View):
    def get(self,request):
        # print(request.path)                  # /customers/
        # print(request.get_full_path())       # /customers/?page=3
        # print(request.session.get('account'))  # alex
        path = request.path
        current_page_number = request.GET.get('page')  # 当前页码
        search_field = request.GET.get('search_field')  # 搜索条件
        keyword = request.GET.get('keyword')  # 搜索数据
        recv_data = copy.copy(request.GET)  # 处理 This QueryDict instance is immutable错误

        if keyword:
            q = Q()  # 实例化对象
            # q.connector = 'or'   # 默认是and
            q.children.append([search_field + '__contains', keyword])  # Q('name__contains'='陈')
            # q.children.append(['name','xx'])      #filter(qq='11',name='xx')
            all_customer = models.Customer.objects.filter(q)

        else:
            all_customer = models.Customer.objects.all()

        if path == '/customers/':
            tag = 1
            # 筛选所有的公户信息
            all_customer = all_customer.filter(consultant__isnull=True)
        else:
            tag = 0
            all_customer = all_customer.filter(consultant__username=request.session.get('account'))

        total_count = all_customer.count()  # 客户数据总数

        per_page_num = settings.PER_PAGE_NUM
        page_number_show = settings.PAGE_NUMBER_SHOW

        page_obj = Paging(current_page_number, total_count, per_page_num, page_number_show, recv_data)
        all_customer = all_customer[page_obj.start_data_number:page_obj.end_data_number]
        page_html = page_obj.page_html_func

        return render(request, 'customer/customers.html',
                      {'all_customer': all_customer, 'page_html': page_html, 'keyword': keyword,
                       'search_field': search_field, 'tag': tag})
    def post(self,request):
        action = request.POST.get('action')
        cids = request.POST.getlist('cids')

        customer_list = models.Customer.objects.filter(id__in=cids)

        if hasattr(self,action):
            ret = getattr(self,action)(request,customer_list)
            if ret:
                return ret
            else:
                return redirect(request.path)
        else:
            return HttpResponse('你的方法不对！！')

    def bulk_delete(self,request,customer_list):
        customer_list.delete()
        return redirect(request.path)

    def convert_gs(self,request,customer_list):
        user_obj = models.UserInfo.objects.get(username=request.session.get('account'))
        print(user_obj)
        # user_obj = models.UserInfo.objects.filter(pk=1)   # 'QuerySet' object has no attribute 'id' ***
        # print(user_obj.filter(pk=1).id)
        customer_list.update(consultant_id=user_obj.id)  # -------

    def convert_sg(self,request,customer_list):
        customer_list.update(consultant=None)

def customers(request):
    if request.method == 'GET':
        path = request.path

        current_page_number = request.GET.get('page')  #当前页码

        search_field = request.GET.get('search_field')   #搜索条件
        keyword = request.GET.get('keyword')  #搜索数据


        recv_data = copy.copy(request.GET)  # 处理 This QueryDict instance is immutable错误
        # print(type(recv_data))  #
        # from django.http.request import QueryDict

        # models.Customer.objects.filter(Q(name__contains='陈')|Q(qq_contains='11'))
        if keyword:
            # models.Customer.objects.filter(**{search_field+'__contains':keyword}   #name='陈')

            q = Q()  # 实例化对象
            # q.connector = 'or'   # 默认是and
            q.children.append([search_field+'__contains',keyword])   #Q('name__contains'='陈')
            # q.children.append(['name','xx'])      #filter(qq='11',name='xx')
            all_customer = models.Customer.objects.filter(q)

        else:
            all_customer = models.Customer.objects.all()

        if path == '/customers/':
            tag = 1
            # 筛选所有的公户信息
            all_customer = all_customer.filter(consultant__isnull=True)
        else:
            tag = 0
            # 前登录对象在user_info表里面记录的用户名
            # all_customer = all_customer.filter(consultant__username=当前登录对象在user_info表里面记录的用户名)
            all_customer = all_customer.filter(consultant__username=request.session.get('account'))


        total_count = all_customer.count()  # 客户数据总数

        per_page_num = settings.PER_PAGE_NUM
        page_number_show = settings.PAGE_NUMBER_SHOW

        page_obj = Paging(current_page_number,total_count,per_page_num,page_number_show,recv_data)
        # all_customer=all_customer[page_obj.start_data_number:page_obj.end_data_number]
        all_customer=all_customer[page_obj.start_data_number:page_obj.end_data_number]
        page_html = page_obj.page_html_func

        return render(request,'customer/customers.html',
            {'all_customer':all_customer,'page_html':page_html,'keyword':keyword,'search_field':search_field,'tag':tag})
    # else:
    #     action = request.POST.get('action')
    #     cids = request.POST.getlist('cids')  # 选择的客户  --多选框要使用getlist()
    #     print(action,cids)
    #     if action == 'bulk_delete':
    #         models.Customer.objects.filter(id__in=cids).delete()
    #
    #     elif action == 'convert_gs':
    #         user_obj = models.UserInfo.objects.filter(username=request.session.get('account'))
    #         models.Customer.objects.filter(id__in=cids).update(consultant_id=user_obj.id)





#合并添加删除页面
def addEditCustomer(request,n=None): # n 编辑的是那条用用户
    old_obj = models.Customer.objects.filter(pk=n).first()
    label ='编辑页面' if n else '添加页面'


    if request.method == 'GET':
        book_form_obj = myforms.CustomerModelForm(instance=old_obj)  # 关键字instance
        return render(request, 'customer/editcustomer.html', {'book_form_obj': book_form_obj,'label':label})
    else:
        next_path = request.GET.get('next')   # 查询参数都会放入request.GET里面   -- 会反解url编码的地址
        print(next_path)   # /customers/?search_field=qq
        # http://127.0.0.1:8000/editcustomer/208/?next=/customers/?search_field=qq&keyword=123&page=3
        book_form_obj = myforms.CustomerModelForm(request.POST,instance=old_obj)  # instance=old_obj
        if book_form_obj.is_valid():
            book_form_obj.save()
            return redirect(next_path)    # /customers/?page=3
            # return redirect('customers')    # customers/page=3
        else:
            return render(request, 'customer/editcustomer.html', {'book_form_obj': book_form_obj,'label':label})