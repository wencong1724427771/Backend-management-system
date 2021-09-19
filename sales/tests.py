# # django外部文件使用django环境
# import os
# import random
# if __name__ == '__main__':
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_sys.settings')
#     import django
#     django.setup()
# from django.http.request import QueryDict
# import copy
#     # /sales/consultrecords/
# query_dict_obj = QueryDict(mutable=QueryDict)
# print(query_dict_obj,type(query_dict_obj))
#
# a = copy.copy(query_dict_obj)
# print(a,type(a))



