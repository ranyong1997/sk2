# -*- coding: utf-8 -*-
# @Time : 2021/11/2 16:41
# @Author : Melon
# @Site : 
# @Note : 
# @File : StartWork.py
# @Software: PyCharm
import time
import pandas as pd
import NewMoocMain.init_mooc as NewMoocInit
from NewMoocMain.log import Logger
from utils.bot_util import WxWebhookNotify
from utils.log_util import logger as log

logger = Logger(__name__).get_log()

# ****************************************** 配置 ******************************************
# 数据文件
input_file = 'data/可用账号.csv'

# 通知机器人
WEB_HOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a22cd5a6-ec18-414f-86f6-e4f3c3174b42"

# 课程ID
course_id = '9edbaab4450d467aa1fc917d39d0f6be'

# 讨论内容
topic_content = '#好#加油#积极响应'


# ****************************************** 主处理函数 ******************************************
def process_csv_logins(input_file, course_id, topic_content):
    try:
        # 开启机器人
        wn_webhook = WxWebhookNotify(WEB_HOOK)

        # 读取CSV文件
        df = pd.read_csv(input_file)

        # 检查所需列是否存在
        required_columns = ['username', 'password']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"CSV文件中缺少 '{col}' 列")

        # 如果没有状态列，则添加状态列
        if 'status' not in df.columns:
            df['status'] = ''
        # 显式转换状态列为object类型
        df['status'] = df['status'].astype(str)
        # 创建一个新的DataFrame来存储更新后的数据
        updated_df = df.copy()

        # 计算总账号数和已完成账号数
        total_accounts = len(df)
        completed_accounts = len(df[df['status'] == '已完成'])

        for index, row in df.iterrows():
            username = str(row['username'])
            password = str(row['password'])
            name = str(row['name'])
            # 跳过已完成的记录
            if row['status'] == '已完成':
                log.info(f"跳过已完成的用户: {name} | 账号:{username} | 进度: {completed_accounts}/{total_accounts}")
                continue
            log.info(f"处理用户名的登录:{name} | 账号:{username} | 进度: {completed_accounts}/{total_accounts}")

            try:
                NewMoocInit.run(
                    username=username,
                    password=password,
                    topic_content=topic_content,
                    jump_content='',
                    type_value=2,
                    course_id=course_id
                )
                # 更新状态为已完成
                updated_df.at[index, 'status'] = '已完成'
                completed_accounts += 1

                log.info(f"完成的姓名:{name} | 账号:{username} | 进度: {completed_accounts}/{total_accounts}")
                wn_webhook.send_msg_markdown(
                    f"""
            **刷课Bot**
课程ID: `{course_id}`
姓名: `{name}`
账号: `{username}`
进度: `{completed_accounts}`/`{total_accounts}`"""
                )
            except Exception as e:
                updated_df.at[index, 'status'] = f'错误：{str(e)}'
                log.error(f"处理 {name} | 账号:{username} 时出错: {e}")
            # 保存进度
            updated_df.to_csv(input_file, index=False)
            print("本次程序运行完成，正常结束。")
        log.info(f"CSV所有账号处理完成. 总账号: {total_accounts}, 已完成: {completed_accounts}")
        return updated_df
    except Exception as e:
        log.exception(f"处理CSV时发生错误:{e}")
        return None


if __name__ == '__main__':
    time.sleep(1)
    print('\n')
    try:
        process_csv_logins(input_file, course_id, topic_content)
    except Exception as e:
        logger.exception(e)
