#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/18 22:45
# @Author  : 冉勇
# @Site    : 
# @File    : main.py
# @Software: PyCharm
# @desc    :

import os
import random
from time import sleep
from bdb import set_trace
from common import init_mooc
from bs4 import BeautifulSoup
import re
import json
import sys
import requests

# 国际商务谈判
BaseURL = "https://course.icve.com.cn"
# 考试url
ExamURL = "https://spoc-exam.icve.com.cn"
# 课程id
courseId = "1754b2c1a83f4268a668e959b9d3941a"
# 评价课程id
subjectId = "89008fd3260bd552a84da2fdc2ebd3a8"
# 评价内容
content = ['非常好', '非常非常的好', '课程精彩，通熟易懂','非常好 课程里的知识很丰富']
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'Accept-Encodign': 'gzip, deflate, br',
    'Cookie': 'JSESSIONID=6AF0A5207E7F87A454361797A8D603EC; _abfpc=1d466485af98ed5add63780f7b4ace668b0502d5_2.0; cna=d0ed267474e1abe89b79166eab802eac; ssxmod_itna=eqAxBC0Qq7qWuDBPr97QGQtIO7D0DCq2W7nDDsqtrDSxGKidDqxBWWl2He9v9vhiAClo2oDgnTP0Nfb9l74h=5llWeDHxY=DUpDTeqrDeW=D5xGoDPxDeDAQKiTDY4DdjpNv=DEDeKDRDAQDzwd/4h6z/G=DI3iDmTLDx7t9ITL5qeG2DGUeIkGx7qDMIeGXC0nPxDUTTZwMIMuixYPWQk0xxBQD7di9DYoUneDHzdN8ghDW0Gm10iQ5WOxqt+G+7Gme/RhA/GGi7xqLdYeGYr+1b5DAYDj1CiD=; ssxmod_itna2=eqAxBC0Qq7qWuDBPr97QGQtIO7D0DCq2WYikIqqhDlphxjb+xj8drKju5QqL3QD6mYmtQjBPeuDwjW3jAqvee4Yv8eCKdYcftOKCDXesC+iF4OqlKUycajU8B1dQ2BWuHqOQfcS6q/24ax9DdEc5C2mKCYIyGZY7GPhrOWp74jCvGErqCPKwh+pvGq0YN+Rqa0pAGW3BaQfHGL9bx0WkCclYaAF5QlC2hDH3202n7OIeTKAjiQO8F6cIhNgLoDQFODjKD+a95=nxbMAQOYpDK4D=; _uid=10b64d0f-5e25-46df-aa14-9e89b0f28624; aliyungf_tc=c9ec8cdfbda8bcd917ef59b8ff4bdd109baf6ad818c5b9c097917d41d0d78f5b; UNTYXLCOOKIE=dXNlci5pY3ZlLmNvbS5jbnx8MWRjZjNmMWY3OTI3NjM2MTVmYmNjM2Q3MDlmMjBhNDN8fDEzMjA2MjY5ODA0fHx6aHpq; learning-course=ms32amyox4hk6j6arvwmra_1754b2c1a83f4268a668e959b9d3941a___; jwplayer.volume=50; JSESSIONID=0E83027FAC1E707AFE9032C602BF79BF.learnspace_kfkc_aliyun; h_courseId=1754b2c1a83f4268a668e959b9d3941a; platform_flag=learnspace; learnspace_taolun=e546ee25771cb793b3354ca277163e90; sid=6a8bfaf1-d01e-4793-a638-082109d758b6; ST="EufDh1+COY0BfbNDo489T75IhLESzhlHQd2EWk9l2sI="; acw_tc=2f6fc12616715246022135707eb6bd8a1e9a9b7c509cc544522bd5e06fa1c9; token=91d9c9b5-ed6d-4883-81d2-99061f7029b6; rest_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dpbklkIjoiMTMyMDYyNjk4MDQiLCJzaXRlQ29kZSI6InpoemoiLCJ1c2VyX25hbWUiOiIxMzIwNjI2OTgwNCIsInBob3RvIjoibnVsbCIsInN1SWQiOiJtczMyYW15b3g0aGs2ajZhcnZ3bXJhIiwiYXV0aG9yaXRpZXMiOlsiUk9MRV9TVFVERU5UIl0sImNsaWVudF9pZCI6IjIxMDgxODc3MTgiLCJ0cnVlTmFtZSI6IuWGieWLhyIsInN1ZElkIjoibXMzMmFteW94NGhrNmo2YXJ2d21yYSIsInJvbGVDb2RlIjoiMCIsInNjb3BlIjpbImFsbCJdLCJyb2xlTmFtZSI6IuWtpueUnyIsImV4cCI6MTY3MjczNDgwOCwianRpIjoiNmRjMDNkZTItMjE2Zi00ZjVmLWJkM2QtMzQ3N2YyMzJjMmUxIn0.elM8UJHeA_x45Ca7YmlCdax1a7fZ2kSFWFtpjuNuUOTNlutVVHq3xbZpWnwyQoTiyLPdTq2oqmInj_U7tr1gO4ROTdg4gKoDDXB-LmJwpinCxBQYziIh2kKV0tl1RHTZ7KudmqryV28gBxs2LxXoliluTMA_ic3Fnr8SlLi-KGksVC36iAVjF_SlR0T-AbEkGoIfV5jbQ-Vr6cM3jWUgvJD4phpS-tmkiEcrMPmK5HNtOLkoXeZt9JHG-iXE3RX3C-M76pPCfRq_xwdqSqEnUQIV9nBj_s0YCN2oaPFmSNNA_p1ObYsBMpOpOgPttUesX9jiDu1xUw2JxePYBWs0AQ; SERVERID=22293c637420c41b505231fd808611e8|1671525221|1671507410; JSESSIONID=650103F18C7B70C516927888E95BCE46; ST="OzvezF+BP115bg5zlCp4r7Z5T6zTGQTZwFfeLBoi/PM="; SERVERID=35549bc96e85f1047cf442f13900a400|1671526710|1671507410'
}

