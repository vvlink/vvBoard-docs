#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Date of establishment: November 27, 2018

@author: zhangzd
"""

import cv2
import requests
import json
import threading
import time
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from aip import AipSpeech
import pygame
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import os
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

access_token = ""
AppID = "15126848"
API_KEY = "BPaS8KCk1B6Io9EqEOw1pOH3"
SECRET_KEY = "AL3B7XOmoRZojqFivCzvxuGYDDQZ7G58"
client = AipSpeech(AppID, API_KEY, SECRET_KEY)
frame = None
now_time = 0
number = None
audio_file='auido.mp3'
data = None

def save_audio(number):
    result  = client.synthesis(number, 'zh', 1, {
        'vol': 5,
        })
    if not isinstance(result, dict):
        with open(audio_file, 'wb') as f:
            f.write(result)
        os.system("play *mp3") 
        

def cvimg_to_b64(img):
    try:
        image = cv2.imencode('.jpg', img)[1]
        base64_data = str(base64.b64encode(image))[2:-1]
        return base64_data
    except Exception as e:
        return "error"


def get_ai_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=" + \
          "client_credentials&client_id=%s&client_secret=%s" % (API_KEY, SECRET_KEY)
    try:
        response = requests.get(url)
        res_text = response.text
        res_json = json.loads(res_text)
        return str(res_json["access_token"])
    except Exception:
        return "error"

    
def get_number(img64):
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    url = url + "?access_token=" + access_token
    data = {
        "image": img64, "type": 'commontext'
    }
    try:
        response = requests.post(url,data=data)
        res_text = response.content.decode("utf-8")
        res_json = json.loads(res_text)
        return res_json
    except Exception:
        return "error"


def psyst_request(frame, nt):
    global number
    if time.time() - nt > 3:
        global now_time
        now_time = time.time()
        img64 = cvimg_to_b64(frame)
        res = get_number(img64)
        try:
            if res["words_result"]:
                if len(res["words_result"]) == 1:
                    number = res["words_result"][0]["words"]
                else:
                    number = res["words_result"][0]["words"]
                    for i in range(1, len(res["words_result"])):
                        number += (res["words_result"][i]["words"])
                return
            else:
                number = None
        except:
            number = None

def put_Text(cvimg, text, location, size=50):
    cvimg = Image.fromarray(cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(cvimg)
    fontText = ImageFont.truetype("./simsun.ttc", size, encoding="utf-8")
    draw.text(location, text, (255,0,0), font=fontText)
    cvimg = cv2.cvtColor(np.array(cvimg), cv2.COLOR_RGB2BGR)
    return cvimg

def main():
    token = get_ai_access_token()
    if token != "error":
        global access_token
        access_token = token
    cap = cv2.VideoCapture(0)
    global now_time
    now_time = time.time()
    while (True):
        ret, frame = cap.read()
        if ret == True:
            frame1 = cv2.resize(frame, (1280, 800), interpolation=cv2.INTER_LINEAR)
            t = threading.Thread(target=psyst_request, args=(frame, now_time,), name='PsysT_REQUEST')
            t.start()
            print(number)
            if number == None:
                frame1 = put_Text(frame1, "Waiting...", (50, 50))
            else:
                try:
                    frame1 = put_Text(frame1, str(number), (200, 50))
                    frame1 = put_Text(frame1, "words:", (50, 50))
                except Exception:
                    pass
                global data
                if data != number:
                    p = threading.Thread(target=save_audio, args=(number,))
                    p.start()
                    data = number
            cv2.imshow('Magic Image', frame1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()


