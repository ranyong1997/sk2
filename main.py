#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/18 22:45
# @Author  : 冉勇
# @Site    : 
# @File    : main.py
# @Software: PyCharm
# @desc    :
import os
import random
import time
from bdb import set_trace
from bs4 import BeautifulSoup
import re
import json
import sys
import requests

request_session = requests.session()
# 国际商务谈判
BaseURL = "https://course.icve.com.cn"
# 考试url
ExamURL = "https://spoc-exam.icve.com.cn"
# 课程id
courseId = "1754b2c1a83f4268a668e959b9d3941a"
# 评价课程id
subjectId = "89008fd3260bd552a84da2fdc2ebd3a8"
# 登录
LOGIN_SYSTEM_URL = f"{BaseURL}/data/userLogin"
# 评价内容
content = ['非常好', '非常非常的好', '课程精彩，通熟易懂', '非常好 课程里的知识很丰富']
# 灌水内容
Irrigation_content = [
    '国际商务谈判，是国际商务活动中不同的利益主体，为了达成某笔交易，而就交易的各项条件进行协商的过程。谈判中利益主体的一方，通常是外国的政府、企业或公民（在现阶段，还包括香港、澳门和台湾地区的企业和商人），另一方，是中国的政府、企业或公民。 国际商务谈判是对外经济贸易工作中不可缺少的重要环节。在现代国际社会中，许多交易往往需要经过艰难繁琐的谈判，尽管不少人认为交易所提供的商品是否优质、技术是否先进或价格是否低廉决定了谈判的成败，但事实上交易的成败往往在一定程度上取决于谈判的成**与否。在国际商务活动中，不同的利益主体需要就共同关心或感兴趣的问题进行磋商，协调和调整各自的经济利益或政治利益，谋求在某一点上取得妥协，从而在使双方都感到有利从而达成协议。所以，我们可以说，国际商务谈判是一种对外经济贸易活动中普遍存在的一项十分重要的经济活动，是调整和解决不同国家和地区政府及商业机构之间不可避免的经济利益冲突的必不可少的一种手段。',
    '结了有关幽默语用,暗含和闪避语用以及身份构建策略在国际商务谈判中的运用,根据研究我们发现,幽默语用主要运用于在谈判中发现冲突之后,用以缓解冲突的方法,然后说明了闪避式回应的特点和作用,最后我们通过成东青的精彩会话,讲述了身份构建中人称变化对于商务谈判的影响.在国际商务谈判中,转化人称可以加剧冲突或缓解冲突.在国际商务谈判中如果巧妙运用了身份构建原则,会让谈判气氛巧妙地朝着我们希望的方向微妙的转化,在对方没察觉到的情况下就占据了主要优势。谈判伊始，佟大为用一盒月饼幽默开场，让谈判气氛不那么紧张。',
    '习了商务谈判，我懂得了，在商务谈判中，开局、沟通、谈判的技巧、情 报因素、时间的把握、还有谈判的策略都是很重要的。没学习商务谈判之前，其 实我们每个人的谈判能力也各不相同，有的同学比较善于沟通，但是有的同学比 较内向，很少和陌生人沟通交流，对于这种同学来说，学习这门课程首先就要联 系说话，甚至是和陌生人说话。我觉得我是这第二类人，还是需要进行培养，锻 炼。谈判艺术就是运用心理学，通过对人性的充分了解，察言观色。听话听声， 使原本紧张的商务谈判在生动轻松的气氛中顺利进行，并且在不露痕迹之中让对 方愉快地接受你的主张，让对方不合理的主张消于无形，而合理的主张则得到你 非常郑重的肯定。',
    '在国际商务谈判中谈判者应该努力了解并接纳对 方的文化，并努力使自己被对方接受。文化差异主 要在沟通过程、伦理与法制、决策机构与决策权限 等方面对国际商务谈判产生影响。为在国际商务谈 判中顺利跨越由于文化差异所引起的障碍，实现双 赢的谈判目标，可采取如下应对策略：选择一个深 谙双方文化的翻译；正视文化差异，做好充分的准 备；树立跨文化谈判意识，正确处理文化差异。',
    '1. 对文化的理解 　　文化是通过社会关系相互传递从而被大家都认同的行为特征和价值观，它包括了知识、信仰、艺术、道德、法律、习俗等等。文化的概念广而且复杂，但它实际上包括了人们生活的每一方面，涉及到人们精神上和生理上的各种需要。 　　2. 中西方文化差异产生的原因 　　国际商务谈判中由于谈判人员来自的地域不同，民族、经济、政治、观念及宗教有极大的差别，而这些方面都是造成世界文化多元性的原因。 　　（1）地域差异 　　地域差异指不同的地理区域由于地理环境、经济发展和传统习惯等的差异，人们往往有着不同的语言、生活方式和爱好，而这些会影响他们的行为习惯。 　　（2）民族差异 　　民族差异是指不同的民族群体在长期的发展过程中，形成了各自的语言、风俗、爱好和习惯。他们在饮食、服饰、居住、节日、礼仪等物质和文化方面各有其特点。就拿我国的汉族和美国来说，我们汉族性格温顺，是典型的农耕民族特征。美国人的性格开朗大方，待人热情，从而导致了美国人在饮食、服饰居住、节日、礼仪等物质和文化生活方面与我国汉族都相差甚大。',
    '商务谈判中的风险防范直接影响谈判收益的大小和谈判收益的最终实现问题。它是确保谈判成**的关键因素之一，谈判人员必须采取各种风险防范措施，确保己方利益，减少经济损失。 风险防范意识 谈判各方在商务谈判中始终面临着各种风险，因此，谈判人员必须时刻具有风险防范识。在谈判准备阶段的商务调研活动，不仅要调查、估计双方能否达成协议（可能性），还要分析达成协议之后能否执行（可行性）：不仅要了解对方的企业性质、主管单位、经营状况、资本实力、信用和履约能力，还要了解产品质量、销售状況、市场豁求和国家政策等等。例如，当前购买保健药品，在市场需求方面，不仅要了解社会对该产品的需求量、需求潜力，还要了解己方销售地区的购买能力。一般而言，收入水平越高，购买力愈强;收入水平越低，购买力愈弱。所以，低收入地区较高收入地区销售保健药品的风险要高。在国家政策方面，今年下半年医疗制度改革具体措施即将出台．改革的总趋势是个人在一般医疗费用中所支付的比例上升，在收入一定的情况下，保健药品的购买力将下降。因此，个人医疗费用上升的幅度对保健药品的购买力影响很大。为了降低风险，保健药品经销商应控制购货数量，降低风险，静观政策变化。（此文所写时间较早，这一例子不一定符合当前实际状况）在谈判过程和签订协议阶段要慎重对待文字表述，使之体现对己方的有利性。书面谈判和谈判协议中关键性概念的表述一定要考虑履约情况。',
    '商务谈判重要性一直以来，谈判无时不有无处不在。大道国家会谈小到个人切磋协商，谈判已经渗透到，现代，社会，政治，经济，军事，文化，外交等各个领域之中，成为人与人之间组织与组织之间，国家与国家之间相互交流沟通，达成共识不可或缺的工具。',
    '不是。报价策略：在谈判之前，我方就提前拟定三种的报价方案，包括：高、中、低，三个不同的报价。其中高价是理想价位，大约可以定在去掉**之外，利润率定于30%-60%之间；中价一般定在利润率为15%-30%之间；低价一般定在利润率5%-15%之间。讨价策略：这是基于我方报价之后，对方的讨价。一般情况下，当我方报价之后，对方一般不支无条件地接受我方的发盘。而是会提出重新报价，或者再询价，让我方做出一些降价让步。还价策略：从我方的报价，引至对方讨价，再到我方的还价。这是一场拉锯战，比的智慧与毅力。还价之时，是在对方讨价后，我方做出的一个适当提高价格的过程',
    '1、充分了解《合同法》及其相关法律，行政法规及司法解释的规定《合同法》规定的主要内容有：合同的含义，订立合同的基本原则（自愿、公平、诚实、信用、合法等）合同订立的程序，合同的有效与无效，合同履行的原则、抗辩权、中止履行、代位权、撤销权等。合同变更和转上的条件与程序，合同终止的事由、程序、条件等，违约责任，合同的具体种类（买卖合同、赠与合同、借款合同、租赁合同、技术合同、委托合同）等，当事人了解了合同及其相关法律法规的规定，有利于详细，合法地订立合同条款，避免因合同条款的漏洞或无效而引起合同**。2、调查了解对方当事人的履约能力等状况，订立合同之前事先调查了解对方当事人的资信状况是非常重要的，这样可以有效地避免欺诈**和违约**。调查了解资信状况主要指查验对方当事人的营业执照，了解对方当事人的信誉程度等。如果对方当事人资信状况良好，则合同订立后履约就可能得到保证；如果对方当事人资信状况不佳、商业信誉不好，甚至濒临破产境地，自然欠缺或没有足够的履约能力，与这样的当事人签订合同就会有很大的风险，合同订立后也会产生**。当事人在调查了解对方当事人的资信状况的同时，还应了解签约对方的主体资格，即在合同上签字的人是否具备签署合同的资格。3、精心准备合同条款，合同条款是当事人履行合同的依据。为避免因条款的不完备或歧义而引起合同**，当事人应精心准备合同条款。除了法律的强制性规定外，其他合同条款都可以在协商一致基础上进行约定。法律给予了合同当事人订立合同的充分自由，当事人应详细约定，尤其是关于合同标的（包括名称、种类等）、数量、质量、价款或者报酬、履行期限、履行地点、履行方式、违约责任（违约金或违约损失赔偿额的计算方法等）解决争议的方法等合同主要之条款。此外、根据合同性质或当事人需要特别约定的条款也应详细规定。']

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'Accept-Encodign': 'gzip, deflate, br',
    'Cookie': 'JSESSIONID=24866ADEE72AA45A42AAD89A3FFB8593; aliyungf_tc=2fc0927f5a3ee5d612d75f5690676ab1366280ad5c6a2dc2aa3d1b76283c9f66; JSESSIONID=59CE88C8727A464FFA345A6758817E7F.learnspace_kfkc_aliyun; _abfpc=f26831421fa2dbe36317aa541ed619c05460effe_2.0; cna=f39af516d46dc05b2480a382baddeb0d; _uid=d2b7a2af-4691-4a84-b203-65ecfcab3e22; jwplayer.volume=50; learnspace_taolun=0be5d730b745f30657fe2554fde22ded; sid=f03db508-22eb-4047-9238-88db953fa0da; h_courseId=1754b2c1a83f4268a668e959b9d3941a; platform_flag=learnspace; UNTYXLCOOKIE=dXNlci5pY3ZlLmNvbS5jbnx8MWRjZjNmMWY3OTI3NjM2MTVmYmNjM2Q3MDlmMjBhNDN8fDEzMjA2MjY5ODA0fHx6aHpq; learning-course=ms32amyox4hk6j6arvwmra_1754b2c1a83f4268a668e959b9d3941a___; rest_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dpbklkIjoiMTMyMDYyNjk4MDQiLCJzaXRlQ29kZSI6InpoemoiLCJ1c2VyX25hbWUiOiIxMzIwNjI2OTgwNCIsInBob3RvIjoibnVsbCIsInN1SWQiOiJtczMyYW15b3g0aGs2ajZhcnZ3bXJhIiwiYXV0aG9yaXRpZXMiOlsiUk9MRV9TVFVERU5UIl0sImNsaWVudF9pZCI6IjIxMDgxODc3MTgiLCJ0cnVlTmFtZSI6IuWGieWLhyIsInN1ZElkIjoibXMzMmFteW94NGhrNmo2YXJ2d21yYSIsInJvbGVDb2RlIjoiMCIsInNjb3BlIjpbImFsbCJdLCJyb2xlTmFtZSI6IuWtpueUnyIsImV4cCI6MTY3Mjc1MDY3NywianRpIjoiODE0NzZlMTMtMmU1YS00ZDBlLTk5MmMtY2M4NDc4ZjgzNjlmIn0.YDLYhcmxUWVZEJCYZHKea4OARmPQI0VDJy4EJ81zFvvG1BKbErxpSPQX2niMhGlYrPSdLFx97haf5Xtg2L8T-Qn5XTMiWAgtSwelP9r1d308tHw9L3H1wnXZjMfp3Pl6X2Uh3UlDtZMzVpEFlvlA8uiI4OyYYf-1HJ8ibcvUAuzwuUI_DdzYjIeosrH3ojwZebxjoBNUV_HmObaZzDRCjTXbuk98EsKm4N2Zk1V4VsVJ4ZmMWVKv3NvChBZuhDhm6wRCohxNfXjrJwqPQ2fLi5pHi6QSw8Gr7NmSxarOTJUQb2G-Q5G5wxp8NFyq6WzsJx_KH5HdLfvvlc9GGv5SnA; ssxmod_itna=QqGxnDRDcDg0iQNGHIgq7qBIvR7KsOQqbY7bNDl2oxA5D8D6DQeGTb2KDBiWbjiiHIW3Yi4qXae3USbb1qKUYaNebDneG0DQKGmDBKDSDWKD9mAT4GGfxBYDQxAYDGDDPcDGqsg2D7OzzM=9CHZ0sDlezwZPCuODDUlDhwPFFp=HQup2Pr4i3EnKDXP3Dv2yCG6cw9PYs13rxEWGeapI4LQ0qS0GxK1hxbmrK3lMxsDM5HQG44o43n/QxDDcqeQx0YYD; ssxmod_itna2=QqGxnDRDcDg0iQNGHIgq7qBIvR7KsOQqbY7D618ChD05bx03Nee2YDB0in8kTLAHQkBCZ7BjQ6t/To67Ob9SbQf7F+7I4Eq+6ZhRUrI1OOQqChIKZans1tTf=D6CC0Dhcp5kUBR5vdd08rXDpfixaRiqXf0wKWXs3M5Et32HUhQu7TEjejjUj45uzWok/nQo=MbInnu3rSfjeknH5Cd9/qvOlLPKWkiiIOyxs7HL3ThImf+O7kW891D+qbx2/1iCS4xaHYK2WRqXfn9tyIgBU40bojcKu+rP1yW/Spt9hvZUnLBUWZhjlXsrdsPLRDwuYPjaodEowpExrpVhIdorPKLtO09aXqpN=av6QvADEvQvynUAYRqhI/lrN4oBh3BgI5n4VgfRa05Z5f033EU1cmpBqEjd/prhRR19+WRtpfEs2XrhKaOW9xYW1Nz14DQK4iDqG9E3RQY09DdnjeOEh7/0iXhQAh=Qi5F+p+k=BPxD08DiQzCDqmhxYD==; ST="Pg/FThCSwk3Qirn22EVmk3+g+inhOFCSbvOmiBgaJ6rkdCdZnHpfPw=="; token=73c063a3-2a91-4c65-9808-d34108ab6ad6; alicfw=477608625%7C2123118199%7C1328233664%7C1328233315; alicfw_gfver=v1.200309.1; acw_tc=76b20f8f16716322626954214e2634dfd4a1d68f75185e7ab47aa16004a729; SERVERID=20157a9178d6239df0e552bdb97bd90e|1671633275|1671244551'
}