# 获取limitId
res = requests.get(
    url=f'{BaseURL}/learnspace/learn/learn/templateeight/index.action?params.courseId={courseId}___¶ms.templateType=8¶ms.templateStyleType=0¶ms.template=templateeight¶ms.classId=¶ms.tplRoot=learn',
    headers=header)
patter = re.compile('limitId.*;')
try:
    limitId = patter.search(res.content.decode()).group().split('"')[1]
except:
    print('\033[31m获取limitId失败，检查Cookie\033[0m')
    exit()

# 获得itemId
res = requests.get(
    f'{BaseURL}/learnspace/learn/learn/templateeight/courseware_index.action?params.courseId={courseId}___',
    headers=header
)
soup = BeautifulSoup(res.content, 'lxml')
# print("soup:", soup)

# ----------------------------------分割线----------------------------------
# # 判断视频
# divs = soup.find_all(id=re.compile("s_point_.*"), itemtype="video")
# # 视频的id
# itemids = {}
# for i in divs:
#     itemids[i.find(class_="s_pointti").text] = i['id'].strip("s_point_")
# print("获取所有视频id===>", itemids, "开始刷课===>")
# # print("itemids.keys():", itemids.keys())
# # 开始刷课
# for key in itemids.keys():
#     itemid = itemids[key]
#     print("itemid:", itemid)
#     itemid = itemids[key]
#     data2 = {
#         'itemId': itemid,
#         'videoTotalTime': '00:10:00'
#     }
#     total = requests.post(url='https://course.icve.com.cn/learnspace/course/plugins/cloud_updateVideoTotalTime.action',
#                           headers=header, data=data2)
#     # 判断视频是否学习完成
#     data2 = {
#         'params.courseId': f'{courseId}___',
#         'params.itemId': itemid
#     }
#     complete = requests.post(
#         url=f'{BaseURL}/learnspace/learn/learnCourseware/getSingleItemCompleteCase.json',
#         headers=header, data=data2)
#     print("code:", complete.content.decode())
#     # 判断返回值 1表示学习完成，2表示部分学习，0表示内容没有学习过
#     if json.loads(complete.content.decode())['result']['completed'] == '1':
#         print(key, '视频状态已完成，跳过')
#         continue
#     # 刷课
#     start = 0
#     end = 0
#     # 轮询片段
#     while True:
#         start = end
#         # 每次增加10秒
#         end = start + 20
#         while True:
#             cmd = os.popen('node ./test.js %s %s %s' % (itemid, start, end))
#             # 原始字符串的开头和结尾删除给定的字符
#             studyrecord = cmd.read().strip('\n')
#             cmd.close()
#             data = {
#                 "limitId": limitId,
#                 "studyRecord": studyrecord
#             }
#             res2 = requests.post(
#                 url=f'{BaseURL}/learnspace/course/study/learningTime_saveVideoLearnDetailRecord.action',
#                 headers=header, data=data
#             )
#             if '保存成功' in res2.content.decode() or '总时长' in res2.content.decode():
#                 print("\r", end="")
#                 print(key, "\033[32m学习时长: {}秒 \033[0m".format(end), end="")
#                 sys.stdout.flush()
#                 break
#             else:
#                 pass
#         if '总时长' in res2.content.decode():
#             break
#     print(key, '\033[31m学习完成\033[0m')
#
# # 判断文档
# divs = soup.find_all(id=re.compile("s_point_.*"), itemtype="doc")
# itemids = {}
# for i in divs:
#     itemids[i.find(class_="s_pointti").text] = i['id'].strip("s_point_")
# # 轮询item
# print("获取所有文档id===>", itemids, "开始刷文档===>")
# for key in itemids.keys():
#     itemid = itemids[key]
#     # 判断文档是否学习完成
#     data2 = {
#         'params.courseId': f'{courseId}___',
#         'params.itemId': itemid
#     }
#     complete = requests.post(
#         url=f'{BaseURL}/learnspace/learn/learnCourseware/getSingleItemCompleteCase.json',
#         headers=header, data=data2)
#     # 判断返回值 1表示学习完成，2表示部分学习，0表示内容没有学习过
#     if json.loads(complete.content.decode())['result']['completed'] == '1':
#         print(key, '状态已完成，跳过')
#         continue
#     # 保存文档
#     doc_data = {
#         'courseId': f'{courseId}',
#         'itemId': itemid,
#         'recordType': 0,
#         'studyTime': 300
#     }
#     response = requests.post(
#         url=f'{BaseURL}/learnspace/course/study/learningTime_saveCourseItemLearnRecord.action',
#         headers=header, data=doc_data)
#     if '成功' in response.content.decode():
#         print(key, '完成')
#     else:
#         print(key, '保存失败')
#         set_trace()
#
# # 判断文本
# divs = soup.find_all(id=re.compile("s_point_.*"), itemtype="text")
# # print(divs)
# itemids = {}
# for i in divs:
#     itemids[i.find(class_="s_pointti").text] = i['id'].strip("s_point_")
# # 轮询item
# print("获取所有图文id===>", itemids, "开始刷图文===>")
# for key in itemids.keys():
#     itemid = itemids[key]
#     # 判断文档是否学习完成
#     data2 = {
#         'params.itemId': itemid,
#         'params.courseId': f'{courseId}___'
#     }
#     complete = requests.post(
#         url=f'{BaseURL}/learnspace/learn/learnCourseware/getSingleItemCompleteCase.json',
#         headers=header, data=data2)
#     # 判断返回值 1表示学习完成，2表示部分学习，0表示内容没有学习过
#     if json.loads(complete.content.decode())['result']['completed'] == '1':
#         print(key, '状态已完成，跳过')
#         continue
#     # 保存图文
#     doc_data = {
#         'courseId': courseId,
#         'studyTime': 300,
#         'itemId': itemid,
#         'recordType': 0
#     }
#     # 判断图文是否学习完成
#     response = requests.post(
#         url=f'{BaseURL}/learnspace/course/study/learningTime_saveCourseItemLearnRecord.action',
#         headers=header, data=doc_data)
#     if json.loads(complete.content.decode())['result']['completed'] == '1':
#         print(key, '完成')
#     else:
#         print(key, '保存失败')
# #         set_trace()
#
# # 课程评价
# data = {"params": {f"subjectId": f"{subjectId}", "star": 5}}
# response = requests.post(
#     url=f'{BaseURL}/discuss-api/discussStar/saveStar', headers=header, json=data)
# if json.loads(response.content.decode())['code'] == '1':
#     print("进行评价")
#     create_data = {
#         "bean": {"subjectId": f"{subjectId}", "content": f"{random.choice(content)}", "thumbImgs": "",
#                  "originalImgs": ""}}
#     response = requests.post(
#         url=f"{BaseURL}/discuss-api/discussComment/create",
#         headers=header, json=create_data
#     )
#     if json.loads(response.content.decode())['code'] == '1':
#         print("课程评价完成！")
#     else:
#         print("错误了！", response.content.decode())
# else:
#
#     print("错误了！", response.content.decode())


