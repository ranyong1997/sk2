#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/18 22:45
# @Author  : 冉勇
# @Site    : 
# @File    : main.py
# @Software: PyCharm
# @desc    :

import os
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
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'Accept-Encodign': 'gzip, deflate, br',
    'Cookie': 'JSESSIONID=2C6C955A502BF2CD111177F97213FDE9; aliyungf_tc=2fc0927f5a3ee5d612d75f5690676ab1366280ad5c6a2dc2aa3d1b76283c9f66; JSESSIONID=59CE88C8727A464FFA345A6758817E7F.learnspace_kfkc_aliyun; _abfpc=f26831421fa2dbe36317aa541ed619c05460effe_2.0; cna=f39af516d46dc05b2480a382baddeb0d; _uid=d2b7a2af-4691-4a84-b203-65ecfcab3e22; jwplayer.volume=50; learnspace_taolun=0be5d730b745f30657fe2554fde22ded; sid=f03db508-22eb-4047-9238-88db953fa0da; h_courseId=1754b2c1a83f4268a668e959b9d3941a; platform_flag=learnspace; rest_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dpbklkIjoiMTMyMDYyNjk4MDQiLCJzaXRlQ29kZSI6InpoemoiLCJ1c2VyX25hbWUiOiIxMzIwNjI2OTgwNCIsInBob3RvIjpudWxsLCJzdUlkIjoibXMzMmFteW94NGhrNmo2YXJ2d21yYSIsImF1dGhvcml0aWVzIjpbIlJPTEVfU1RVREVOVCJdLCJjbGllbnRfaWQiOiIyMTA4MTg3NzE4IiwidHJ1ZU5hbWUiOiLlhonli4ciLCJzdWRJZCI6Im1zMzJhbXlveDRoazZqNmFydndtcmEiLCJyb2xlQ29kZSI6IjAiLCJzY29wZSI6WyJhbGwiXSwicm9sZU5hbWUiOiLlrabnlJ8iLCJleHAiOjE2NzI0ODA0OTUsImp0aSI6IjhhMzEwYmNhLTBhOTItNGJkNi1iNTljLWZiMDYxOTY5ZTMxMiJ9.C1uheB06kxBlKLzSzF_3KMVftFo_k8sw422qmGVVgbP4uf9zg8OKcXOT15-eQG4cNYHH5kqYnaFpNsdovsL1ulliMtT1STlcGy3Ffxy93RfE1jueEKyzxBdGecbueUE1nS4z8B52ZCXHgxF0sgs8YxzsKW8pdd1BqIkgdnCfAitsZMYoC5r2eUHZck8l0EM9avhWErGePnzDIOLeGw_QIbTE78Xjk6W-CRm95WDXqbfr0X9DuGG56VQEcX02AXupB3-Ige6pPJJq8x4kovSHT5ysrWbc8goOY44hNYRVly3ePflY3m1V6P85kAsxKs4xhJOfy_-KVwrNMUCBZxDXRw; UNTYXLCOOKIE=dXNlci5pY3ZlLmNvbS5jbnx8MWRjZjNmMWY3OTI3NjM2MTVmYmNjM2Q3MDlmMjBhNDN8fDEzMjA2MjY5ODA0fHx6aHpq; learning-course=ms32amyox4hk6j6arvwmra_1754b2c1a83f4268a668e959b9d3941a___; alicfw=3865426961%7C2125469483%7C1328233664%7C1328233175; alicfw_gfver=v1.200309.1; ST="Lp0N24NZQ4ikzOAMzeiD6hHlVqsivGtyBkQh+vyyjujPynPKx9AvIA=="; acw_tc=76b20f8116714615264758520e25b26cba2a5bb7cd1e00dec9f9dec8a5b871; token=e3d13e42-b2d3-472e-9b37-a3d8035bc0ef; SERVERID=16f30ddb1f23abc6369b5e279368fe9f|1671462610|1671244551',
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
# 判断视频
divs = soup.find_all(id=re.compile("s_point_.*"), itemtype="video")
# 视频的id
itemids = {}
for i in divs:
    itemids[i.find(class_="s_pointti").text] = i['id'].strip("s_point_")
