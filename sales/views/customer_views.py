# -*- coding = utf-8 -*-
# @Time: 2021/8/6 10:16
# @Author: Bon
# @File: customer_views.py
# @Software: PyCharm
import copy

from django.shortcuts import render,redirect,reverse,HttpResponse
from django.conf import settings
from django.db.models import Q
from django.views import View

from sales import models
from utils.page_func import Paging
from sales.myForms import CustomerModelForm,ConsultRecordModelForm,EnrollmentModelForm,CourseRecordModelForm


# 首页
def home(request):
    return render(request,'starter.html')


class Customers(View):
    def get(self,request):
        # print(type(request.get_full_path()))   # <class 'str'>
        recv_data = copy.copy(request.GET)
        # print(request.GET.urlencode())
        # print('xxx')
        current_page_number = request.GET.get('page')  # 当前页码 & 开始取第几条数据的位置
        search_field = request.GET.get('search_field')  # 搜索条件
        keyword = request.GET.get('keyword')  # 关键字  xx__contains
        # 先根据路径过滤数据库查询对象
        if request.path == reverse('sales:mycustomers'):
            tag = 1
            all_customers = models.Customer.objects.all().filter(consultant__username=request.session.get('account'))
        else:
            tag = 0
            all_customers = models.Customer.objects.all().filter(consultant__isnull=True)
        if keyword:
            q = Q()  # 实例化q对象
            # q.connector = 'or' # 默认是and
            q.children.append([search_field, keyword])  # Q(name__contains='xx')
            # q.children.append([search_field1, keyword1])  # 可以完成多条件
            all_customers = all_customers.filter(q)
        else:
            all_customers = all_customers.all()

        total_count = all_customers.count()  # 总数据量
        per_page_num = settings.PER_PAGE_COUNT  # 10
        page_number_show = settings.PAGE_NUMBER_SHOW  # 7

        page_obj = Paging(current_page_number, total_count, per_page_num, page_number_show, recv_data)
        page_html = page_obj.page_html_func

        all_customers = all_customers[page_obj.start_data_number:page_obj.end_data_number]

        context = {
            "all_customers": all_customers,
            "page_html": page_html,
            "search_field": search_field,
            "keyword": keyword,  # 保存搜索条件
            "tag": tag  # 第二种方法判断公户还是私户
            # "page_html":mark_safe(page_html)
        }
        return render(request, 'customer/customers.html', context=context)

    def post(self,request):
        action = request.POST.get('action')
        print(action,type(action))    # bulk_delete <class 'str'>
        cids = request.POST.getlist('cids')  # 多选框取值
        print(cids,type(cids))

        if hasattr(self,action):
            ret = getattr(self,action)(request,cids)
            if ret:
                return ret
            else:
                return redirect(request.path)
        else:
            return HttpResponse('你访问的路径不存在!')

    # blank '------'
    def blank(self,request,*args,**kwargs):
        return redirect(request.path)

    # 批量删除
    def bulk_delete(self,request,cids):
        models.Customer.objects.filter(id__in=cids).delete()
        return redirect(request.path)

    # 公转私
    def reverse_gs(self,request,cids):
        from django.db import transaction
        import time
        with transaction.atomic():
            customer_list_obj = models.Customer.objects.select_for_update().filter(id__in=cids,consultant__isnull=True)
        if customer_list_obj.count() != len(cids):
            return HttpResponse('你太慢了...')
        user_obj = models.UserInfo.objects.get(username=request.session.get('account'))
        customer_list_obj.update(consultant_id=user_obj.id)

    # 私转公
    def reverse_sg(self, request, cids):
        customer_list_obj = models.Customer.objects.filter(id__in=cids)
        customer_list_obj.update(consultant_id=None)


