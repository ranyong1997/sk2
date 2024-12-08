#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/8 16:22
# @Author  : 冉勇
# @Site    : 
# @File    : main.py
# @Software: PyCharm
# @desc    :
import concurrent.futures
import subprocess


def run_script(script_name):
    subprocess.run(['python', script_name])


def run_scripts():
    scripts = ['StartWork.py', 'StartWork1.py', 'StartWork2.py', 'StartWork3.py']

    # 使用ThreadPoolExecutor（如果是IO密集型任务）
    # 或者ProcessPoolExecutor（如果是CPU密集型任务）
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 提交所有脚本执行任务
        futures = [executor.submit(run_script, script) for script in scripts]

        # 等待所有任务完成
        concurrent.futures.wait(futures)


if __name__ == '__main__':
    run_scripts()