print("获取所有视频id===>", itemids, "开始刷课===>")
# print("itemids.keys():", itemids.keys())
# 开始刷课
for key in itemids.keys():
    itemid = itemids[key]
    print("itemid:", itemid)
    itemid = itemids[key]
    data2 = {
        'itemId': itemid,
        'videoTotalTime': '00:10:00'
    }
    total = requests.post(url='https://course.icve.com.cn/learnspace/course/plugins/cloud_updateVideoTotalTime.action',
                          headers=header, data=data2)
    # 判断视频是否学习完成
    data2 = {
        'params.courseId': f'{courseId}___',
        'params.itemId': itemid
    }
    complete = requests.post(
        url=f'{BaseURL}/learnspace/learn/learnCourseware/getSingleItemCompleteCase.json',
        headers=header, data=data2)
    print("code:", complete.content.decode())
    # 判断返回值 1表示学习完成，2表示部分学习，0表示内容没有学习过
    if json.loads(complete.content.decode())['result']['completed'] == '1':
        print(key, '视频状态已完成，跳过')
        continue
    # 刷课
    start = 0
    end = 0
    # 轮询片段
    while True:
        start = end
        # 每次增加10秒
        end = start + 20
        while True:
            cmd = os.popen('node ./test.js %s %s %s' % (itemid, start, end))
            # 原始字符串的开头和结尾删除给定的字符
            studyrecord = cmd.read().strip('\n')
            cmd.close()
            data = {
                "limitId": limitId,
                "studyRecord": studyrecord
            }
            res2 = requests.post(
                url=f'{BaseURL}/learnspace/course/study/learningTime_saveVideoLearnDetailRecord.action',
                headers=header, data=data
            )
            if '保存成功' in res2.content.decode() or '总时长' in res2.content.decode():
                print("\r", end="")
                print(key, "\033[32m学习时长: {}秒 \033[0m".format(end), end="")
                sys.stdout.flush()
                break
            else:
                pass
        if '总时长' in res2.content.decode():
            break
    print(key, '\033[31m学习完成\033[0m')

# 判断文档
divs = soup.find_all(id=re.compile("s_point_.*"), itemtype="doc")
itemids = {}
for i in divs:
    itemids[i.find(class_="s_pointti").text] = i['id'].strip("s_point_")
# 轮询item
print("获取所有文档id===>", itemids, "开始刷文档===>")
for key in itemids.keys():
    itemid = itemids[key]
    # 判断文档是否学习完成
    data2 = {
        'params.courseId': f'{courseId}___',
        'params.itemId': itemid
    }
    complete = requests.post(
        url=f'{BaseURL}/learnspace/learn/learnCourseware/getSingleItemCompleteCase.json',
        headers=header, data=data2)
    # 判断返回值 1表示学习完成，2表示部分学习，0表示内容没有学习过
    if json.loads(complete.content.decode())['result']['completed'] == '1':
        print(key, '状态已完成，跳过')
        continue
    # 保存文档
    doc_data = {
        'courseId': f'{courseId}',
        'itemId': itemid,
        'recordType': 0,
        'studyTime': 300
    }
    response = requests.post(
        url=f'{BaseURL}/learnspace/course/study/learningTime_saveCourseItemLearnRecord.action',
        headers=header, data=doc_data)
    if '成功' in response.content.decode():
        print(key, '完成')
    else:
        print(key, '保存失败')
        set_trace()

# 判断文本
divs = soup.find_all(id=re.compile("s_point_.*"), itemtype="text")
# print(divs)
itemids = {}
for i in divs:
    itemids[i.find(class_="s_pointti").text] = i['id'].strip("s_point_")
# 轮询item
print("获取所有图文id===>", itemids, "开始刷图文===>")
for key in itemids.keys():
    itemid = itemids[key]
    # 判断文档是否学习完成
    data2 = {
        'params.itemId': itemid,
        'params.courseId': f'{courseId}___'
    }
    complete = requests.post(
        url=f'{BaseURL}/learnspace/learn/learnCourseware/getSingleItemCompleteCase.json',
        headers=header, data=data2)
    # 判断返回值 1表示学习完成，2表示部分学习，0表示内容没有学习过
    if json.loads(complete.content.decode())['result']['completed'] == '1':
        print(key, '状态已完成，跳过')
        continue
    # 保存图文
    doc_data = {
        'courseId': courseId,
        'studyTime': 300,
        'itemId': itemid,
        'recordType': 0
    }
    # 判断图文是否学习完成
    response = requests.post(
        url=f'{BaseURL}/learnspace/course/study/learningTime_saveCourseItemLearnRecord.action',
        headers=header, data=doc_data)
    if '成功' in response.content.decode():
        print(key, '完成')
    else:
        print(key, '保存失败')
        set_trace()

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

# -----------------未开发功能-----------------
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
