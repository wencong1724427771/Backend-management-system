# django外部文件使用django环境
# import os
# if __name__ == '__main__':        # 配置django环境变量
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Login.settings')
#     import django
#     django.setup()  # 运行django环境变量
#
#     from sales import models
#     import random
#
#     sex_type = (('male', '男性'), ('female', '女性'))
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
#
#     obj_list=[]
#     for i in range(250):
#         obj = models.Customer(
#             qq=f'{i+1}236789',
#             name=f'liye{i}',
#             sex=random.choice(sex_type)[0],
#             source=random.choice(source_type)[1],
#             course=random.choice(course_choices)[1],
#         )
#         obj_list.append(obj)
#
#     models.Customer.objects.bulk_create(obj_list)
# page_number_range = range(1,255)
# print(page_number_range,type(page_number_range))

list = [0,1,2,3,4,5,6,7,8,9]
print(list[0:3])
print(list[0:13])
print(list[10:14])
page_html = '<a></a>'
st = 'afa%ssdf' %page_html
print(st)