from django.shortcuts import render,redirect,HttpResponse
from django import forms
from sales import models
from django.http import JsonResponse
from utils.md5_func import md5_function
from django.urls import reverse
from sales import myforms
from django.utils.safestring import mark_safe  #{{ page_html|safe }}
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
            return render(request, 'login/register.html', {'register_obj':register_obj})


def home(request):
    return render(request,'customer/home.html')


def customers(request):
    current_page_number = request.GET.get('page')  #当前页码
    try:    # 防止恶意输入错误代码
        current_page_number = abs(int(current_page_number))
    except Exception:
        current_page_number = 1

    per_page_num = 10  # 每页显示多少数据
    page_number_show = 7  # 总共显示的页码数量
    half_number = page_number_show // 2

    all_customer = models.Customer.objects.all()[0:200]   # 当前数据库中所有客户数据
    total_count = all_customer.count()  # 客户数据总数
    a, b = divmod(total_count, per_page_num)  # 商和余数
    if b:  # 如果余数不为0，页码总数为商加一
        total_page_count = a + 1
    else:
        total_page_count = a


    #如果当前页码小于等于0时，默认显示第一页
    if current_page_number<=0:
        current_page_number = 1

    if current_page_number >= total_page_count:
        current_page_number = total_page_count


    star_page_number = current_page_number -half_number
    end_page_number = current_page_number + half_number + 1 # range故首不顾尾


    if star_page_number<1:
        star_page_number = 1
        end_page_number = page_number_show + 1

    if end_page_number >= total_page_count:
        star_page_number = total_page_count - page_number_show+1
        end_page_number = total_page_count+1

    # 如果总页数小于需要展示的页数
    if total_page_count < page_number_show:
        star_page_number = 1
        end_page_number = total_page_count+1

    page_number_range = range(star_page_number,end_page_number)  #<class 'range'>

    all_customer=all_customer[(current_page_number-1)*per_page_num:current_page_number*per_page_num] #[0:10]、[10:20]

   # 页面数据
    page_html = ''
    for i in page_number_range:  # range(0:10)
        if i==current_page_number:   # 为当前页添加颜色

            page_html += f'<li class="active"><a href = "?page={i}" > {i} </a></li>'
        else:
            page_html += f'<li><a href = "?page={i}" > {i} </a></li>'
    #前一页
    previous_page = f'''
            <li>
               <a href="?page={current_page_number - 1}" aria-label="Previous">
                 <span aria-hidden="true">&laquo;</span>
               </a>
            </li>
        '''
    #后一页
    next_page = f'''
            <li>
                <a href="?page={current_page_number + 1}" aria-label="Next">
                 <span aria-hidden="true">&raquo;</span>
                </a>
            </li>
        '''
    first_page = f'''
        <li>
           <a href="?page={1}" aria-label="Previous">
             <span aria-hidden="true">首页</span>
           </a>
        </li>
    '''
    last_page = f'''
        <li>
           <a href="?page={total_page_count}" aria-label="Previous">
             <span aria-hidden="true">尾页</span>
           </a>
        </li>
    '''

    page_html = f'''
    <nav aria-label="Page navigation">
        <ul class="pagination">
            {first_page}
            {previous_page}
            {page_html}
            {next_page}
            {last_page}
        </ul>
    </nav>
    '''


    return render(request,'customer/customers.html',
        {'all_customer':all_customer,'page_html':mark_safe(page_html)})





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