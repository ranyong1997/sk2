#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/18 22:22
# @Author  : 冉勇
# @Site    : 
# @File    : demo.py
# @Software: PyCharm
# @desc    :
import os
import random
from bdb import set_trace
from time import sleep
from common import init_mooc
import requests
from bs4 import BeautifulSoup
import re
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
header[
    'Cookie'] = 'JSESSIONID=B39C70F71A9B138AB8920AC997D1E4D0; aliyungf_tc=2fc0927f5a3ee5d612d75f5690676ab1366280ad5c6a2dc2aa3d1b76283c9f66; JSESSIONID=59CE88C8727A464FFA345A6758817E7F.learnspace_kfkc_aliyun; _abfpc=f26831421fa2dbe36317aa541ed619c05460effe_2.0; cna=f39af516d46dc05b2480a382baddeb0d; _uid=d2b7a2af-4691-4a84-b203-65ecfcab3e22; jwplayer.volume=50; learnspace_taolun=0be5d730b745f30657fe2554fde22ded; sid=f03db508-22eb-4047-9238-88db953fa0da; h_courseId=1754b2c1a83f4268a668e959b9d3941a; platform_flag=learnspace; ST="BnD3eMizlU4AV0ueX929Vpgq1EF2EXdus64ZJEfmlAI="; rest_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dpbklkIjoiMTMyMDYyNjk4MDQiLCJzaXRlQ29kZSI6InpoemoiLCJ1c2VyX25hbWUiOiIxMzIwNjI2OTgwNCIsInBob3RvIjpudWxsLCJzdUlkIjoibXMzMmFteW94NGhrNmo2YXJ2d21yYSIsImF1dGhvcml0aWVzIjpbIlJPTEVfU1RVREVOVCJdLCJjbGllbnRfaWQiOiIyMTA4MTg3NzE4IiwidHJ1ZU5hbWUiOiLlhonli4ciLCJzdWRJZCI6Im1zMzJhbXlveDRoazZqNmFydndtcmEiLCJyb2xlQ29kZSI6IjAiLCJzY29wZSI6WyJhbGwiXSwicm9sZU5hbWUiOiLlrabnlJ8iLCJleHAiOjE2NzI0ODA0OTUsImp0aSI6IjhhMzEwYmNhLTBhOTItNGJkNi1iNTljLWZiMDYxOTY5ZTMxMiJ9.C1uheB06kxBlKLzSzF_3KMVftFo_k8sw422qmGVVgbP4uf9zg8OKcXOT15-eQG4cNYHH5kqYnaFpNsdovsL1ulliMtT1STlcGy3Ffxy93RfE1jueEKyzxBdGecbueUE1nS4z8B52ZCXHgxF0sgs8YxzsKW8pdd1BqIkgdnCfAitsZMYoC5r2eUHZck8l0EM9avhWErGePnzDIOLeGw_QIbTE78Xjk6W-CRm95WDXqbfr0X9DuGG56VQEcX02AXupB3-Ige6pPJJq8x4kovSHT5ysrWbc8goOY44hNYRVly3ePflY3m1V6P85kAsxKs4xhJOfy_-KVwrNMUCBZxDXRw; token=1531fdf6-d778-46ae-aa05-e6e8575fd543; UNTYXLCOOKIE=dXNlci5pY3ZlLmNvbS5jbnx8MWRjZjNmMWY3OTI3NjM2MTVmYmNjM2Q3MDlmMjBhNDN8fDEzMjA2MjY5ODA0fHx6aHpq; learning-course=ms32amyox4hk6j6arvwmra_1754b2c1a83f4268a668e959b9d3941a___; acw_tc=707c9f6116713737060972064e791e3579aece5f89f190a7ad8530665e75fb; SERVERID=16f30ddb1f23abc6369b5e279368fe9f|1671374191|1671244551'

start = 0
end = 0
while True:
    start = end
    end = start + 20
    cmd = os.popen('node ./test.js %s %s %s' % (itemid, start, end))
    studyrecord = cmd.read().strip('\n')
    print(studyrecord)
    cmd.close()
    data = {
        'limitId': itemid,
        'studyRecord': studyrecord
    }
    res2 = requests.post(
        url='https://course.icve.com.cn/learnspace/course/study/learningTime_saveVideoLearnDetailRecord.action',
        headers=header, data=data)
    print(res2.json())
