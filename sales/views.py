from django.shortcuts import render,redirect,HttpResponse
from django import forms
from sales import models
from django.http import JsonResponse
from utils.md5_func import md5_function
from django.urls import reverse
from sales import myforms
from utils.page_func import Paging
from django.conf import settings
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





def customers(request):
    current_page_number = request.GET.get('page')  #当前页码

    search_field = request.GET.get('search_field')   #搜索条件
    keyword = request.GET.get('keyword')  #搜索数据

    # http: // 127.0.0.1: 8000 / customers /?search_field = qq & keyword = 123  #
    # print(request.GET)  # <QueryDict: {'search_field': ['qq'], 'keyword': ['172']}>
    # print(request.GET.urlencode())  # page=2&search_field=qq&keyword=123
    import copy
    recv_data = copy.copy(request.GET)  # 处理 This QueryDict instance is immutable错误
    print(type(recv_data))  #
    # from django.http.request import QueryDict


    from django.db.models import Q

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




    total_count = all_customer.count()  # 客户数据总数

    per_page_num = settings.PER_PAGE_NUM
    page_number_show = settings.PAGE_NUMBER_SHOW

    page_obj = Paging(current_page_number,total_count,per_page_num,page_number_show,recv_data)
    all_customer=all_customer[page_obj.start_data_number:page_obj.end_data_number]
    page_html = page_obj.page_html_func

    return render(request,'customer/customers.html',
        {'all_customer':all_customer,'page_html':page_html})





#合并添加删除页面
def addEditCustomer(request,n=None): # n 编辑的是那条用用户
    old_obj = models.Customer.objects.filter(pk=n).first()
    label ='编辑页面' if n else '添加页面'

    if request.method == 'GET':
        book_form_obj = myforms.CustomerModelForm(instance=old_obj)  # 关键字instance
        return render(request, 'customer/editcustomer.html', {'book_form_obj': book_form_obj,'label':label})
    else:
        book_form_obj = myforms.CustomerModelForm(request.POST,instance=old_obj)  # instance=old_obj
        if book_form_obj.is_valid():
            book_form_obj.save()
            return redirect('/customers/')
        else:
            return render(request, 'customer/editcustomer.html', {'book_form_obj': book_form_obj,'label':label})