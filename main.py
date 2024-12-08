#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/8 16:22
# @Author  : 冉勇
# @Site    : 
# @File    : main.py
# @Software: PyCharm
# @desc    :
import subprocess


def run_scripts():
    # 并行运行脚本
    process1 = subprocess.Popen(['python', 'StartWork.py'])
    process2 = subprocess.Popen(['python', 'StartWork1.py'])
    process3 = subprocess.Popen(['python', 'StartWork2.py'])
    process4 = subprocess.Popen(['python', 'StartWork3.py'])
    process5 = subprocess.Popen(['python', 'StartWork5.py'])

    # 等待两个进程都完成
    process1.wait()
    process2.wait()
    process3.wait()
    process4.wait()
    process5.wait()


if __name__ == '__main__':
    run_scripts()
