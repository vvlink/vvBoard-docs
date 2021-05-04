#!/usr/bin/env python
# coding: utf-8

# # 温州中学作息广播系统（schedule版）

# ## 功能描述
# 
# 1. 根据网课的作息时间表，自动播放铃声。
# 2. 起床铃声后播报天气预报，课间播报英语听力，饭点提醒吃饭等。
# 3. 播报天气预报前，会先播放提示音“叮”。
# 
# **注：在“虚谷号”上部署该系统，只需要将.py代码复制到“vvBoard”的“Python”文件夹，文件名为“main.py”。**

# ### 1.基础库

# In[1]:


import os,sys,time,datetime
import requests,re
from aip import AipSpeech
import schedule


# ### 2.获取天气的函数
# 
# 使用“心知天气”API，以北京为例返回的信息格式如下：
# 
# {"results":[{"location":{"id":"WX4FBXXFKE4F","name":"北京","country":"CN","path":"北京,北京,中国","timezone":"Asia/Shanghai","timezone_offset":"+08:00"},"now":{"text":"晴","code":"1","temperature":"7"},"last_update":"2020-02-22T18:10:00+08:00"}]}

# In[2]:


#获取天气预报，参数为城市的名称，如wenzhou
def get_weather(location):
    API='https://api.seniverse.com/v3/weather/now.json'
    KEY='S_zw8qq3BQPUr1wMU'
    result = requests.get(API, params={
        'key': KEY,
        'location': location,
        'language': 'zh-Hans',
        'unit': 'c'
    }, timeout=1)
    result=result.json()
    r=result["results"][0]
    s1=r["location"]["name"] #城市名称
    s2=r["now"]["text"] #天气信息
    s3=r["now"]["temperature"] #气温
    s=s1 + '今天的天气' + s2 +'，气温'+ s3
    return s


# ### 3.获取随机英语的函数

# In[3]:


# 每天一句英语
def getmryj():
    urle="http://dict.cn"
    r = requests.get(urle)
    resx=r.text
    #得到文本内容
    pattern = 'cleardot.gif.*\s.*'
    text1 = re.findall(pattern,resx)
    pattern = '\s\w.*\t'
    text2=re.findall(pattern,text1[0])
    #替换空格
    text3=text2[0].replace("&nbsp;",".")
    #得到mp3的地址
    pattern = 'audio=".*\S.mp3'
    text1 = re.findall(pattern,resx)
    pattern = 'http.*\S'
    text2 = re.findall(pattern,text1[0])
    #替换空格
    text4 = text2[0].replace("'","")
    return text3,text4


# ### 4.语音合成的函数

# In[4]:


""" 你的 APPID AK SK """
APP_ID = "15126848"
API_KEY = "BPaS8KCk1B6Io9EqEOw1pOH3"
SECRET_KEY = "AL3B7XOmoRZojqFivCzvxuGYDDQZ7G58"
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def tts(txt):
    #播放语音之前，先播放提示音，这个文件要下载过来
    os.system('play ding.wav')
    time.sleep(1)
    result = client.synthesis(txt, 'zh', 1, {'vol': 5,})
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('auido.mp3', 'wb') as f:
            f.write(result)
        os.system('play auido.mp3')

#tts("虚谷号测试语音")


# ### 5.开始工作
# 
# 定时运行，根据时间来调度，使用了schedule库。
# 
# **注：如果再次运行该代码，请先在“服务”处选择“重启 & 清空输出”或者“重启 & 运行所有”。**

# In[ ]:


# 铃声播放
def play_wave(s):
    ling = 'wave/'+ s +'.mp3'
    os.system('play ' + ling)

def tips(s):
    txt = "虚谷号提醒你" + s
    tts(txt)
# 课间英语
def learning():
    txt = "虚谷号英语学习时间："
    s1,s2=getmryj()
    txt = txt + s1
    tts(txt)
    #5秒钟后播放原英文朗读
    time.sleep(5)
    os.system('play ' + s2)
# 天气预报
def weather():
    txt = "虚谷号播放天气预报信息："
    txt = txt + get_weather("wenzhou")
    tts(txt)

# 起床
schedule.every().day.at("07:00").do(play_wave,s="起床")
schedule.every().day.at("07:10").do(weather)
schedule.every().day.at("07:30").do(play_wave,s="早读")
schedule.every().day.at("08:00").do(play_wave,s="上课")
schedule.every().day.at("09:00").do(play_wave,s="下课")
#趣味英语
schedule.every().day.at("09:10").do(learning)
schedule.every().day.at("09:20").do(play_wave,s="上课")
schedule.every().day.at("10:20").do(play_wave,s="下课")
schedule.every().day.at("10:40").do(play_wave,s="上课")
schedule.every().day.at("11:40").do(play_wave,s="下课")
# 午饭
schedule.every().day.at("12:00").do(tips,s="亲爱的主人，要吃午饭了！")
schedule.every().day.at("13:30").do(play_wave,s="上课")
schedule.every().day.at("14:30").do(play_wave,s="下课")
schedule.every().day.at("14:50").do(play_wave,s="上课")
schedule.every().day.at("15:50").do(play_wave,s="下课")
schedule.every().day.at("16:10").do(play_wave,s="上课")
schedule.every().day.at("17:10").do(play_wave,s="下课")
# 晚饭
schedule.every().day.at("18:00").do(tips,s="亲爱的主人，要吃晚饭了！")
schedule.every().day.at("18:10").do(play_wave,s="晚饭")
# 晚自修
schedule.every().day.at("18:30").do(play_wave,s="晚读开始")
schedule.every().day.at("19:30").do(play_wave,s="晚读结束")
schedule.every().day.at("19:50").do(play_wave,s="上课")
schedule.every().day.at("21:30").do(play_wave,s="下课")
# 睡觉
schedule.every().day.at("22:30").do(play_wave,s="就寝")

while True:
    schedule.run_pending()
    time.sleep(1)


# ### 6.参考资料
# 
# 正则表达式：https://zhuanlan.zhihu.com/p/71239731
# 
# Python的定时运行：https://www.jianshu.com/p/b77d934cc252
# 
# 树莓派+百度AI实现语音播报：https://github.com/vincen20/RaspberryPi_VOICE_V1/
# 
# schedule库：https://github.com/dbader/schedule

# In[ ]:




