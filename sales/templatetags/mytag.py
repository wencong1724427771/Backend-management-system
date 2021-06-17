
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
register = template.Library()


@register.simple_tag   #---------******----------
def show_info(request):
    if request.path == reverse('customers'):
        return mark_safe('<option value="">公户转私户</option>')
    else:
        return mark_safe('<option value="">私户转公户</option>')




'''
    {% if request.path == '/customers/' %}
        <option value="1">公户转私户</option>
    {% else %}
        <option value="2">私户转公户</option>
    {% endif %}
'''