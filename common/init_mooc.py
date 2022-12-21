#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/17 10:48
# @Author  : 冉勇
# @Site    : 
# @File    : init_mooc.py
# @Software: PyCharm
# @desc    :
import os
import csv
import random
import time
import base64
from io import BytesIO
import requests
from urllib import request
from http import cookiejar
import json

from requests import Request, Session

BASE_URL = 'https://sso.icve.com.cn'
base_url_ = 'https://icve-mooc.icve.com.cn'
# 登录
LOGIN_SYSTEM_URL = f"{BASE_URL}/data/userLogin"

request_session = requests.session()
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Encodign': 'gzip, deflate, br',
    'Content-Type': 'application/json',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'Referer': 'https://sso.icve.com.cn/sso/auth?mode=simple&source=2&redirect=https://icve-mooc.icve.com.cn/cms/courseDetails/index.htm?classId=0be8d630dbe5fe61a4dedc86799d3c7d',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': ''
}


def to_url(name, password):
    data = {
        "userName": name,
        "password": password,
        "type": 1
    }
    a = request_session.post(url=LOGIN_SYSTEM_URL, json=data, headers=header)
    # ulist_url = 'https://icve-mooc.icve.com.cn/learning/u/student/student/mooc_index.action'
    # res = request_session.get(url=ulist_url, headers=header)
    # print(res.text)
    # token_ = requests.post(url=LOGIN_SYSTEM_URL, json=data, headers=header)
    # code_url = f"{base_url_}/patch/zhzj/api_getUserInfo.action"
    # # https://icve-mooc.icve.com.cn/?token=ec832a0a-4aca-4cc7-88dd-33f4f8917cb7
    # code_result = requests.post(url=code_url, data=token_.json()['data'], headers=header)
    # cookiejar = code_result.cookies
    # cookiedict = requests.utils.dict_from_cookiejar(cookiejar)
    # cookie_str = json.dumps(cookiedict)
    # print(cookie_str)
    return a.json()


def login(name, password):  # 0.登录
    """
    登录
    :param name: 用户名
    :param password: 密码
    """
    login_fail_num = 0
    print(f'正在登录账号:【{name}】')
    while login_fail_num < 6:
        result = to_url(name, password)
        json_result = result['code']
        if json_result == 200:
            print(f"==================== 登陆成功:【{str(name)}】 ====================\n")
            return True
        else:
            print("\t\t--->", result['msg'])
            login_fail_num += 1
    raise Exception(f"账号:{str(name)} 登录失败")


def get_user_all():
    """读取csv至字典"""
    # with open("data/data.csv", "r", encoding='gbk') as csvFile:
    with open("../data/data.csv", "r", encoding='gbk') as csvFile:
        reader = csv.reader(csvFile)
        # 建立空字典
        result = {}
        for item in reader:
            # 忽略第一行
            if reader.line_num == 1:
                continue
            result[item[0]] = item[1]
    return result


if __name__ == '__main__':
    for key, value in get_user_all().items():
        username = key
        password = value
        login(name=username, password=password)
        # to_url(name=username, password=password)
