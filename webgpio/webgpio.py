#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 21:49:02 2018
@author: james、yyp、xiezuouru
version：0.1
"""
import threading #导入threading模块
from flask import Flask
from flask import request
from xugu import Pin
from xugu import Servo
import time

app = Flask(__name__)
ret = None
pin = None
types = None
pin_D_list=['D0','D1','D2','D3','D4','D5','D6','D7','D8','D9','D10','D11','D12','D13']
pin_A_list=['A0','A1','A2','A3','A4','A5']
type_list=['Digital','Analog','Servo']

@app.route('/web_gpio',methods=["POST","GET"])
def web_gpio():
    if (request.method == 'GET'):
        return web_gpio_get(request)
    elif (request.method=='POST'):
        return web_gpio_post(request)

def web_gpio_get(request):
    global ret,pin
    pin=request.values.get("pin")    
    if not (pin in pin_D_list or pin in pin_A_list):
        return "error:invalid Pin"
    if pin in pin_D_list:
        ret = 0
        time.sleep(0.5)
        return str(value)
    if pin in pin_A_list:
        ret = 1
        time.sleep(0.5)
        return str(value)
        
def web_gpio_post(request):
    global types,pin,value
    pin=request.values.get("pin")
    value=request.values.get("value")
    types=request.values.get("types")
    if not (pin in pin_D_list or pin in pin_A_list):
        return "error:invalid Pin"
    try:
        value=int(value)
    except Exception:
        return "error:Value"
    if not types in type_list:
        return "error:invalid Type"
    return "success:set "+pin+" to "+str(value)+" with "+types+" mode"

def rungpio():
    global value,ret,types
    while True:
        if ret == 0:    
            xugu_pin=Pin(pin,Pin.IN)
            value=xugu_pin.read_digital()
            ret = None
        if ret == 1:
            xugu_pin=Pin(pin,Pin.ANALOG)
            value=xugu_pin.read_analog()
            ret = None
        if types=="Digital":
            xugu_pin=Pin(pin,Pin.OUT)
            xugu_pin.write_digital(value)
            types=None
        if types=="Analog":
            print(value)
            xugu_pin=Pin(pin,Pin.OUT)
            xugu_pin.write_analog(value)
            types=None
        if types=="Servo":
            xugu_servo=Servo(pin)
            xugu_servo.write_angle(value)
            types=None
             
def run():
    app.run(host='0.0.0.0',port=1024,debug=False)   

t=threading.Thread(target=run)
t.start()

rungpio()

