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

        # 查询逻辑
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
        print(action, cids)


        if hasattr(self,action):
            ret = getattr(self,action)(request,cids)
            print('----',ret,'---',getattr(self,action))
            if ret:
                return ret
            else:
                return redirect(request.path)
        else:
            return HttpResponse('你的方法不对！！')

    def bulk_delete(self,request,cids):
        customer_list = models.Customer.objects.filter(id__in=cids, consultant__isnull=True)
        customer_list.delete()
        return redirect(request.path)

    def convert_gs(self,request,cids):

        from django.db import transaction
        with transaction.atomic():
            customer_list = models.Customer.objects.select_for_update().filter(id__in=cids, consultant__isnull=True)
        if customer_list.count() != len(cids):
            return  HttpResponse('宝,ni手速太慢了')

        user_obj = models.UserInfo.objects.get(username=request.session.get('account'))
        customer_list.update(consultant_id=user_obj.id)


    def convert_sg(self,request,cids):
        customer_list = models.Customer.objects.filter(id__in=cids)
        customer_list.update(consultant=None)


    def blank(*args,**kwargs):
        pass



#合并添加删除客户信息页面
def addEditCustomer(request,n=None): # n 编辑的是那条用用户
    old_obj = models.Customer.objects.filter(pk=n).first()
    label ='编辑页面' if n else '添加页面'


    if request.method == 'GET':
        customerInfo_form_obj = myforms.CustomerModelForm(instance=old_obj)  # 关键字instance
        return render(request, 'customer/editcustomer.html', {'customerInfo_form_obj': customerInfo_form_obj,'label':label})
    else:
        next_path = request.GET.get('next')   # 查询参数都会放入request.GET里面   -- 会反解url编码的地址
        # print(next_path,'2222222')      # /sales/customers/ 2222222
        customerInfo_form_obj = myforms.CustomerModelForm(request.POST,instance=old_obj)  # instance=old_obj
        if customerInfo_form_obj.is_valid():
            customerInfo_form_obj.save()
            return redirect(next_path)    # /customers/?page=3
            # return redirect('customers')    # customers/page=3
        else:
            return render(request, 'customer/editcustomer.html', {'customerInfo_form_obj': customerInfo_form_obj,'label':label})



def test(request):
    return render(request,'test.html')



class ConsultRecord(View):
    def get(self, request):

        current_page_number = request.GET.get('page')  # 当前页码
        search_field = request.GET.get('search_field')  # 搜索条件
        keyword = request.GET.get('keyword')  # 搜索数据
        recv_data = copy.copy(request.GET)  # 处理 This QueryDict instance is immutable错误
        # 单个客户的id值
        customer_id = request.GET.get('customer_id')

        # 查询逻辑
        if keyword:
            q = Q()  # 实例化对象
            q.children.append([search_field, keyword])  # Q('name__contains'='陈')
            # all_records = models.ConsultRecord.objects.filter(customer__name__contains='xxx')
            all_records = models.ConsultRecord.objects.filter(q)
        else:
            all_records = models.ConsultRecord.objects.all()

        # delete_status=False   让跟进者看不到，实际上没有删除
        # 筛选登陆证自己的记录
        all_records = all_records.filter(consultant__username=request.session.get('account'),delete_status=False)

        if customer_id:
            all_records=all_records.filter(customer_id=customer_id)

        total_count = all_records.count()  # 客户数据总数
        per_page_num = settings.PER_PAGE_NUM
        page_number_show = settings.PAGE_NUMBER_SHOW

        page_obj = Paging(current_page_number, total_count, per_page_num, page_number_show, recv_data)
        all_records = all_records[page_obj.start_data_number:page_obj.end_data_number]
        page_html = page_obj.page_html_func

        return render(request, 'consult_record/consult_record.html',
                      {'all_records': all_records, 'page_html': page_html, 'keyword': keyword,
                       'search_field': search_field})

    def post(self, request):
        action = request.POST.get('action')
        cids = request.POST.getlist('cids')
        # print(action, cids)
        consult_record_list = models.ConsultRecord.objects.filter(id__in=cids)

        if hasattr(self, action):
            ret = getattr(self, action)(request, consult_record_list)
            if ret:
                return ret
            else:
                return redirect(request.path)
        else:
            return HttpResponse('你的方法不对！！')

    def bulk_delete(self, request, consult_record_list):
        consult_record_list.update(delete_status =True)
        return redirect(request.path)

    def blank(*args, **kwargs):
        pass



