# -*- coding = utf-8 -*-
# @Time: 2021/8/3 20:06
# @Author: Bon
# @File: xx.py
# @Software: PyCharm

# # django外部文件使用django环境
# import os
# import random
# if __name__ == '__main__':
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_sys.settings')
#     import django
#     django.setup()
#
#     from sales import models
#     sex = ['male','female']
#     source_type = (('qq', "qq群"),
#                    ('referral', "内部转介绍"),
#                    ('website', "官方网站"),
#                    ('baidu_ads', "百度推广"),
#                    ('office_direct', "直接上门"),
#                    ('WoM', "口碑"),
#                    ('public_class', "公开课"),
#                    ('website_luffy', "路飞官网"),
#                    ('others', "其它"),)
#     course_choices = (('LinuxL', 'Linux中高级'),
#                       ('PythonFullStack', 'Python高级全栈开发'),)
#     obj_list = []
#
#     for i in range(251):
#         obj = models.Customer(
#             qq = f'{i+1}2345798',
#             name = f'xm{i+1}',
#             sex = random.choice(sex),
#             source = random.choice(source_type)[1],
#             course=random.choice(course_choices[1]),
#         )
#         obj_list.append(obj)
#
#     models.Customer.objects.bulk_create(obj_list)

