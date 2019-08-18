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



access_token = "" #定义sccess_token变量
API_KEY = "YNoddBhqFuPn0gsrqG6lxk7A" #定义API_KEY变量
SECRET_KEY = "p5dyxaxz2XiHCtnL1HagsQBzOBv5nEzA" #定义SECRET_KEY变量
frame = None #定义frame变量
now_time = 0 #定义now_time变量
plant_info = None #定义plant_info变量



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

def get_plant(img64):
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/plant"
    url = url + "?access_token=" + access_token
    data = {
        "image": img64, "type": 'plant'
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
    判断识别的是植物还是植物，并提取有效数据
    """
    global plant_info
    if time.time() - nt > 3: #判断时间差是否大于3
        global now_time #声明now_time是全局变量
        now_time = time.time() #给now_time重新赋值为当前秒数
        img64 = cvimg_to_b64(frame) #调用cvimg_to_b64函数
        res = get_plant(img64) #调用get_plant函数
        if "error_msg" in res:
            if res["error_msg"] == 'Open api daily request limit reached':
                raise Exception('Open api daily request limit reached')
        if "error" not in res: #判断识别是否出错
            try:
                plant_info = res["result"] #将识别出来的结果赋值给plant_info
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

def main():
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
            if not plant_info or plant_info[0]["name"]=="非植物":
                frame1 = put_Text(frame1, "Waiting...", (50, 50)) #在画布上显示Waiting     
            elif plant_info[0]["name"]!="非植物":
                print(plant_info[0]) #打印植物信息
               	try:
                        #在画布上写字
                    #for i in range(5):
                    frame1 = put_Text(frame1, str(plant_info[0]["score"])[:4], (150, 0 * 70 + 50))
                    frame1 = put_Text(frame1, str(plant_info[0]["name"]), (320, 0 * 70 + 50))
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


if __name__ == "__main__":
    main()