# 添加和编辑根据记录
def addEditConsultRecord(request,n=None):
    old_obj = models.ConsultRecord.objects.filter(pk=n).first()
    label ='编辑页面' if n else '添加页面'


    if request.method == 'GET':
        # next_path = request.get_full_path()
        # print(next_path, '----------------')    # /sales/consultrecords/
        record_from_obj = myforms.ConsultRecordModelForm(request,instance=old_obj)  # 关键字instance
        return render(request, 'consult_record/addconsult_record.html', {'record_from_obj': record_from_obj, 'label':label})
    else:
        next_path = request.GET.get('next')   # 查询参数都会放入request.GET里面   -- 会反解url编码的地址
        # print(next_path,'----------------') # http://127.0.0.1:8000/editconsult_record/?next=/sales/consultrecords/
        record_from_obj = myforms.ConsultRecordModelForm(request,request.POST,instance=old_obj)  # instance=old_obj
        if record_from_obj.is_valid():
            record_from_obj.save()
            return redirect(next_path)
        else:
            return render(request, 'consult_record/editconsult_record.html', {'record_from_obj': record_from_obj, 'label':label})


# 报名信息
# def enrollment(request):
#
#     if request.method == 'GET':
#         enrollments_obj = models.Enrollment.objects.all()
#         return render(request,'enrollment_info/enrollment.html',{'enrollments_obj':enrollments_obj})
#     if request.method == 'POST':




#CBV 报名信息
class Enrollment(View):
    def get(self,request):
        current_page_number = request.GET.get('page')       # 当前页码
        recv_data = copy.copy(request.GET)
        enrollments_obj = models.Enrollment.objects.all()   # 报名表中的所有信息
        search_field = request.GET.get('search_field')      # 获取前端传来的查询方法
        print(search_field)
        keyword = request.GET.get('keyword')                # 获取前端传来的查询条件
        # print(search_field,keyword)
        if search_field == 'stu_name':
            enrollments_obj = models.Enrollment.objects.filter(customer__name__contains=keyword)
        if search_field == 'stu_class':
            enrollments_obj = models.Enrollment.objects.filter(enrolment_class__course__contains=keyword)


        total_count = models.Enrollment.objects.all().count()
        per_page_num = settings.PER_PAGE_NUM
        page_number_show = settings.PAGE_NUMBER_SHOW

        page_obj = Paging(current_page_number, total_count, per_page_num, page_number_show, recv_data)
        enrollments_obj = enrollments_obj[page_obj.start_data_number:page_obj.end_data_number]
        page_html = page_obj.page_html_func

        return render(request, 'enrollment_info/enrollment.html',
                      {'enrollments_obj': enrollments_obj,'page_html':page_html,'search_field':search_field,'keyword':keyword})

        # return render(request, 'consult_record/consult_record.html',
        #               {'all_records': all_records, 'page_html': page_html, 'keyword': keyword,
        #                'search_field': search_field})

    def post(self, request):
        action = request.POST.get('action')
        cids = request.POST.getlist('cids')
        print(action, cids)

        if hasattr(self, action):
            ret = getattr(self, action)(cids)
            print('----', ret, '---', getattr(self, action))
            if ret:
                return ret
            else:
                return redirect(request.path)
        else:
            return HttpResponse('你的方法不对！！')

    def bulk_delete(self,cids):
        enrollments_obj = models.Enrollment.objects.filter(id__in=cids)
        enrollments_obj.delete()

    def blank(*args,**kwargs):
        pass






# 添加和编辑根据记录
def addEditEnrollment(request,n=None):
    old_obj = models.Enrollment.objects.filter(pk=n).first()
    # label = '编辑页面' if n else '添加页面'
    if request.method == 'GET':

        erollment_from_obj = myforms.EnrollmentModelForm(request,instance=old_obj)  # 关键字instance
        return render(request, 'enrollment_info/editerollment.html', {'erollment_from_obj': erollment_from_obj})
    else:
        erollment_from_obj = myforms.EnrollmentModelForm(request,request.POST,instance=old_obj)
        if erollment_from_obj.is_valid():
            erollment_from_obj.save()
            return redirect('sales:enrollment')
        else:
            return render(request, 'enrollment_info/editerollment.html', {'erollment_from_obj': erollment_from_obj})




