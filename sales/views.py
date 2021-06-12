from django.shortcuts import render,redirect,HttpResponse
from django import forms
from sales import models
from django.http import JsonResponse
from utils.md5_func import md5_function
from django.urls import reverse
from sales import myforms
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
                                      'autocomplete':'off'})#默认属性name:username'
        # < input type = "text" name = "username" class ="username" placeholder="用户名" autocomplete="off" >
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
            print(222, '------------')
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
            print(333)
            return render(request, 'login/register.html', {'register_obj':register_obj})


def home(request):
    return render(request,'customer/home.html')

def customers(request):
    all_customer=models.Customer.objects.all()
    return render(request,'customer/customers.html',{'all_customer':all_customer})



def addcustomer(request):
    if request.method == 'GET':
        book_form_obj = myforms.CustomerModelForm()
        return render(request,'customer/addcustomer.html',{'book_form_obj':book_form_obj})
    else:
        book_form_obj = myforms.CustomerModelForm(request.POST)

        if book_form_obj.is_valid():
            book_form_obj.save()
            return redirect('customers')
        else:
            return render(request, 'customer/addcustomer.html', {'book_form_obj': book_form_obj})


# 编辑用户
def editcustomer(request,n): # n 编辑的是那条用用户
    old_obj = models.Customer.objects.filter(pk=n).first()
    if request.method == 'GET':
        book_form_obj = myforms.CustomerModelForm(instance=old_obj)  # 关键字instance
        return render(request, 'customer/editcustomer.html', {'book_form_obj': book_form_obj})
    else:
        book_form_obj = myforms.CustomerModelForm(request.POST,instance=old_obj)  # instance=old_obj
        if book_form_obj.is_valid():
            book_form_obj.save()
            return redirect('/customers/')
        else:
            return render(request, 'customer/editcustomer.html', {'book_form_obj': book_form_obj})

'''
# def edit_book(request, pk):
#     book_obj = models.Book.objects.filter(id=pk).first()
#     if request.method == "POST":
#         #修改数据时，直接可以将用户数据包request.POST传进去，
#         #再传一个要修改的对象的示例，ModelForm就可以自动完成修改数据了。
#         form_obj = forms.BookModelForm(request.POST, instance=book_obj)
#         if form_obj.is_valid():  // 数据校验
#             form_obj.save()   // 直接保存
#         return redirect("/book_list/")
#     #form_obj通过instance设置初始化的值，例如，图书管理系统中的编辑书籍功能，
#     #点击编辑后跳转到编辑书籍页面，跳转后需要用要编辑的书籍信息填充页面对应信息。
#     #不同于Form组件的是，ModelForm直接就可以传实例化的对象，而不需要将对象转化成字典的形式传。
#     form_obj = forms.BookModelForm(instance=book_obj)  
#     return render(request, "v2/edit_book.html", locals())
'''
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