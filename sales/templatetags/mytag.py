
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
register = template.Library()

# 自定义标签，实现不同页面显示不同选项
@register.simple_tag   #---------******----------
def show_info(request):
    if request.path == reverse('customers'):
        return mark_safe('<option value="convert_gs">公户转私户</option>')
    else:
        return mark_safe('<option value="convert_sg">私户转公户</option>')
'''
    {% if request.path == '/customers/' %}
        <option value="1">公户转私户</option>
    {% else %}
        <option value="2">私户转公户</option>
    {% endif %}
'''


@register.simple_tag
def reverse_url(url_name,pk,request):
    from django.http.request import QueryDict
    # /customers/?search_field=qq&keyword=123&page=3
    next_path = request.get_full_path()
    query_dict_obj = QueryDict(mutable=QueryDict)
    query_dict_obj['next'] = next_path
    # print(query_dict_obj)  # < QueryDict: {'next': ['/customers/?search_field=qq&keyword=123']} >
    encode_url = query_dict_obj.urlencode()  # next=%2Fcustomers%2F%3Fsearch_field%3Dqq%26keyword%3D123%26page%3D3
    # url编码 / ？ = & 等不安全字符会被替换成%➕对应的assic码

    per_path = reverse(url_name,args=(pk,))  # /editcustomer/92/
    # full_path = per_path + '?next=' + next_path
    full_path = per_path + '?' + encode_url
    return full_path


# print(type(request.GET))    # <class 'django.http.request.QueryDict'>   request.GET.urlencode()
# # http://127.0.0.1:8000/editcustomer/208/?next=/customers/?search_field=qq&keyword=123&page=3