# 获取limitId
res = requests.get(
    url=f'{BaseURL}/learnspace/learn/learn/templateeight/index.action?params.courseId={courseId}___',
    headers=header)
# print(res.text)
patter = re.compile('limitId.*;')

# # 获取userId
# res1 = requests.get(
#     url='https://course.icve.com.cn/taolun/learn/courseTopicAction.action?action=item&itemId=402883a983232378018329f7892a1ddc&courseId=1754b2c1a83f4268a668e959b9d3941a&ssoUserId=wjk092157&realName=%25E8%2583%25A1%25E4%25B8%25BD%25E5%258D%258E&loginType=0&userPhoto=&topicModule=learn_one&topicModuleColour=blue&titleFlag=1&templateType=8&desensitizationDisplay=true',
#     # url='https://course.icve.com.cn/taolun/learn/courseTopicAction.action?action=item&itemId=402883a983232378018329f7892a1ddc&courseId=1754b2c1a83f4268a668e959b9d3941a&ssoUserId=wjk092157&realName=%25E8%2583%25A1%25E4%25B8%25BD%25E5%258D%258E&loginType=0&userPhoto=&topicModule=learn_one&topicModuleColour=blue&titleFlag=1&templateType=8&desensitizationDisplay=true',
#     headers=header)
# print(res1.text)
# patter = re.compile('limitId.*;')
try:
    limitId = patter.search(res.content.decode()).group().split('"')[1]
