#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/5 10:51
# @Author  : 冉勇
# @Site    :
# @File    : log_util.py
# @Software: PyCharm
# @desc    : 日志工具
import os
import time
from loguru import logger
from functools import partial

# 日志路径
log_path = os.path.join(os.getcwd(), 'logs')
# 判断是否创建
if not os.path.exists(log_path):
    os.mkdir(log_path)


# 创建一个函数来动态生成日志文件路径
def get_log_path(log_type):
    return os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_{log_type}.log')


# 创建一个自定义的 sink 函数
def custom_sink(message, log_type):
    record = message.record
    if record["level"].name.lower() == log_type:
        log_path = get_log_path(log_type)
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(message)


# 为每种日志类型添加 logger
logger.add(partial(custom_sink, log_type="info"), level="INFO")
logger.add(partial(custom_sink, log_type="error"), level="ERROR")
logger.add(partial(custom_sink, log_type="warning"), level="WARNING")
logger.add(partial(custom_sink, log_type="debug"), level="DEBUG")

