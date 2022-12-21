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


class Login:
    def __init__(self):

        self.header = {
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
        self.s = requests.Session()
        self.Cookie = ''

    def login(self, name, password):
        login_fail_num = 0
        print(f'正在登录账号:【{name}】')
        while login_fail_num < 6:
            data = {
                "userName": name,
                "password": password,
                "type": 1
            }
            try:
                res = self.s.post(url=LOGIN_SYSTEM_URL, json=data, headers=self.header)
                cookies = res.cookies
                cookie = requests.utils.dict_from_cookiejar(cookies)
                # print(res.json())  # {'code': 200, 'msg': 'ok', 'data': '2e57fa48-7276-4509-91fc-c98bc028778e', 'sign': None}

                if res.json()['code'] == 200:
                    print(f"==================== 登陆成功:【{str(name)}】 ====================\n")
                    print(self.s.cookies.set('Cookie', cookie))
                    return self.s.cookies.set('Cookie', cookie)
                #     获取limitId

                else:
                    print("\t\t--->", res.json()['msg'])
            except Exception as e:
                login_fail_num += 1
                print("获取token失败: \n{0}".format(e))
        raise Exception(f"账号:{str(name)} 登录失败")

    def get_user_all(self):
        """读取csv至字典"""
        with open("data/data.csv", "r", encoding='gbk') as csvFile:
            # with open("../data/data.csv", "r", encoding='gbk') as csvFile:
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
    login = Login()
    for key, value in login.get_user_all().items():
        username = key
        password = value
        login.login(name=username, password=password)
