#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 13:02:42 2018

@author: james
"""

import cv2
import requests
import json
import threading
import time
import base64
import numpy as np
import xugu

servo=xugu.Servo(12)
access_token="24.42017d996da0a23f3c4567b8dfd16a21.2592000.1550220300.282335-14563606"
API_KEY="ijoqlG1PdSsdxtXc7DNn68jh"
SECRET_KEY="Erpr184wiWCG7ZZglFKKG3Zm3up6xUmi"
face_num=0
frame=None
now_time=0
face_info={}

def cvimg_to_b64(img):
    try:
        image = cv2.imencode('.jpg', img)[1]
        base64_data = str(base64.b64encode(image))[2:-1]
        return base64_data
    except Exception as e:
        return "error"


def face_search(img64):
    url="https://aip.baidubce.com/rest/2.0/face/v3/search"
    url=url+"?access_token="+access_token
    data={
            "image":img64,
            "image_type":"BASE64",
            "group_id_list":"test_group"}
    try:
        response=requests.post(url,files=None,data=data)
        res_text=response.text
        res_json=json.loads(res_text)
        return res_json
    except Exception:
        return "error"

def get_ai_access_token():
    url="https://aip.baidubce.com/oauth/2.0/token?grant_type=" +\
    "client_credentials&client_id=%s&client_secret=%s" %(API_KEY,SECRET_KEY)
    try:
        response=requests.get(url)
        res_text=response.text
        res_json=json.loads(res_text)
        return str(res_json["access_token"])
    except Exception:
        return "error"

def get_face_info(img64):
    url="https://aip.baidubce.com/rest/2.0/face/v3/detect"
    url = url + "?access_token=" + access_token
    data = {"face_field":"age,beauty,expression,faceshape,gender,glasses,landmark,race,qualities",
                  "image_type":"BASE64","image":img64,"max_face_num":5}
    try:
        response = requests.post(url,data=data)
        res_text=response.text
        res_json=json.loads(res_text)
        return res_json
    except Exception:
        return "error"
    
def post_request(frame,face_num,nt):
    global face_info
    if(face_num>0) and (time.time()-nt>3):
        global now_time
        now_time=time.time()
        img64=cvimg_to_b64(frame)
        res=get_face_info(img64)
        try:
            status=res['error_msg']
        except Exception:
            status=""
        if(status=="SUCCESS"):
            face_info['gender']= res['result']['face_list'][0]['gender']['type']
            face_info['age']=res['result']['face_list'][0]['age']
            face_info['beauty']=res['result']['face_list'][0]['beauty']
            return 
        else:
            face_info={}
            
def faceDetect(img,face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')):
    size=img.shape[:2]
    divisor = 8
    h,w=size
    minSize=(w//divisor,h//divisor)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 1,cv2.CASCADE_SCALE_IMAGE,minSize)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    return img,len(faces)


def put_Text(cvimg,text,location,size=2):
    cvimg=cv2.putText(cvimg, text, location,cv2.FONT_HERSHEY_SIMPLEX, size, (51, 102, 255), 3)
    return cvimg


def check_token():
    print(int(time.time()) - 1547628298)
    if int(time.time()) - 1547628298 >= 2592000:
        global access_token
        token = get_ai_access_token()
        if token != "error":
            access_token = get_ai_access_token()


def main():
    check_token()
    cap = cv2.VideoCapture(0)
    global now_time
    now_time=time.time()
    while(True):
        global face_info
        global servo
        ret, frame = cap.read()
        if ret == True:
            frame1,face_num = faceDetect(frame)
            frame1=cv2.flip(frame1,1,dst=None)
            frame1=cv2.resize(frame1,(1280,800),interpolation=cv2.INTER_LINEAR)
            t=threading.Thread(target=post_request,args=(frame,face_num,now_time,), name='POST_REQUEST')
            t.start()
            print(face_info)
            if face_info=={} :
                frame1=put_Text(frame1,"Waiting...",(50,50))
            else:
                try:
                    frame1=put_Text(frame1,str(int(face_info['age'])),(300,50))
                    frame1=put_Text(frame1,str(face_info['gender']),(300,120))
                    frame1=put_Text(frame1,str(int(face_info['beauty'])),(300,190))
                    frame1=put_Text(frame1,"Age:",(50,50))
                    frame1=put_Text(frame1,"Gender:",(50,120))
                    frame1=put_Text(frame1,"Beauty:",(50,190))
                    servo.angle(int(face_info['beauty']*3))
                except Exception:
                    pass
                
            cv2.imshow('Magic Image',frame1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

main()


