from bdb import set_trace
import requests
from bs4 import BeautifulSoup
import re
import os
import json
import sys

# 课程id
courseId = '1754b2c1a83f4268a668e959b9d3941a'
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'Accept-Encodign': 'gzip, deflate, br',
    'Cookie': ''
}
header['Cookie'] = 'JSESSIONID=39852212283062F9AB82381A81900347; aliyungf_tc=bb2d5b8e81cbdbbb6a197f82ad4b7819d2d7de9e7876ecb3bd6df25f3e36f6e3; _uid=a4c90428-db62-4781-9b7b-0ac45e61bf47; rest_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dpbklkIjoiMTMyMDYyNjk4MDQiLCJzaXRlQ29kZSI6InpoemoiLCJ1c2VyX25hbWUiOiIxMzIwNjI2OTgwNCIsInBob3RvIjpudWxsLCJzdUlkIjoibXMzMmFteW94NGhrNmo2YXJ2d21yYSIsImF1dGhvcml0aWVzIjpbIlJPTEVfU1RVREVOVCJdLCJjbGllbnRfaWQiOiIyMTA4MTg3NzE4IiwidHJ1ZU5hbWUiOiLlhonli4ciLCJzdWRJZCI6Im1zMzJhbXlveDRoazZqNmFydndtcmEiLCJyb2xlQ29kZSI6IjAiLCJzY29wZSI6WyJhbGwiXSwicm9sZU5hbWUiOiLlrabnlJ8iLCJleHAiOjE2NzE3NzkwMTgsImp0aSI6ImM1NmFmYzZjLTFjMDMtNGViNy05NGNiLWM2YzhjMjlmNzgxMCJ9.S9bFVfmqsX0JDW4gmxXtgQPIJzeLEoURzY4ITH85AqTwKmKTzp3cpMoPboexe71Bx2hLMVHLKmE9cRMx_7BYkg5euCtgZUG5QoW1_L1iJhQ6HK2Jf2g-W4hqfxPd4V9mpdbjYSBCFFiQdTzQ-rFvXfcgYYIDQVR-kVYpbJMGhbaPDu_KfrGLFL9mwn8e6d31MRRWUVd-MmpXwzIwecZh5SzclbSKiBZbmRU0emfsKvSicmE4WvDqmwlZTwgXnOpG1Za-kbrK9xay_CBslbI-GA7vF8qeyimYloPGhKF_xvn0Pc_S0drlAQ4q9_sS60eRz1BV4hGEVgKTl6rG-LwUXA; h_courseId=1754b2c1a83f4268a668e959b9d3941a; platform_flag=learnspace; _abfpc=214f13227d1bb5c000032efdf10dbf74c0b26699_2.0; cna=ce3b72a7124523cfdc0da5523173753c; token=55f32f75-dd15-4622-a842-141528bf1bba; UNTYXLCOOKIE="dXNlci5pY3ZlLmNvbS5jbnx8YTFjMDUwMTM4MzQ0ZGM5OTQyMDdiMzA5MjA1MGM2YjF8fDIxMTUxMzkwMTV8fHpoemo="; learning-course=402883ab84ed29d60184edc4d5ec0231_c3f008fd84e649a78bdb4e274a079e4d___; jwplayer.volume=50; alicfw=619652209%7C2126371654%7C1328233921%7C1328232936; alicfw_gfver=v1.200309.1; acw_tc=707c9f6616705713566573978e30e6a266991fb10f8a1af324e0290f39b11e; SERVERID=db0581f1d84e519339e911738e844a10|1670571376|1670569410'

# 获得limitId
res = requests.get(
    url='https://course.icve.com.cn/learnspace/learn/learn/templateeight/index.action?params.courseId=1754b2c1a83f4268a668e959b9d3941a___',
    headers=header)
patter = re.compile('limitId.*;')
try:
    limitId = patter.search(res.content.decode()).group().split('"')[1]
except:
    print('\033[31m获取limitId失败，检查Cookie\033[0m')
    exit()

# 获得itemId
res = requests.get(
    url='https://course.icve.com.cn/learnspace/learn/learn/templateeight/courseware_index.action?params.courseId=1754b2c1a83f4268a668e959b9d3941a___¶ms.templateType=8¶ms.templateStyleType=0¶ms.template=templateeight¶ms.classId=¶ms.tplRoot=learn',
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
        'params.courseId': courseId,
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
        end = start + 10
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
        'courseId': '1754b2c1a83f4268a668e959b9d3941a___',
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