def addEditCustomer(request,n=None):
    old_obj = models.Customer.objects.filter(pk=n).first()
    label  = '编辑页面' if n else '添加页面'

    if request.method == 'GET':
        model_form_obj = CustomerModelForm(instance=old_obj)
        return render(request, 'customer/editcustomer.html', {'form_obj': model_form_obj,'label':label})
    else:
        # a = request.GET['next']
        # print(a,type(a),'xxx')     # /customers/?page=2 <class 'str'> xxx   # 会自动解析encode编码
        next_path = request.GET.get('next')
        # print(next_path,'000')     # /customers/?search_field=name__contains&keyword=xm2&page=2  000


        model_form_obj = CustomerModelForm(request.POST,instance=old_obj)
        if model_form_obj.is_valid():
            model_form_obj.save()
            return redirect(next_path)
        else:
            return render(request, 'customer/editcustomer.html', {'form_obj': model_form_obj,'label':label})

# 跟进记录
class ConsultRecord(View):
    def get(self, request):
        recv_data = copy.copy(request.GET)

        current_page_number = request.GET.get('page')  # 当前页码 & 开始取第几条数据的位置
        search_field = request.GET.get('search_field')  # 搜索条件
        keyword = request.GET.get('keyword')  # 关键字  xx__contains

        all_records = models.ConsultRecord.objects.all()
        if keyword:
            q = Q()  # 实例化q对象
            # q.connector = 'or' # 默认是and
            q.children.append([search_field, keyword])  # Q(name__contains='xx')
            # q.children.append([search_field1, keyword1])  # 可以完成多条件
            all_records = all_records.filter(q)
        else:
            all_records = all_records.all()

        total_count = all_records.count()  # 总数据量
        per_page_num = settings.PER_PAGE_COUNT  # 10
        page_number_show = settings.PAGE_NUMBER_SHOW  # 7

        page_obj = Paging(current_page_number, total_count, per_page_num, page_number_show, recv_data)
        page_html = page_obj.page_html_func

        all_records = all_records[page_obj.start_data_number:page_obj.end_data_number]

        context = {
            "all_records": all_records,
            "page_html": page_html,
            "search_field": search_field,
            "keyword": keyword,  # 保存搜索条件

        }
        return render(request, 'consultrecords/consultrecords.html', context=context)

    def post(self, request):
        action = request.POST.get('action')
        cids = request.POST.getlist('cids')  # 多选框取值


        if hasattr(self, action):
            ret = getattr(self, action)(request,cids)
            if ret:
                return ret
            else:
                return redirect(request.path)
        else:
            return HttpResponse('你访问的路径不存在!')

    # blank '------'
    def blank(self, request, *args, **kwargs):
        return redirect(request.path)

    # 批量删除
    def bulk_delete(self, request,cids):
        all_records_obj = models.ConsultRecord.objects.filter(id__in=cids)
        all_records_obj.delete()
        return redirect(request.path)


# 添加编辑跟进记录
def addEditConsultRecord(request,n=None):
    old_obj = models.ConsultRecord.objects.filter(pk=n).first()
    label  = '编辑跟进记录' if n else '添加跟进记录'

    if request.method == 'GET':
        model_form_obj = ConsultRecordModelForm(instance=old_obj)
        return render(request, 'consultrecords/addConsultRecord.html', {'form_obj': model_form_obj,'label':label})
    else:
        next_path = request.GET.get('next')
        print(next_path,'xxx')

        model_form_obj = ConsultRecordModelForm(request.POST,instance=old_obj)
        if model_form_obj.is_valid():
            model_form_obj.save()
            return redirect('sales:consultrecords')
            # return redirect(next_path)
        else:
            return render(request, 'consultrecords/editConsultRecord.html', {'form_obj': model_form_obj,'label':label})



