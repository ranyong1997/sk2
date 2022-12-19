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
    'Cookie': 'JSESSIONID=2A84CEE7CC44375CF50D6CBE2742A4F5; _abfpc=1d466485af98ed5add63780f7b4ace668b0502d5_2.0; cna=d0ed267474e1abe89b79166eab802eac; ssxmod_itna=eqAxBC0Qq7qWuDBPr97QGQtIO7D0DCq2W7nDDsqtrDSxGKidDqxBWWl2He9v9vhiAClo2oDgnTP0Nfb9l74h=5llWeDHxY=DUpDTeqrDeW=D5xGoDPxDeDAQKiTDY4DdjpNv=DEDeKDRDAQDzwd/4h6z/G=DI3iDmTLDx7t9ITL5qeG2DGUeIkGx7qDMIeGXC0nPxDUTTZwMIMuixYPWQk0xxBQD7di9DYoUneDHzdN8ghDW0Gm10iQ5WOxqt+G+7Gme/RhA/GGi7xqLdYeGYr+1b5DAYDj1CiD=; ssxmod_itna2=eqAxBC0Qq7qWuDBPr97QGQtIO7D0DCq2WYikIqqhDlphxjb+xj8drKju5QqL3QD6mYmtQjBPeuDwjW3jAqvee4Yv8eCKdYcftOKCDXesC+iF4OqlKUycajU8B1dQ2BWuHqOQfcS6q/24ax9DdEc5C2mKCYIyGZY7GPhrOWp74jCvGErqCPKwh+pvGq0YN+Rqa0pAGW3BaQfHGL9bx0WkCclYaAF5QlC2hDH3202n7OIeTKAjiQO8F6cIhNgLoDQFODjKD+a95=nxbMAQOYpDK4D=; _uid=10b64d0f-5e25-46df-aa14-9e89b0f28624; aliyungf_tc=2cc934b53a9e2b0d308ff85854a818e7729d7650204be521a68ff8ed1c66f27d; jwplayer.volume=50; alicfw=3773620543%7C2125521110%7C1328233537%7C1328232896; alicfw_gfver=v1.200309.1; learnspace_taolun=1399e65bc4193aadc0cd8bc6a27e6bf1; sid=cc227fa0-6364-400f-8076-2bca3396f99f; ST="nDi5rTR0LL+nMbpgO4avOeY7+kgdwXhJRPgpeFH/Abk="; acw_tc=76b20f8916714331784022914e0b1676c47a8dfb570d965192e0ff6e64b387; token=c06aaeb7-be0e-41cd-800f-0e120c2cc37e; UNTYXLCOOKIE="dXNlci5pY3ZlLmNvbS5jbnx8OTBmM2MxNDdmMzVjY2Q1YjQyY2VmOTRkMGI1ZmNiNTZ8fHdqazA5MjE1N3x8emh6ag=="; learning-course=402883e484ed33dc0184f1bafe7414a2_1754b2c1a83f4268a668e959b9d3941a___; SERVERID=16f30ddb1f23abc6369b5e279368fe9f|1671433450|1671413934',
    'Content-Type': 'application/json',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
}

# for key, value in init_mooc.get_user_all().items():
#     username = key  # 账号
#     password = value  # 密码
#     a = init_mooc.login(name=username, password=password)
    # header[
        # 'Cookie'] = f'JSESSIONID={a[4]}; aliyungf_tc=2fc0927f5a3ee5d612d75f5690676ab1366280ad5c6a2dc2aa3d1b76283c9f66; JSESSIONID=59CE88C8727A464FFA345A6758817E7F.learnspace_kfkc_aliyun; _abfpc=f26831421fa2dbe36317aa541ed619c05460effe_2.0; cna=f39af516d46dc05b2480a382baddeb0d; UNTYXLCOOKIE=dXNlci5pY3ZlLmNvbS5jbnx8MWRjZjNmMWY3OTI3NjM2MTVmYmNjM2Q3MDlmMjBhNDN8fDEzMjA2MjY5ODA0fHx6aHpq; learning-course=ms32amyox4hk6j6arvwmra_1754b2c1a83f4268a668e959b9d3941a___; _uid=d2b7a2af-4691-4a84-b203-65ecfcab3e22; token={a[0]}; alicfw=3124608875%7C2125642936%7C1328233664%7C1328232708; alicfw_gfver=v1.200309.1; jwplayer.volume=50; acw_tc={a[1]}; SERVERID={a[2]}'
    # header['Cookie'] = 'webtrn_cms=085401849537d69cc5716d58e7ca205b; whatysns=751f50efbd43e9d7505ebdaa9ac85ff3; webtrn=9eb19412ac0dbc2ebe3eccd20fd6e9c6; _abfpc=f26831421fa2dbe36317aa541ed619c05460effe_2.0; cna=f39af516d46dc05b2480a382baddeb0d; _uid=465596ae-2b2a-4f73-abf7-2e998c2fd451; token=17b59daf-1b58-439e-bc2a-6e3f1322462d; acw_tc=76b20f8516713413351382620e65fc7db251c85f9f886c556e4ffbe610487a; JSESSIONID=FA2C5D34879521AC288D6CD2AFA4CBD4; SERVERID=f25cd604b9c4c08dc3b80e49f8c85d21|1671341938|1671244553'
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
