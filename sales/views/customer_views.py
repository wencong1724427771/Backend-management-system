import copy

from django.shortcuts import render,redirect,HttpResponse
from sales import models
from django.urls import reverse
from sales import myforms
from utils.page_func import Paging
from django.conf import settings
from django.db.models import Q
from django.views import View
# Create your views here.


def home(request):
    return render(request,'customer/home.html')


#CBV
class Customers(View):
    def get(self,request):
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

        # if path == '/customers/':
        if path == reverse('sales:customers'):
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
        print(action,cids)
        customer_list = models.Customer.objects.filter(id__in=cids)

        if hasattr(self,action):
            ret = getattr(self,action)(request,customer_list)
            print('----',ret,'---',getattr(self,action))
            if ret:
                return ret
            else:
                print(request.path,9999)
                return redirect(request.path)
        else:
            return HttpResponse('你的方法不对！！')

    def bulk_delete(self,request,customer_list):
        customer_list.delete()

    def convert_gs(self,request,customer_list):
        user_obj = models.UserInfo.objects.get(username=request.session.get('account'))
        # user_obj = models.UserInfo.objects.filter(pk=1)   # 'QuerySet' object has no attribute 'id' ***
        # print(user_obj.filter(pk=1).id)
        customer_list.update(consultant_id=user_obj.id)  # -------

    def convert_sg(self,request,customer_list):
        customer_list.update(consultant=None)

    def blank(*args,**kwargs):
        pass



#合并添加删除页面
def addEditCustomer(request,n=None): # n 编辑的是那条用用户
    old_obj = models.Customer.objects.filter(pk=n).first()
    label ='编辑页面' if n else '添加页面'


    if request.method == 'GET':
        book_form_obj = myforms.CustomerModelForm(instance=old_obj)  # 关键字instance
        return render(request, 'customer/editcustomer.html', {'book_form_obj': book_form_obj,'label':label})
    else:
        next_path = request.GET.get('next')   # 查询参数都会放入request.GET里面   -- 会反解url编码的地址
        book_form_obj = myforms.CustomerModelForm(request.POST,instance=old_obj)  # instance=old_obj
        if book_form_obj.is_valid():
            book_form_obj.save()
            return redirect(next_path)    # /customers/?page=3
            # return redirect('customers')    # customers/page=3
        else:
            return render(request, 'customer/editcustomer.html', {'book_form_obj': book_form_obj,'label':label})


def test(request):
    return render(request,'test.html')