# from collections import OrderedDict   # 3.6之后默认有序
#
# d1 = {
#         1: {
#             'name': '业务系统',
#             'icon': 'fa-address-card-o',
#             'weight': 100,
#             'children': [{
#                 'title': '客户管理',
#                 'url': '/customers/'
#             }, {
#                 'title': '私户信息展示',
#                 'url': '/mycustomers/'
#                 }]
#             },
#         2: {
#             'name': '教务系统',
#             'icon': 'fa-user-circle-o',
#             'weight': 200,
#             'children': [{
#                 'title': '课程记录展示',
#                 'url': '/courserecord/'
#             }]
#         }
# }
# sort_d1 = sorted(d1,key=lambda x:d1[x]['weight'],reverse=True)    # x是字典的键
#
# order_dict = OrderedDict()
# for key in sort_d1:
#     order_dict[key] = d1[key]
# print(order_dict)

# dic = {1:'xx',2:'oo'}
# for i in dic:
#     print(i)
#     '''
#     1
#     2
#     '''


print('------元组打散-------')
tup = (1,2,3,4)
print(tup)
print(*tup)
print('------列表打散-------')


print('------字典打散-------')    # 字典的拆包放在函数中
def func_dic(name, age):
    print(name, age)

# **将字典打散
dic = {'name': '张三', 'age': 20}
func_dic(**dic)        # 打散的只是  值     且本句与 func_dic(name='张三'， age=20)等价
print(**dic)