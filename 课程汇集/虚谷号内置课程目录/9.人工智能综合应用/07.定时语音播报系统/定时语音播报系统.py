#!/usr/bin/env python
# coding: utf-8

# # 定时语音播报系统

# ## 功能描述
# 1. 运行程序后，在特定的时间执行任务，如播报天气预报、英语听力、提醒吃饭等。
# 2. 播报天气预报前，会先播放提示音“叮”，这样不会太突兀。
# 3. 英语听力会提供两种语音，一种是百度合成等，一种是真人发音。
# 4. 还需要什么功能？请大家提提
# 
# **注：在“虚谷号”上部署该系统，只需要将.py代码复制到“vvBoard”的“Python”文件夹，文件名为“main.py”。**

# ### 1.基础库

import os,sys,time,datetime
import requests,re
from aip import AipSpeech
from threading import Timer

# ### 2.获取天气的函数

API='https://api.seniverse.com/v3/weather/now.json'
KEY='S_zw8qq3BQPUr1wMU'
LANGUAGE='zh-Hans'
UNIT='c'
def fetchWeather(location):
    #location：城市名称，如wenzhou、hangzhou
    result = requests.get(API, params={
        'key': KEY,
        'location': location,
        'language': LANGUAGE,
        'unit': UNIT
    }, timeout=1)
    #print(result)
    return result

#解析天气预报
def get_weather(location):
    result = fetchWeather(location)
    result=result.json()
    r=result["results"][0]
    s1=r["location"]["name"] #城市名称
    s2=r["now"]["text"] #天气信息
    s3=r["now"]["temperature"] #气温
    s=s1 + '今天的天气' + s2 +'，气温'+ s3
    return s

# ### 3.获取随机英语的函数

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


is_w = True    
# 每隔40秒执行一次任务
# 7点播报天气信息，8和9点会朗读英语，12和17点会提醒做饭。
def autorun():
    global is_w
    cur=datetime.datetime.now()
    mins=cur.minute
    hours=cur.hour
    txt = '虚谷号智能助手……'
    if hours == 7 and is_w == True:
        txt = txt + "播放天气预报信息："
        txt = txt + get_weather("wenzhou")
        tts(txt)
        is_w = False
    if hours > 7:
        is_w = True
    # 提醒做饭了
    if hours in (12,17) and mins == 0:
        txt = txt + "提醒你，吃饭时间到了！"
        tts(txt)
    # 处理英语
    if hours in (8,9) and mins == 0:
        txt = txt + "英语学习时间："
        s1,s2=getmryj()
        txt = txt + s1
        tts(txt)
        #5秒钟后播放原英文朗读
        time.sleep(5)
        os.system('play ' + s2)
    print('TimeNow:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    t = Timer(40, autorun)
    t.start()

if __name__ == "__main__":
    autorun()