except Exception:
    print('\033[31m获取limitId失败，检查Cookie\033[0m')
    exit()

# 获得itemId
res = requests.get(
    f'{BaseURL}/learnspace/learn/learn/templateeight/courseware_index.action?params.courseId={courseId}___',
    headers=header
)
soup = BeautifulSoup(res.content, 'lxml')
# print("soup:", soup)

# ----------------------------------分割线----------------------------------
# 判断视频
divs = soup.find_all(id=re.compile("s_point_.*"), itemtype="video")
# 视频的id
itemids = {}
for i in divs:
    itemids[i.find(class_="s_pointti").text] = i['id'].strip("s_point_")
print("获取所有视频id===>", itemids, "开始刷课===>")
# print("itemids.keys():", itemids.keys())
# 开始刷课
for key in itemids.keys():
    itemid = itemids[key]
    print("itemid:", itemid)
    itemid = itemids[key]
    data2 = {
        'itemId': itemid,
        'videoTotalTime': '00:10:00'
    }
    total = requests.post(url=f'{BaseURL}/learnspace/course/plugins/cloud_updateVideoTotalTime.action',
                          headers=header, data=data2)
    # 判断视频是否学习完成
    data2 = {
        'params.courseId': f'{courseId}___',
        'params.itemId': itemid
    }
    complete = requests.post(
        url=f'{BaseURL}/learnspace/learn/learnCourseware/getSingleItemCompleteCase.json',
        headers=header, data=data2)
    print("code:", complete.content.decode())
    # 判断返回值 1表示学习完成，2表示部分学习，0表示内容没有学习过
    if json.loads(complete.content.decode())['result']['completed'] == '1':
        print(key, '视频状态已完成，跳过')
        continue
    # 刷课
    start = 0
    end = 0
    # 轮询片段
    while True:
        start = end
        # 每次增加10秒
        end = start + 20
        while True:
            cmd = os.popen('node ./test.js %s %s %s' % (itemid, start, end))
            # 原始字符串的开头和结尾删除给定的字符
            studyrecord = cmd.read().strip('\n')
            cmd.close()
            data = {
                "limitId": limitId,
                "studyRecord": studyrecord
            }
            res2 = requests.post(
                url=f'{BaseURL}/learnspace/course/study/learningTime_saveVideoLearnDetailRecord.action',
                headers=header, data=data
            )
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
    time.sleep(1)

