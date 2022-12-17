
## 适用https://icve-mooc.icve.com.cn/cms/
###主要刷课API
- URL：https://course.icve.com.cn/learnspace/course/study/learningTime_saveVideoLearnDetailRecord.action
请求方式：Post
参数：

limitId: 包含在网页的javascript中，每次刷新页面limitId也会刷新，可重复用
studyRecord： 通过crypto-js AES加密的一串数据，包含课程ID，视频ID，以及学习时长，学习起始秒数和学习结束的秒数。

返回结果：”保存状态成功“或者“参数不合法，超出时长”，学习时长越长，需要等待一定时间才能第再次保存学习状态。学习时长短不需要等待。

![](image/img1.png)


###获取limitId
- URL:https://course.icve.com.cn/learnspace/learn/learn/templateeight/index.action?params.courseId=26ae32dc2dcd4c9cbace10894d9a172b___&params.templateType=8&params.templateStyleType=0&params.template=templateeight&params.classId=&params.tplRoot=learn
请求方式： Get

参数：url里面可以看到，主要包含一个课程id，其他的似乎默认就行,可以去浏览器里找到对应的url

返回结果：内容是html网页，直接通过正则搜索找到limitId

![](image/img2.png)


studyRecord AES加密的学习状态参数
![](image/img3.png)

官方加密功能函数和格式化函数的js文件URL: https://course.icve.com.cn/learnspace/resource/common/js/CommonUtil.js?v=2022042401。

studyRecord参数就是将数据格式化后序列化再进行AES加密得到的字符串

主要的参数就只有courseId,itemId,stratTime,endTime:

courseId: 代表当前学习课程的16进制id

itemId: 对应课程中的每个视频或者文档也有一个16进制id

startTime: 对应视频时长进度

endTime: 对应视频的时长，表示当前视频从startTime秒学习到了endTime的秒数

### 文档内容完成学习API
- url:https://course.icve.com.cn/learnspace/course/study/learningTime_saveCourseItemLearnRecord.action

参数：课程id，视频id，其他的参数固定即可
![](image/img4.png)


获取itemId
url:https://course.icve.com.cn/learnspace/learn/learn/templateeight/courseware_index.action?params.courseId=26ae32dc2dcd4c9cbace10894d9a172b___

返回的html中包含itmeId，可以通过beautifulsoup搜索id=spoint.* 获得对对应的标签
![](image/img5.png)

判断内容是否已经完成
url:https://course.icve.com.cn/learnspace/learn/learnCourseware/getSingleItemCompleteCase.json

返回json,completed等于1表示学习完成，2表示部分学习，0表示内容没有学习过。
![](image/img6.png)

效果图
![](image/img7.png)
![](image/img8.png)


完整py+nodejs代码
py需要安装库: requests bs4

nodejs需要安装库: crypto-js

自行替换python代码中的Cookie，test.js主要是做参数加密，运行python文件即可

文章参考地址：https://www.52pojie.cn/forum.php?mod=viewthread&tid=1710666&highlight=mooc