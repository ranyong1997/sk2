#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/21 15:45
# @Author  : 冉勇
# @Site    :
# @File    : demo1.py
# @Software: PyCharm
# @desc    :
import requests

# 网址
BaseURL = "https://course.icve.com.cn"
# 课程id
courseId = "1754b2c1a83f4268a668e959b9d3941a"
# 登录网址
LOGIN_SYSTEM_URL = "https://sso.icve.com.cn/data/userLogin"


def login():
    session = requests.session()  # 实例化session对象
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'Accept-Encodign': 'gzip, deflate, br',
        'Cookie':'p_h5_u=0A34EA57-33D4-4BBE-AA29-498BCCF3D3DB; selectedStreamLevel=FHD; dumaScrollAreaId_11CookieName=837; JSESSIONID=FCA373F89A72C2EF4558902B950CC5CF; _abfpc=1d466485af98ed5add63780f7b4ace668b0502d5_2.0; cna=d0ed267474e1abe89b79166eab802eac; ssxmod_itna=eqAxBC0Qq7qWuDBPr97QGQtIO7D0DCq2W7nDDsqtrDSxGKidDqxBWWl2He9v9vhiAClo2oDgnTP0Nfb9l74h=5llWeDHxY=DUpDTeqrDeW=D5xGoDPxDeDAQKiTDY4DdjpNv=DEDeKDRDAQDzwd/4h6z/G=DI3iDmTLDx7t9ITL5qeG2DGUeIkGx7qDMIeGXC0nPxDUTTZwMIMuixYPWQk0xxBQD7di9DYoUneDHzdN8ghDW0Gm10iQ5WOxqt+G+7Gme/RhA/GGi7xqLdYeGYr+1b5DAYDj1CiD=; ssxmod_itna2=eqAxBC0Qq7qWuDBPr97QGQtIO7D0DCq2WYikIqqhDlphxjb+xj8drKju5QqL3QD6mYmtQjBPeuDwjW3jAqvee4Yv8eCKdYcftOKCDXesC+iF4OqlKUycajU8B1dQ2BWuHqOQfcS6q/24ax9DdEc5C2mKCYIyGZY7GPhrOWp74jCvGErqCPKwh+pvGq0YN+Rqa0pAGW3BaQfHGL9bx0WkCclYaAF5QlC2hDH3202n7OIeTKAjiQO8F6cIhNgLoDQFODjKD+a95=nxbMAQOYpDK4D=; _uid=10b64d0f-5e25-46df-aa14-9e89b0f28624; sid=632519b2-2297-437e-8306-01388da15d65; h_courseId=1754b2c1a83f4268a668e959b9d3941a; platform_flag=learnspace; alicfw=742397870%7C2123194196%7C1328233537%7C1328232896; alicfw_gfver=v1.200309.1; rest_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dpbklkIjoiMTgwNzAyNTU1NDgiLCJzaXRlQ29kZSI6InpoemoiLCJ1c2VyX25hbWUiOiIxODA3MDI1NTU0OCIsInBob3RvIjpudWxsLCJzdUlkIjoiNDAyODgzZTY4NGU4MzU2ZDAxODRlYTg0NGEyYjA2MTAiLCJhdXRob3JpdGllcyI6WyJST0xFX1NUVURFTlQiXSwiY2xpZW50X2lkIjoiMjEwODE4NzcxOCIsInRydWVOYW1lIjoi5byg5YeM5q-FIiwic3VkSWQiOiI0MDI4ODNlNjg0ZTgzNTZkMDE4NGVhODQ0YTJiMDYxMCIsInJvbGVDb2RlIjoiMCIsInNjb3BlIjpbImFsbCJdLCJyb2xlTmFtZSI6IuWtpueUnyIsImV4cCI6MTY3MjgwNTk3NiwianRpIjoiZjMzMWRiMzQtODBlOC00ZTM4LWIxZDEtNzY5YmJkODUxNDQ1In0.gMNlD4BpN2GlMjKLZUxMH9fvN4WECxEWBlWUyyAnx1i87RDl_eYhPnl6ap-1j1xsEL132rZvoglfBanUc17pl-245sYmGZpCnBtsASKubzopQO_HAugG2EHo8Vbx5YIeKshtFKlV2f6zEBJrjq_gavhk0BN70Agsa3i4oLQJJUkvX2k8cF0_4pW1pSL1PM-YVVTzCP-oq01uK5X7TT5HmXDb8Rq7LSAdLkf0vIgaHifEdJ2jDHFVVrDn0YIfi9KEXME_PW_kLHlkvfm-qxpgBj93fjhVbIYDjLdw6TnAZG0Wf8i6RcHamGelsqvN5TmMwk4mv6pztZlTwCSyWOuF0g; ST="7aEHP7LJgeTSUA9NDbj5GRTBf7CDm/1onfRRUvsd2IU="; UNTYXLCOOKIE=dXNlci5pY3ZlLmNvbS5jbnx8MWRjZjNmMWY3OTI3NjM2MTVmYmNjM2Q3MDlmMjBhNDN8fDEzMjA2MjY5ODA0fHx6aHpq; learning-course=ms32amyox4hk6j6arvwmra_1754b2c1a83f4268a668e959b9d3941a___; jwplayer.volume=50; token=388a9c7e-cae9-4f81-a077-a149769904e4; SERVERID=7ddb0b35eddd98b5af4392c4e96c032f|1671610714|1671584891'
    }
    data = {
        "userName": '13206269804',
        "password": 'Test_123',
        "type": 1
    }
    res = session.post(url=LOGIN_SYSTEM_URL, json=data, headers=session.headers)
    print(res.content.decode())
    token = res.json()['data']
    data = {
        "token": token,
        "courseId": "1754b2c1a83f4268a668e959b9d3941a___",
    }
    response = session.post(url='https://course.icve.com.cn/learnspace/course/study/learningTime_queryLearningTime.action', data=data,
                           headers=session.headers)
    print(response.content.decode())


login()
