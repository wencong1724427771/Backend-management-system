# -*- coding = utf-8 -*-
# @Time: 2021/8/12 12:35
# @Author: Bon
# @File: icon图标.py
# @Software: PyCharm

# import re
# import requests

# url = 'http://www.fontawesome.com.cn/faicons/#web-application'
#
# response = requests.get(url)
# res_data = response.text
# # <i class="fa fa-address-book-o" aria-hidden="true"></i>
#
# find_tag = re.compile('<i class=".*?" aria-hidden="true"></i>')
# find_text = re.compile('<i class="(.*?)" aria-hidden="true"></i>')
#
# res_tag = re.findall(find_tag, res_data)
# res_text = re.findall(find_text, res_data)
# # print(res_tag)
# # print(res_text)
# icon_list = [[re.findall('<i class="(.*?)" aria-hidden="true"></i>', i)[0], i] for i in res_tag[0:10]]
#
# print(icon_list)


icon_list = [['fa fa-font-awesome', '<i class="fa fa-font-awesome" aria-hidden="true"></i>'],
             ['fa fa-flag fa-fw', '<i class="fa fa-flag fa-fw" aria-hidden="true"></i>'],
             ['fa fa-wheelchair-alt fa-fw', '<i class="fa fa-wheelchair-alt fa-fw" aria-hidden="true"></i>'],
             ['fa fa-camera-retro fa-fw', '<i class="fa fa-camera-retro fa-fw" aria-hidden="true"></i>'],
             ['fa fa-universal-access fa-fw', '<i class="fa fa-universal-access fa-fw" aria-hidden="true"></i>'],
             ['fa fa-hand-spock-o fa-fw', '<i class="fa fa-hand-spock-o fa-fw" aria-hidden="true"></i>'],
             ['fa fa-ship fa-fw', '<i class="fa fa-ship fa-fw" aria-hidden="true"></i>'],
             ['fa fa-venus fa-fw', '<i class="fa fa-venus fa-fw" aria-hidden="true"></i>'],
             ['fa fa-file-image-o fa-fw', '<i class="fa fa-file-image-o fa-fw" aria-hidden="true"></i>'],
             ['fa fa-spinner fa-fw', '<i class="fa fa-spinner fa-fw" aria-hidden="true"></i>'],
             ['fa fa-check-square fa-fw', '<i class="fa fa-check-square fa-fw" aria-hidden="true"></i>'],
             ['fa fa-credit-card fa-fw', '<i class="fa fa-credit-card fa-fw" aria-hidden="true"></i>'],
             ['fa fa-pie-chart fa-fw', '<i class="fa fa-pie-chart fa-fw" aria-hidden="true"></i>'],
             ['fa fa-won fa-fw', '<i class="fa fa-won fa-fw" aria-hidden="true"></i>'],
             ['fa fa-file-text-o fa-fw', '<i class="fa fa-file-text-o fa-fw" aria-hidden="true"></i>'],
             ['fa fa-arrow-right fa-fw', '<i class="fa fa-arrow-right fa-fw" aria-hidden="true"></i>'],
             ['fa fa-play-circle fa-fw', '<i class="fa fa-play-circle fa-fw" aria-hidden="true"></i>'],
             ['fa fa-facebook-official fa-fw', '<i class="fa fa-facebook-official fa-fw" aria-hidden="true"></i>'],
             ['fa fa-medkit fa-fw', '<i class="fa fa-medkit fa-fw" aria-hidden="true"></i>'],
             ['fa fa-flag', '<i class="fa fa-flag" aria-hidden="true"></i>'],
             ['fa fa-search', '<i class="fa fa-search" aria-hidden="true"></i>'],
             ['fas fas-algolia', '<i class="fas fas-algolia" aria-hidden="true"></i>'],
             ['fa fa-address-book', '<i class="fa fa-address-book" aria-hidden="true"></i>'],
             ['fa fa-address-book-o', '<i class="fa fa-address-book-o" aria-hidden="true"></i>'],
             ['fa fa-address-card', '<i class="fa fa-address-card" aria-hidden="true"></i>'],
             ['fa fa-address-card-o', '<i class="fa fa-address-card-o" aria-hidden="true"></i>'],
             ['fa fa-bandcamp', '<i class="fa fa-bandcamp" aria-hidden="true"></i>'],
             ['fa fa-bath', '<i class="fa fa-bath" aria-hidden="true"></i>'],
             ['fa fa-bathtub', '<i class="fa fa-bathtub" aria-hidden="true"></i>'],
             ['fa fa-drivers-license', '<i class="fa fa-drivers-license" aria-hidden="true"></i>'],
             ['fa fa-drivers-license-o', '<i class="fa fa-drivers-license-o" aria-hidden="true"></i>'],
             ['fa fa-eercast', '<i class="fa fa-eercast" aria-hidden="true"></i>'],
             ['fa fa-envelope-open', '<i class="fa fa-envelope-open" aria-hidden="true"></i>'],
             ['fa fa-envelope-open-o', '<i class="fa fa-envelope-open-o" aria-hidden="true"></i>'],
             ['fa fa-etsy', '<i class="fa fa-etsy" aria-hidden="true"></i>'],
             ['fa fa-free-code-camp', '<i class="fa fa-free-code-camp" aria-hidden="true"></i>'],
             ['fa fa-grav', '<i class="fa fa-grav" aria-hidden="true"></i>'],
             ['fa fa-handshake-o', '<i class="fa fa-handshake-o" aria-hidden="true"></i>'],
             ['fa fa-id-badge', '<i class="fa fa-id-badge" aria-hidden="true"></i>'],
             ['fa fa-id-card', '<i class="fa fa-id-card" aria-hidden="true"></i>'],
             ['fa fa-id-card-o', '<i class="fa fa-id-card-o" aria-hidden="true"></i>'],
             ['fa fa-imdb', '<i class="fa fa-imdb" aria-hidden="true"></i>'],
             ['fa fa-linode', '<i class="fa fa-linode" aria-hidden="true"></i>'],
             ['fa fa-meetup', '<i class="fa fa-meetup" aria-hidden="true"></i>'],
             ['fa fa-microchip', '<i class="fa fa-microchip" aria-hidden="true"></i>'],
             ['fa fa-podcast', '<i class="fa fa-podcast" aria-hidden="true"></i>'],
             ['fa fa-quora', '<i class="fa fa-quora" aria-hidden="true"></i>'],
             ['fa fa-ravelry', '<i class="fa fa-ravelry" aria-hidden="true"></i>'],
             ['fa fa-s15', '<i class="fa fa-s15" aria-hidden="true"></i>'],
             ['fa fa-shower', '<i class="fa fa-shower" aria-hidden="true"></i>']]
