#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/9 16:58
# @Author  : 冉勇
# @Site    : 
# @File    : test.py
# @Software: PyCharm
# @desc    :
import random
from bdb import set_trace
from time import sleep
from common import init_mooc
import requests
from bs4 import BeautifulSoup
import re
import os
import json
import sys

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Encodign': 'gzip, deflate, br',
    'Cookie': '',
    'Content-Type': 'application/json',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
}

for key, value in init_mooc.get_user_all().items():
    a = init_mooc.login(name=key, password=value)
    print(a[0])
    header['Cookie'] = f'webtrn_cms={a[3]}; whatysns=751f50efbd43e9d7505ebdaa9ac85ff3; webtrn=9eb19412ac0dbc2ebe3eccd20fd6e9c6; _abfpc=f26831421fa2dbe36317aa541ed619c05460effe_2.0; cna=f39af516d46dc05b2480a382baddeb0d; JSESSIONID={a[4]}; _uid=465596ae-2b2a-4f73-abf7-2e998c2fd451; acw_tc={a[1]}; token={a[0]}; SERVERID={a[2]}'
print(header['Cookie'])


header[
    'Cookie'] = 'JSESSIONID=0ED04E93C86D68DA2CF0D03094145661; aliyungf_tc=2fc0927f5a3ee5d612d75f5690676ab1366280ad5c6a2dc2aa3d1b76283c9f66; JSESSIONID=59CE88C8727A464FFA345A6758817E7F.learnspace_kfkc_aliyun; _abfpc=f26831421fa2dbe36317aa541ed619c05460effe_2.0; cna=f39af516d46dc05b2480a382baddeb0d; UNTYXLCOOKIE=dXNlci5pY3ZlLmNvbS5jbnx8MWRjZjNmMWY3OTI3NjM2MTVmYmNjM2Q3MDlmMjBhNDN8fDEzMjA2MjY5ODA0fHx6aHpq; learning-course=ms32amyox4hk6j6arvwmra_1754b2c1a83f4268a668e959b9d3941a___; _uid=d2b7a2af-4691-4a84-b203-65ecfcab3e22; token=d271970f-a6ec-46b5-ae11-1f40367beda9; acw_tc=707c9f6716712679062397759e01f8eb14abb3a11b2f43df9524ce9212acdb; alicfw=3124608875%7C2125642936%7C1328233664%7C1328232708; alicfw_gfver=v1.200309.1; SERVERID=db0581f1d84e519339e911738e844a10|1671268091|1671244551'

# 获得limitId
res = requests.get(
    url='https://course.icve.com.cn/learnspace/learn/learn/templateeight/index.action?params.courseId=1754b2c1a83f4268a668e959b9d3941a___¶ms.templateType=8¶ms.templateStyleType=0¶ms.template=templateeight¶ms.classId=¶ms.tplRoot=learn',
    headers=header)
patter = re.compile('limitId.*;')
try:
    limitId = patter.search(res.content.decode()).group().split('"')[1]
except:
    print('\033[31m获取limitId失败，检查Cookie\033[0m')
    exit()

# 获得itemId
res = requests.get(
    'https://course.icve.com.cn/learnspace/learn/learn/templateeight/courseware_index.action?params.courseId=1754b2c1a83f4268a668e959b9d3941a___',
    headers=header)
soup = BeautifulSoup(res.content, 'lxml')
divs = soup.find_all(id=re.compile("s_point_.*"), itemtype="video")
itemids = {}
for i in divs:
    itemids[i.find(class_="s_pointti").text] = i['id'].strip("s_point_")

# 开始刷课
for key in itemids.keys():
    itemid = itemids[key]
    data2 = {
        'itemId': itemid,
        'videoTotalTime': '00:10:00'
    }
    total = requests.post(url='https://course.icve.com.cn/learnspace/course/plugins/cloud_updateVideoTotalTime.action',
                          headers=header, data=data2)

    # 判断视频是否学习完成
    data2 = {
        'params.courseId': '1754b2c1a83f4268a668e959b9d3941a___',
        'params.itemId': itemid
    }
    complete = requests.post(
        url='https://course.icve.com.cn/learnspace/learn/learnCourseware/getSingleItemCompleteCase.json',
        headers=header, data=data2)
    if json.loads(complete.content.decode())['result']['completed'] == '1':
        print(key, '视频状态已完成，跳过')
        continue

    start = 0
    end = 0
    # 轮询片段
    while True:
        start = end
        end = start + 20
        # 单个视频片段状态保存循环
        while True:
            cmd = os.popen('node ./test.js %s %s %s' % (itemid, start, end))
            studyrecord = cmd.read().strip('\n')
            cmd.close()
            data = {
                'limitId': limitId,
                'studyRecord': studyrecord
            }
            res2 = requests.post(
                url='https://course.icve.com.cn/learnspace/course/study/learningTime_saveVideoLearnDetailRecord.action',
                headers=header, data=data)
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

# 刷文档内容

# 取出itemid
divs = soup.find_all(id=re.compile("s_point_.*"), itemtype="doc")
itemids = {}
for i in divs:
    itemids[i.find(class_="s_pointti").text] = i['id'].strip("s_point_")

# 轮询item
for key in itemids.keys():
    itemid = itemids[key]

    # 判断文档是否学习完成
    data2 = {
        'params.courseId': '1754b2c1a83f4268a668e959b9d3941a___',
        'params.itemId': itemid
    }
    complete = requests.post(
        url='https://course.icve.com.cn/learnspace/learn/learnCourseware/getSingleItemCompleteCase.json',
        headers=header, data=data2)
    if json.loads(complete.content.decode())['result']['completed'] == '1':
        print(key, '状态已完成，跳过')
        continue

    # 保存文档
    doc_data = {
        'courseId': '1754b2c1a83f4268a668e959b9d3941a',
        'itemId': itemid,
        'recordType': 0,
        'studyTime': 300
    }
    response = requests.post(
        url='https://course.icve.com.cn/learnspace/course/study/learningTime_saveCourseItemLearnRecord.action',
        headers=header, data=doc_data)
    if '成功' in response.content.decode():
        print(key, '完成')
    else:
        print(key, '保存失败')
        set_trace()
