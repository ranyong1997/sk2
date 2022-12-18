#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/18 22:45
# @Author  : 冉勇
# @Site    : 
# @File    : main.py
# @Software: PyCharm
# @desc    :

import os
from bs4 import BeautifulSoup
import re
import json
import sys
import requests

BaseURL = "https://course.icve.com.cn"
# 课程id
courseId = "1754b2c1a83f4268a668e959b9d3941a"
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Encodign': 'gzip, deflate, br',
    'Cookie': 'JSESSIONID=B39C70F71A9B138AB8920AC997D1E4D0; aliyungf_tc=2fc0927f5a3ee5d612d75f5690676ab1366280ad5c6a2dc2aa3d1b76283c9f66; JSESSIONID=59CE88C8727A464FFA345A6758817E7F.learnspace_kfkc_aliyun; _abfpc=f26831421fa2dbe36317aa541ed619c05460effe_2.0; cna=f39af516d46dc05b2480a382baddeb0d; _uid=d2b7a2af-4691-4a84-b203-65ecfcab3e22; jwplayer.volume=50; learnspace_taolun=0be5d730b745f30657fe2554fde22ded; sid=f03db508-22eb-4047-9238-88db953fa0da; h_courseId=1754b2c1a83f4268a668e959b9d3941a; platform_flag=learnspace; ST="BnD3eMizlU4AV0ueX929Vpgq1EF2EXdus64ZJEfmlAI="; rest_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dpbklkIjoiMTMyMDYyNjk4MDQiLCJzaXRlQ29kZSI6InpoemoiLCJ1c2VyX25hbWUiOiIxMzIwNjI2OTgwNCIsInBob3RvIjpudWxsLCJzdUlkIjoibXMzMmFteW94NGhrNmo2YXJ2d21yYSIsImF1dGhvcml0aWVzIjpbIlJPTEVfU1RVREVOVCJdLCJjbGllbnRfaWQiOiIyMTA4MTg3NzE4IiwidHJ1ZU5hbWUiOiLlhonli4ciLCJzdWRJZCI6Im1zMzJhbXlveDRoazZqNmFydndtcmEiLCJyb2xlQ29kZSI6IjAiLCJzY29wZSI6WyJhbGwiXSwicm9sZU5hbWUiOiLlrabnlJ8iLCJleHAiOjE2NzI0ODA0OTUsImp0aSI6IjhhMzEwYmNhLTBhOTItNGJkNi1iNTljLWZiMDYxOTY5ZTMxMiJ9.C1uheB06kxBlKLzSzF_3KMVftFo_k8sw422qmGVVgbP4uf9zg8OKcXOT15-eQG4cNYHH5kqYnaFpNsdovsL1ulliMtT1STlcGy3Ffxy93RfE1jueEKyzxBdGecbueUE1nS4z8B52ZCXHgxF0sgs8YxzsKW8pdd1BqIkgdnCfAitsZMYoC5r2eUHZck8l0EM9avhWErGePnzDIOLeGw_QIbTE78Xjk6W-CRm95WDXqbfr0X9DuGG56VQEcX02AXupB3-Ige6pPJJq8x4kovSHT5ysrWbc8goOY44hNYRVly3ePflY3m1V6P85kAsxKs4xhJOfy_-KVwrNMUCBZxDXRw; token=1531fdf6-d778-46ae-aa05-e6e8575fd543; UNTYXLCOOKIE=dXNlci5pY3ZlLmNvbS5jbnx8MWRjZjNmMWY3OTI3NjM2MTVmYmNjM2Q3MDlmMjBhNDN8fDEzMjA2MjY5ODA0fHx6aHpq; learning-course=ms32amyox4hk6j6arvwmra_1754b2c1a83f4268a668e959b9d3941a___; acw_tc=707c9f6916713756937186072e180d1e2eb8501e70dd005549fefb76e81c52; alicfw=3865426961%7C2125469483%7C1328233664%7C1328233175; alicfw_gfver=v1.200309.1; SERVERID=16f30ddb1f23abc6369b5e279368fe9f|1671376557|1671244551',
    'Content-Type': 'application/json',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
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
print("soup:", soup)
# 刷视频
divs = soup.find_all(id=re.compile("s_point_.*"), itemtype="video")
# 视频的id
itemids = {}
for i in divs:
    itemids[i.find(class_="s_pointti").text] = i['id'].strip("s_point_")
print("获取所有视频id===>", itemids, "开始刷课===>")
print("itemids.keys():", itemids.keys())
# 开始刷课
for key in itemids.keys():
    itemid = itemids[key]
    print("itemid:", itemid)
    data2 = {
        'itemId': itemid,
        'videoTotalTime': '00:10:00'
    }
    total = requests.post(url=f'{BaseURL}/learnspace/course/plugins/cloud_updateVideoTotalTime.action',
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
    # 判断返回值 0为成功，1为失败
    if json.loads(complete.content.decode())['result']['completed'] == '0':
        print(key, '视频状态已完成，跳过')
    continue
    # 刷课
    start = 0
    end = 0
    while True:
        start = end
        # 每次增加20秒
        end = start + 20
        cmd = os.popen('node ./test.js %s %s %s' % (itemid, start, end))
        # 原始字符串的开头和结尾删除给定的字符
        studyrecord = cmd.read().strip('\n')
        cmd.close()
        data = {
            "limitId": itemid,
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
    sleep(1)

# 刷文档
divs = soup.find_all(id=re.compile("s_point_.*"), itemtype="doc")
itemids = {}
for i in divs:
    itemids[i.find(class_="s_pointti").text] = i['id'].strip("s_point_")
    # 轮询item
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

# todo:
#  刷课类型：itemtype="doc"、exam(测验)、topic(讨论)、video