# 判断文档
divs = soup.find_all(id=re.compile("s_point_.*"), itemtype="doc")
itemids = {}
for i in divs:
    itemids[i.find(class_="s_pointti").text] = i['id'].strip("s_point_")
# 轮询item
print("获取所有文档id===>", itemids, "开始刷文档===>")
for key in itemids.keys():
    itemid = itemids[key]
    # 判断文档是否学习完成
    data2 = {
        'params.courseId': f'{courseId}___',
        'params.itemId': itemid
    }
    complete = requests.post(
        url=f'{BaseURL}/learnspace/learn/learnCourseware/getSingleItemCompleteCase.json',
        headers=header, data=data2)
    # 判断返回值 1表示学习完成，2表示部分学习，0表示内容没有学习过
    if json.loads(complete.content.decode())['result']['completed'] == '1':
        print(key, '状态已完成，跳过')
        continue
    # 保存文档
    doc_data = {
        'courseId': f'{courseId}',
        'itemId': itemid,
        'recordType': 0,
        'studyTime': 300
    }
    response = requests.post(
        url=f'{BaseURL}/learnspace/course/study/learningTime_saveCourseItemLearnRecord.action',
        headers=header, data=doc_data)
    if '成功' in response.content.decode():
        print(key, '\033[31m文档完成\033[0m')
    else:
        print(key, '保存失败')
        set_trace()
