#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/20 11:00
# @Author  : 冉勇
# @Site    : 
# @File    : demo.py
# @Software: PyCharm
# @desc    :
from selenium import webdriver  # 用来驱动浏览器的
from selenium.webdriver import ActionChains  # 破解滑动验证码的时候用的 可以拖动图片
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys  # 键盘按键操作
from selenium.webdriver.support import expected_conditions as EC  # 和下面WebDriverWait一起用的
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
import time

option = webdriver.ChromeOptions()
# 设置此属性，浏览器不会弹请禁用开发者模式的弹框
option.add_experimental_option('useAutomationExtension', False)
# 设置开发者模式启动，该模式下webdriver属性为正常值，如果不设置，某些网站会检测出window.navigator.webdriver属性，该属性是会被网站认为是爬虫程序，因此隐藏该属性
option.add_experimental_option('excludeSwitches', ['enable-automation'])

driver = webdriver.Chrome()

try:
    wait = WebDriverWait(driver, 10)
    # 1、访问地址
    driver.get(
        "https://icve-mooc.icve.com.cn/cms/")
    # # 2、查找输入框
    # input_tag = wait.until(
    #     # 调用EC的presence_of_element_located()
    #     EC.presence_of_element_located(
    #         # 此处可以写一个元组
    #         # 参数1: 查找属性的方式
    #         # 参数2: 属性的名字
    #         (By.ID, "userName")
    #     )
    # )
    input_tag = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginBtn"]'))).click()   # 点击登录
    input_tag = wait.until(EC.presence_of_element_located((By.ID, "userName"))).send_keys('13206269804')    # 输入账号
    input_tag = wait.until(EC.presence_of_element_located((By.ID, "password11"))).send_keys('Ranyong_520')  # 输入密码
    input_tag = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="isTy"]'))).click()   # 点击同意
    input_tag = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "dl"))).click()   # 点击登录
    time.sleep(3)
    input_tag = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="moocStuBtn"]'))).click() # 点击我的MOOC
    time.sleep(3)
    input_tag = wait.until(WebDriverWait((By.CLASS_NAME, "course-name")))  #
    input_tag = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="openingData"]/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/a[3]'))).click()
    time.sleep(2)
    # 获取cookie
    dictCookies = driver.get_cookies()
    # 获取每个cookie
    cookies = [item['name'] + '=' + item['value'] for item in dictCookies]
    # 拼接cookie
    cookieStr = '; '.join(cookies)
    print(cookieStr)
finally:
    driver.close()