# -----------------未开发功能-----------------
# # 判断音频
# divs = soup.find_all(id=re.compile("s_point_.*"), itemtype="audio")
# # 音频的id
# itemids = {}
# for i in divs:
#     itemids[i.find(class_="s_pointti").text] = i['id'].strip("s_point_")
# print("获取所有音频id===>", itemids, "开始刷音频>>>>")
# # 开始刷音频
# for key in itemids.keys():
#     itemid = itemids[key]
#     print("itemid:", itemid)
#     # 判断音频是否学习完成
#     data2 = {
#         'params.courseId': f'{courseId}___',
#         'params.itemId': itemid
#     }
#     complete = requests.post(
#         url=f'{BaseURL}/learnspace/learn/learnCourseware/getSingleItemCompleteCase.json',
#         headers=header, data=data2)
#     print("code:", complete.content.decode())
#     # 判断返回值 1表示学习完成，2表示部分学习，0表示内容没有学习过
#     if json.loads(complete.content.decode())['result']['completed'] == '1':
#         print(key, '音频状态已完成，跳过')
#         continue
#     # 刷音频
#     print(f"检测到未刷音频{key}，开始刷音频")
#     while True:
#         start = 0
#         end = 0
#         # 轮询片段
#         while True:
#             start = end
#             # 每次增加10秒
#             end = start + 300
#             cmd = os.popen('node ./test.js %s %s %s' % (itemid, start, end))
#             # 原始字符串的开头和结尾删除给定的字符
#             # studyRecord参数就是将数据格式化后序列化再进行AES加密得到的字符串
#             studyrecord = cmd.read().strip('\n')
#             cmd.close()
#             data = {
#                 "limitId": limitId,
#                 "studyRecord": studyrecord
#             }
#             res2 = requests.post(
#                 url=f'{BaseURL}/learnspace/course/study/learningTime_saveAudioLearnDetailRecord.action',
#                 headers=header, data=data
#             )
#             if '请求成功' in res2.content.decode():
#                 print("\r", end="")
#                 print(key, "\033[32m学习时长: {}秒 \033[0m".format(end), end="")
#                 sys.stdout.flush()
#                 break
#         print(key, '\033[31m学习完成\033[0m')