time.sleep(1)

# 判断文本
divs = soup.find_all(id=re.compile("s_point_.*"), itemtype="text")
# print(divs)
itemids = {}
for i in divs:
    itemids[i.find(class_="s_pointti").text] = i['id'].strip("s_point_")
# 轮询item
print("获取所有图文id===>", itemids, "开始刷图文===>")
for key in itemids.keys():
    itemid = itemids[key]
    # 判断文档是否学习完成
    data2 = {
        'params.itemId': itemid,
        'params.courseId': f'{courseId}___'
    }
    complete = requests.post(
        url=f'{BaseURL}/learnspace/learn/learnCourseware/getSingleItemCompleteCase.json',
        headers=header, data=data2)
    # 判断返回值 1表示学习完成，2表示部分学习，0表示内容没有学习过
    if json.loads(complete.content.decode())['result']['completed'] == '1':
        print(key, '状态已完成，跳过')
        continue
    # 保存图文
    doc_data = {
        'courseId': courseId,
        'studyTime': 300,
        'itemId': itemid,
        'recordType': 0
    }
    # 判断图文是否学习完成
    response = requests.post(
        url=f'{BaseURL}/learnspace/course/study/learningTime_saveCourseItemLearnRecord.action',
        headers=header, data=doc_data)
    if json.loads(complete.content.decode())['result']['completed'] == '1':
        print(key, '\033[31m图文完成\033[0m')
    else:
        print(key, '保存失败')
