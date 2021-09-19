# 需要先注册中间件才能使用
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect

class Auth(MiddlewareMixin):
    # 请求来了自动执行process_request方法
    # 白名单  通过访问路径来放行
    # white_list = ['/login/', ]
    white_list = [reverse('sales:login'),reverse('sales:register')]
    def process_request(self,request):

        path = request.path
        if path not in self.white_list:

            status = request.session.get('account')

            if not status:
                return redirect('sales:login')
        # return None  # 默认