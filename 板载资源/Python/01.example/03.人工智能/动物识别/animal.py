#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Date of establishment: November 27, 2018

@author: zhangzd
"""

import cv2 #导入cv2模块
import requests #导入requests模块
import json #导入json模块
import threading #导入threading模块
import time #导入时间模块
import base64 #导入base64模块
import numpy as np #导入numpy模块
from PIL import Image, ImageDraw, ImageFont #导入PIL模块
from xugu import *
import os
import signal
from aip import AipSpeech
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

audio_file='auido.mp3'
AppID = "15469649"
access_token = "" #定义sccess_token变量
API_KEY = "3vZgLINSnGGEafPflkTLzkGh" #定义API_KEY变量
SECRET_KEY = "8cUXtkMed2z86kqfyrV606ylnCmfcc48" #定义SECRET_KEY变量
frame = None #定义frame变量
now_time = 0 #定义now_time变量
animal_info = None #定义animal_info变量
client = AipSpeech(AppID, API_KEY, SECRET_KEY)

def save_audio(number):
    result  = client.synthesis(number, 'zh', 1, {
        'vol': 5,
        'per': 2
        })
    if not isinstance(result, dict):
        with open(audio_file, 'wb') as f:
            f.write(result)
        os.popen("play *mp3")

def cvimg_to_b64(img):
    """
    图片转换函数，将二进制图片转换为base64加密格式
    """
    try:
        image = cv2.imencode('.jpg', img)[1] #将图片格式转换(编码)成流数据，赋值到内存缓存中
        base64_data = str(base64.b64encode(image))[2:-1] #将图片加密成base64格式的数据
        return base64_data #返回加密后的结果
    except Exception as e:
        return "error"

def get_ai_access_token():
    """
    获取token值
    """
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=" + \
          "client_credentials&client_id=%s&client_secret=%s" % (API_KEY, SECRET_KEY)
    try:
        response = requests.get(url)
        res_text = response.text
        res_json = json.loads(res_text)
        return str(res_json["access_token"])
    except Exception:
        return "error"

def get_animal(img64):
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/animal"
    url = url + "?access_token=" + access_token
    data = {
        "image": img64, "type": 'animal'
    }
    try:
        response = requests.post(url,data=data)
        res_text=response.content.decode("utf-8")
        res_json=json.loads(res_text)
        return res_json
    except Exception:
        return "error"


def post_request(frame, nt):
    """
    判断识别的是动物还是植物，并提取有效数据
    """
    global animal_info
    if time.time() - nt > 3: #判断时间差是否大于3
        global now_time #声明now_time是全局变量
        now_time = time.time() #给now_time重新赋值为当前秒数
        img64 = cvimg_to_b64(frame) #调用cvimg_to_b64函数
        res = get_animal(img64) #调用get_animal函数
        print(res)
        if "error_msg" in res:
            if res["error_msg"] == 'Open api daily request limit reached':
                raise Exception('Open api daily request limit reached')
        if "error" not in res: #判断识别是否出错
            try:
                animal_info = res["result"] #将识别出来的结果赋值给animal_info
            except:
                pass
            return #退出函数
          

def put_Text(cvimg, text, location, size=30):
    """
    将动植物信息显示在屏幕上
    """
    cvimg = Image.fromarray(cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(cvimg)
    fontText = ImageFont.truetype("./simsun.ttc", size, encoding="utf-8")
    draw.text(location, text, (255, 0, 0), font=fontText)
    cvimg = cv2.cvtColor(np.array(cvimg), cv2.COLOR_RGB2BGR)
    return cvimg
left_pin = Pin(9,Pin.OUT)
right_pin = Pin(3,Pin.OUT)
middle_pin = Pin(6,Pin.OUT)

def speed():
    i = 40
    middle_pin.write_analog(i)
    left_pin.write_analog(0)
    right_pin.write_analog(180)
    flag = True
    animal = None
    while True:
        while i<160 and flag == True:
            if animal_info != None and len(animal_info) > 1:
                if animal == animal_info[0]["name"]:
                    i+=1
                    if i == 160:
                        flag = False
                        animal = None
                    middle_pin.write_analog(i)
                    time.sleep(.2)
                else:
                    right_pin.write_analog(0)
                    animal = animal_info[0]["name"]
                    save_audio(animal_info[0]["name"])
                    time.sleep(3)
            else:
                i+=1
                if i == 160:
                    flag = False
                    animal = None
                middle_pin.write_analog(i)
                time.sleep(.2)
                left_pin.write_analog(0)
                right_pin.write_analog(180)

        while i>40 and flag == False:
            if animal_info != None and len(animal_info) > 1:
                if animal == animal_info[0]["name"]:
                    i-=1
                    if i == 40:
                        flag = True
                        animal = None
                    middle_pin.write_analog(i)
                    time.sleep(.2)
                else:
                    left_pin.write_analog(180)
                    animal = animal_info[0]["name"]
                    save_audio(animal_info[0]["name"])
                    time.sleep(3)
            else:
                i-=1
                if i == 40:
                    flag = True
                    animal = None
                middle_pin.write_analog(i)
                time.sleep(.2)
                left_pin.write_analog(0)
                right_pin.write_analog(180)

def main(pid):
    """
    程序主函数
    """
    token = get_ai_access_token()
    if token != "error":
        global access_token
        access_token = token
    cap = cv2.VideoCapture(0) #创建摄像头对象
    global now_time #声明now_time为全局变量
    now_time = time.time() #将当前时间秒数赋值给now_time

    while (True): #创建一个死循环用于循环读取摄像头数据
        ret, frame = cap.read() #从摄像头中读取一张图片
        if ret == True: #判断是否读取成功
            #创建一个1280x800的窗口
            frame1 = cv2.resize(frame, (1280, 800), interpolation=cv2.INTER_LINEAR)
            #创建一个线程用于处理读取到的图片
            t=threading.Thread(target=post_request,args=(frame,now_time,), name='POST_REQUEST')
            t.start() #启动这个线程
            if not animal_info or animal_info[0]["name"]=="非动物":
                frame1 = put_Text(frame1, "Waiting...", (50, 50)) #在画布上显示Waiting
            elif animal_info[0]["name"]!="非动物":
                print(animal_info[0]) #打印动物信息
               	try:
                        #在画布上写字
                    #for i in range(5):
                    frame1 = put_Text(frame1, str(animal_info[0]["score"][:4]), (150, 0 * 70 + 50))
                    frame1 = put_Text(frame1, str(animal_info[0]["name"]), (320, 0 * 70 + 50))
                    #for i in range(5):
                    frame1 = put_Text(frame1, "score:", (50, 0 * 70 + 50))
                    frame1 = put_Text(frame1, "name:", (250, 0 * 70 + 50))
                except Exception:
                    pass
            cv2.imshow('Magic Image', frame1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    os.kill(pid,signal.SIGKILL)


if __name__ == "__main__":
    pid = os.getpid()
    t_main = threading.Thread(target=main,args=(pid,))
    t_main.start()
    speed()
    