# 课程记录
class CourseRecord(View):
    def get(self, request):
        current_page_number = request.GET.get('page')  # 当前页码
        search_field = request.GET.get('search_field')  # 搜索条件
        keyword = request.GET.get('keyword')  # 搜索数据
        recv_data = copy.copy(request.GET)  # 处理 This QueryDict instance is immutable错误
        # print(recv_data,'--------')  <QueryDict: {'search_field': ['course_title'], 'keyword': ['django'], 'page': ['1']}> --------
        # all_course_record = models.CourseRecord.objects.all()

        # 查询逻辑
        if keyword:
            q = Q()  # 实例化对象
            q.children.append([search_field + '__contains', keyword])  # Q('name__contains'='陈')
            # q.children.append(['name','xx'])      #filter(qq='11',name='xx')
            all_course_record = models.CourseRecord.objects.filter(q)

        else:
            all_course_record = models.CourseRecord.objects.all()


        total_count = all_course_record.count()  # 客户数据总数

        per_page_num = settings.PER_PAGE_NUM
        page_number_show = settings.PAGE_NUMBER_SHOW

        page_obj = Paging(current_page_number, total_count, per_page_num, page_number_show, recv_data)
        all_course_record = all_course_record[page_obj.start_data_number:page_obj.end_data_number]
        page_html = page_obj.page_html_func

        return render(request, 'course_record/course_record.html',
                      {'all_course_record': all_course_record, 'page_html': page_html, 'keyword': keyword,
                       'search_field': search_field})


    def post(self,request):
        action = request.POST.get('action')
        cids = request.POST.getlist('cids')
        # print(action, cids)

        if hasattr(self, action):
            getattr(self, action)(request, cids)
            return redirect('sales:courserecord')
        else:
            return HttpResponse('你的方法不对！！')

    def bulk_delete(self, request, cids):
        customer_list = models.CourseRecord.objects.filter(id__in=cids)
        customer_list.delete()
        # return redirect(request.path)

    def bulk_create_studyrecords(self, request, cids):
        course_record_list = models.CourseRecord.objects.filter(pk__in=cids)
        for course_record in course_record_list:
            student_objs = course_record.re_class.customer_set.all().exclude(status='unregistered')
            # for student in student_objs:
            #     models.StudyRecord.objects.create(
            #         course_record = course_record,
            #         student = student,
            #     )
            student_list = []
            for student in student_objs:
                obj = models.StudyRecord(
                    course_record = course_record,
                    student = student,
                )
                student_list.append(obj)
            models.StudyRecord.objects.bulk_create(student_list)


    def blank(*args, **kwargs):
        pass



def addEditCourseRecord(request,n=None):
    label = '编辑页面' if n else '添加页面'
    # obj = models.CourseRecord.objects.filter(pk=n)   # 'QuerySet' object has no attribute '_meta'
    obj = models.CourseRecord.objects.filter(pk=n).first()
    if request.method == 'GET':
        course_form_obj = myforms.CourseRecordModelForm(instance=obj)
        return render(request,'course_record/addcourse_record.html',{'course_form_obj':course_form_obj,'label':label})

    if request.method == 'POST':
        next_path = request.GET.get('next')
        course_form_obj = myforms.CourseRecordModelForm(request.POST,instance=obj)
        if course_form_obj.is_valid():
            course_form_obj.save()
            return redirect(next_path)
        else:
            return render(request, 'course_record/addcourse_record.html', {'course_form_obj': course_form_obj})


from django.forms.models import modelformset_factory
from django import forms
class StudyRecordModelForm(forms.ModelForm):
    class Meta:
        models = models.StudyRecord
        fields = '__all__'




# 学习记录展示
class StudyRecord(View):
    def get(self,request,course_id):
        formset_obj = modelformset_factory(model=models.StudyRecord,form=StudyRecordModelForm,extra=0)
        # formset = formset_obj()
        formset = formset_obj(queryset=models.StudyRecord.objects.filter(course_record_id=course_id))

        all_study_records = models.StudyRecord.objects.filter(course_record_id=course_id)
        return render(request,'course_record/study_record.html',
                      {'formset':formset})

    def post(self,request,course_id):
        formset_obj = modelformset_factory(model=models.StudyRecord, form=StudyRecordModelForm, extra=0)
        formset = formset_obj(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(request.path)
        else:
            return render(request,'course_record/study_record.html',
                          {'formset': formset})