time.sleep(1)

# 课程评价
data = {"params": {f"subjectId": f"{subjectId}", "star": 5}}
response = requests.post(
    url=f'{BaseURL}/discuss-api/discussStar/saveStar', headers=header, json=data)
if json.loads(response.content.decode())['code'] == '1':
    print("进行评价")
    create_data = {
        "bean": {"subjectId": f"{subjectId}", "content": f"{random.choice(content)}", "thumbImgs": "",
                 "originalImgs": ""}}
    response = requests.post(
        url=f"{BaseURL}/discuss-api/discussComment/create",
        headers=header, json=create_data
    )
    if json.loads(response.content.decode())['code'] == '1':
        print("课程评价完成！")
        print(key, '\033[31m课程评价完成\033[0m')
    else:
        print("错误了！", response.content.decode())
else:
    print("错误了！", response.content.decode())
time.sleep(1)

# 主题讨论
divs = soup.find_all(id=re.compile("s_point_.*"), itemtype="topic")
# print(divs)
itemids = {}
for i in divs:
    itemids[i.find(class_="s_pointti").text] = i['id'].strip("s_point_")
# 轮询item
print("获取所有讨论id===>", itemids, "开始刷讨论===>")
for key in itemids.keys():
    itemid = itemids[key]
    print(itemid)
    data = {
        "action": "reply",
        "curPage": 999,
        "parentId": '402883e681197106018329f789602031',
        "mainId": '402883e681197106018329f789602031',
        "content": "{}".format(random.choice(Irrigation_content)),
        "itemId": itemid,
        "courseId": courseId,
        "createUserId": "402883ab84ce0af7018532b0aa6e5dcf",  # 用户id，需要提前获取
    }
    response = requests.post(
        url=f'{BaseURL}/taolun/learn/courseTopicAction.action', headers=header, data=data)
    print(json.loads(response.content.decode()))
    if json.loads(response.content.decode())['success'] == True:
        print("灌水成功")
        print(key, '\033[31m灌水完成\033[0m')
    else:
        print("错误了！", response.content.decode())
time.sleep(1)


