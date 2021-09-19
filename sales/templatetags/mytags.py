# -*- coding = utf-8 -*-
# @Time: 2021/8/5 14:29
# @Author: Bon
# @File: mytags.py
# @Software: PyCharm
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def show_info(request):
    path = request.path
    if path == reverse('sales:customers'):
        return mark_safe('<option value="reverse_gs">公户转私户</option>')
    else:
        return mark_safe('<option value="reverse_sg">私户转公户</option>')



from django.http.request import QueryDict
# 路径拼接,返回原路径
@register.simple_tag
def reverse_url(request,pk,url_name):
    path = request.get_full_path()
    query_dict_obj = QueryDict(mutable=True)
    query_dict_obj['next'] = path
    encode_url = query_dict_obj.urlencode()
    # print(encode_url,type(encode_url),'---')
    #next=%2Fcustomers%2F%3Fsearch_field%3Dname__contains%26keyword%3Dxm2%26page%3D2 <class 'str'>

    prefix_path = reverse(url_name,args=(pk,))

    full_path = prefix_path + '?' + encode_url
    return full_path


@register.simple_tag
def reverse_url_add(url_name,request):
    from django.http.request import QueryDict
    # /sales/consultrecords/
    next_path = request.get_full_path()
    query_dict_obj = QueryDict(mutable=QueryDict) #  //???
    query_dict_obj['next'] = next_path
    # print(query_dict_obj)  # < QueryDict: {'next': ['/sales/consultrecords/']} >
    encode_url = query_dict_obj.urlencode()  # next=%2Fcustomers%2F%3Fsearch_field%3Dqq%26keyword%3D123%26page%3D3

    per_path = reverse(url_name)  # /editconsult_record/
    # full_path = per_path + '?next=' + next_path
    full_path = per_path + '?' + encode_url
    return full_path

# http://127.0.0.1:8000/editconsult_record/?next=/sales/consultrecords/