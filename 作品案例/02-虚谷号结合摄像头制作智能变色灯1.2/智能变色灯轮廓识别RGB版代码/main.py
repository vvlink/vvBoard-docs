#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# author linmy


'''虚谷号中Cv2库的下载
方法①sudo pip install opencv-python
方法②sudo apt-get install python-opencv
scope的密码：输入scope后回车
# 同理，还有其他的：python-scipy/python-numpy/
colorlist是本地的py文件，用于存储各种颜色的说明
'''
import cv2
from yeelight import Bulb
import time
import colorList

bulb = Bulb("192.168.31.39")
bulb.turn_on()
#得到图片
def get_pic():
    cap=cv2.VideoCapture(0)
    sucess,img=cap.read()
    cv2.imwrite("CachePhoto/image.jpg",img)
    cap.release()

#处理图片
def get_color(frame):
    print('开始处理')
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    maxsum = -100
    color = None
    color_dict = colorList.getColorList()
    for d in color_dict:
        mask = cv2.inRange(hsv, color_dict[d][0], color_dict[d][1])
        cv2.imwrite('CachePhoto/' + d +'.jpg', mask)
        binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
        binary = cv2.dilate(binary, None, iterations=2)
        img, cnts, hiera = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        sum = 0
        for c in cnts:
            #轮廓面积
            sum += cv2.contourArea(c)   
        if sum > maxsum:
            maxsum = sum
            color = d
    return color


if __name__ == '__main__':
    while 1:
        get_pic()
        filename = r"CachePhoto/image.jpg"
        frame = cv2.imread(filename)
        rgb=get_color(frame)
        red=int(rgb[1:3],16)
        green=int(rgb[3:5],16)
        blue=int(rgb[5:7],16)
        bulb.set_rgb(red,green,blue)
        time.sleep(5)