# -----------------未开发功能-----------------
# # 判断音频
# divs = soup.find_all(id=re.compile("s_point_.*"), itemtype="audio")
# # 音频的id
# itemids = {}
# for i in divs:
#     itemids[i.find(class_="s_pointti").text] = i['id'].strip("s_point_")
# print("获取所有音频id===>", itemids, "开始刷音频>>>>")
# # 开始刷音频
# for key in itemids.keys():
#     itemid = itemids[key]
#     print("itemid:", itemid)
#     data2 = {
#         'params.courseId': f'{courseId}___',
#         'params.itemId': itemid,
#         'params.videoTotalTime': '00:10:00'
#     }
#     total = requests.post(url=f'{BaseURL}/learnspace/learn/learn/common/audio_learn_record_detail.action',
#                           headers=header, data=data2)
#     # 判断音频是否学习完成
#     data2 = {
#         'params.courseId': f'{courseId}___',
#         'params.itemId': itemid
#     }
#     complete = requests.post(
#         url=f'{BaseURL}/learnspace/learn/learnCourseware/getSingleItemCompleteCase.json',
#         headers=header, data=data2)
#     print("code:", complete.content.decode())
#     # 判断返回值 1表示学习完成，2表示部分学习，0表示内容没有学习过
#     if json.loads(complete.content.decode())['result']['completed'] == '1':
#         print(key, '音频状态已完成，跳过')
#         continue
#     # 刷音频
#     print(f"检测到未刷音频{key}，开始刷音频")
#     while True:
#         doc_data = {
#             'courseId': f'{courseId}',
#             'itemId': itemid,
#             'studyTime': 300
#         }
#         response = requests.post(
#             url=f'{BaseURL}/learnspace/course/study/learningTime_saveLearningTime.action',
#             headers=header, data=doc_data)
#         start = 0
#         end = 0
#         # 轮询片段
#         while True:
#             start = end
#             # 每次增加10秒
#             end = start + 20
#             cmd = os.popen('node ./test.js %s %s %s' % (itemid, start, end))
#             # 原始字符串的开头和结尾删除给定的字符
#             # studyRecord参数就是将数据格式化后序列化再进行AES加密得到的字符串
#             studyrecord = cmd.read().strip('\n')
#             # print("--->", studyrecord)
#             cmd.close()
#             data = {
#                 "studyRecord": studyrecord,
#                 "limitId": limitId
#             }
#             res2 = requests.post(
#                 url=f'{BaseURL}/learnspace/course/study/learningTime_saveAudioLearnDetailRecord.action',
#                 headers=header, data=data)
#             if '请求成功' in res2.content.decode():
#                 print("\r", end="")
#                 print(key, "\033[32m学习时长: {}秒 \033[0m".format(end), end="")
#                 sys.stdout.flush()
#                 break
#         print(key, '\033[31m学习完成\033[0m')

# todo:需要重新解析考试网址
# # 判断随堂考试
# divs = soup.find_all(id=re.compile("s_point_.*"), itemtype="exam")
# # print(divs)
# itemids = {}
# for i in divs:
#     itemids[i.find(class_="s_pointti").text] = i['id'].strip("s_point_")
# # 轮询item
# print("获取所有考试id===>", itemids, "开始刷考试===>")
# for key in itemids.keys():
#     itemid = itemids[key]
#     # 判断测验是否完成
#     print(itemid)
#     data2 = {
#         'params.itemId': itemid,
#         'params.courseId': f'{courseId}___'
#     }
#     complete = requests.post(
#         url=f'{BaseURL}/learnspace/learn/learnCourseware/getSingleItemCompleteCase.json',
#         headers=header, data=data2)
#     if json.loads(complete.content.decode())['result']['completed'] == '1':
#         print(key, '状态已完成，跳过')
#         continue
#     # 考试
#     print("开始考试---->")
#     # todo:考试逻辑
#     doc_data = {
#         'courseId': f'{courseId}___',
#         'studyTime': 300,
#         'itemId': itemid,
#     }
#     # 判断图文是否学习完成
#     response = requests.post(
#         url=f'{BaseURL}/learnspace/course/study/learningTime_saveLearningTime.action',
#         headers=header, data=doc_data)
#     if '成功' in response.content.decode():
#         print(key, '完成')
#     else:
#         print(key, '保存失败')
#         set_trace()

# todo:
#  刷课类型：itemtype="doc(实现)"、exam(待实现)、topic(实现)、video(实现)、text(实现)、audio(待实现)