# 报名记录
class Enrollment(View):
    def get(self, request):
        recv_data = copy.copy(request.GET)

        current_page_number = request.GET.get('page')  # 当前页码 & 开始取第几条数据的位置
        search_field = request.GET.get('search_field')  # 搜索条件
        keyword = request.GET.get('keyword')  # 关键字  xx__contains
        # print(search_field,keyword)    # search_field=customer__name__contains&keyword=xm&page=1 xxx
        all_enrollments = models.Enrollment.objects.all()
        if keyword:
            q = Q()  # 实例化q对象
            # q.connector = 'or' # 默认是and
            q.children.append([search_field, keyword])  # Q(name__contains='xx')
            # q.children.append([search_field1, keyword1])  # 可以完成多条件
            all_enrollments = all_enrollments.filter(q)
        else:
            all_enrollments = all_enrollments.all()

        total_count = all_enrollments.count()  # 总数据量
        per_page_num = settings.PER_PAGE_COUNT  # 10
        page_number_show = settings.PAGE_NUMBER_SHOW  # 7

        page_obj = Paging(current_page_number, total_count, per_page_num, page_number_show, recv_data)
        page_html = page_obj.page_html_func

        all_enrollments = all_enrollments[page_obj.start_data_number:page_obj.end_data_number]

        context = {
            "all_enrollments": all_enrollments,
            "page_html": page_html,
            "search_field": search_field,
            "keyword": keyword,  # 保存搜索条件

        }
        return render(request, 'enrollment/enrollment.html', context=context)

    def post(self, request):
        action = request.POST.get('action')
        cids = request.POST.getlist('cids')  # 多选框取值


        if hasattr(self, action):
            ret = getattr(self, action)(request,cids)
            if ret:
                return ret
            else:
                return redirect(request.path)
        else:
            return HttpResponse('你访问的路径不存在!')

    # blank '------'
    def blank(self, request, *args, **kwargs):
        return redirect(request.path)

    # 批量删除
    def bulk_delete(self, request,cids):
        all_records_obj = models.Enrollment.objects.filter(id__in=cids)
        all_records_obj.delete()
        return redirect(request.path)


# 添加编辑报名记录
def addEditEnrollment(request,n=None):
    old_obj = models.Enrollment.objects.filter(pk=n).first()
    label  = '编辑报名记录' if n else '添加报名记录'

    if request.method == 'GET':
        model_form_obj = EnrollmentModelForm(instance=old_obj)
        return render(request, 'enrollment/addenrollment.html', {'model_form_obj': model_form_obj,'label':label})
    else:
        next_path = request.GET.get('next')
        # print(next_path,'xxxxxxxxxxxxxxxx')    # /sales/enrollments/ xxxxxxxxxxxxxxxx
        model_form_obj = EnrollmentModelForm(request.POST,instance=old_obj)
        if model_form_obj.is_valid():
            model_form_obj.save()
            # return redirect('sales:enrollments')
            return redirect(next_path)
        else:
            return render(request, 'enrollment/editenrollment.html', {'form_obj': model_form_obj,'label':label})


# 课程记录
class CourseRecord(View):
    def get(self, request):
        current_page_number = request.GET.get('page')  # 当前页码
        search_field = request.GET.get('search_field')  # 搜索条件
        keyword = request.GET.get('keyword')  # 搜索数据
        recv_data = copy.copy(request.GET)  # 处理 This QueryDict instance is immutable错误

        # 查询逻辑
        if keyword:
            q = Q()  # 实例化对象
            q.children.append([search_field + '__contains', keyword])  # Q('name__contains'='陈')
            # q.children.append(['name','xx'])      #filter(qq='11',name='xx')
            all_course_record = models.CourseRecord.objects.filter(q)

        else:
            all_course_record = models.CourseRecord.objects.all()

        total_count = all_course_record.count()  # 客户数据总数

        per_page_num = settings.PER_PAGE_COUNT
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
        course_form_obj = CourseRecordModelForm(instance=obj)
        return render(request,'course_record/addcourse_record.html',{'course_form_obj':course_form_obj,'label':label})

    if request.method == 'POST':
        next_path = request.GET.get('next')
        course_form_obj = CourseRecordModelForm(request.POST,instance=obj)
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
        # print(course_id)
        formset_obj = modelformset_factory(model=models.StudyRecord,form=StudyRecordModelForm,extra=0)
        # formset = formset_obj()
        formset = formset_obj(queryset=models.StudyRecord.objects.filter(course_record_id=course_id))

        # all_study_records = models.StudyRecord.objects.filter(course_record_id=course_id)
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