# todo:需要重新解讨论参数
# # 判断讨论
# divs = soup.find_all(id=re.compile("s_point_.*"), itemtype="topic")
# # print(divs)
# itemids = {}
# for i in divs:
#     itemids[i.find(class_="s_pointti").text] = i['id'].strip("s_point_")
# # 轮询item
# print("获取所有讨论id===>", itemids, "开始刷讨论===>")
# for key in itemids.keys():
#     itemid = itemids[key]
#     print("itemid--->", itemid)
#     data2 = {
#         'currentId': '402883ab80d6633a018330a12d672bbf',
#         'action': "reply",
#         'curPage': 34,
#         'parentId': '402883ab80d6633a018330a12d672bbf',
#         'mainId': '402883ab80d6633a018330a12d672bbf',
#         'content': '<p>11</p>',
#         'itemId': '402883a9832d1365018330a12d481e49',
#         'courseId': '1754b2c1a83f4268a668e959b9d3941a',
#         'createUserId': '402883e5811970fc0183f4ae5cbf55e8',
#         'createUserName': '13206269804',
#         'createNickName': '冉勇',
#         'createPicFileName': 'null',
#         'replyUserId': '402883e48119710601832876cf911f17',
#         'replyUserName': '13983127453',
#         'replyNickName': '金莹',
#         'loginType': 0
#     }
#     complete = requests.post(
#         url=f'{BaseURL}/taolun/learn/courseTopicAction.action',
#         headers=header, data=data2)
#     print("--->", complete.content.decode())

# todo:需要重新解析考试网址
# # 判断随堂考试
# divs = soup.find_all(id=re.compile("s_point_.*"), itemtype="exam")
# # print(divs)
# itemids = {}
# for i in divs:
#     itemids[i.find(class_="s_pointti").text] = i['id'].strip("s_point_")
# # 轮询item
# print("获取所有考试id===>", itemids, "开始刷考试===>")
# for key in itemids.keys():
#     itemid = itemids[key]
#     # 判断测验是否完成
#     print(itemid)
#     data2 = {
#         'params.itemId': itemid,
#         'params.courseId': f'{courseId}___'
#     }
#     complete = requests.post(
#         url=f'{BaseURL}/learnspace/learn/learnCourseware/getSingleItemCompleteCase.json',
#         headers=header, data=data2)
#     if json.loads(complete.content.decode())['result']['completed'] == '1':
#         print(key, '状态已完成，跳过')
#         continue
#     # 考试
#     print("开始考试---->")
#     # todo:考试逻辑
#     doc_data = {
#         'courseId': f'{courseId}___',
#         'studyTime': 300,
#         'itemId': itemid,
#     }
#     # 判断图文是否学习完成
#     response = requests.post(
#         url=f'{BaseURL}/learnspace/course/study/learningTime_saveLearningTime.action',
#         headers=header, data=doc_data)
#     if '成功' in response.content.decode():
#         print(key, '完成')
#     else:
#         print(key, '保存失败')
#         set_trace()

# todo:
#  刷课类型：itemtype="doc(实现)"、exam(待实现)、topic(待实现)、video(实现)、text(实现)、audio(待实现)
