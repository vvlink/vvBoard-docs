#!/usr/bin/env python
# coding: utf-8

# # “吟诗作对”机器人（升级版）

# 硬件准备：虚谷号、麦克风（连接到虚谷号）、小音箱（连接到虚谷号）、按钮传感器、Arduino扩展板（可选）
# 
# 注意事项：
#     - 请逐步运行单元格中的代码，即可查看具体效果。也可以全部运行，按下按钮（接在D2上）开始对话。
#     - 听到提示音后约等待两秒钟开始说话。
#     - 如果使用USB小音箱，请务必在电源口接上2A的电源。
#     - 请确认虚谷号处于上网状态。
#     
# 本范例的具体介绍请参考百度AI的文档。https://ai.baidu.com/docs#/ASR-Online-Python-SDK/f71dfc54

# ### 准备工作1：导入基本库

# In[ ]:


import pyaudio
import wave
import os
from aip import AipSpeech


# ### 准备工作2：设置认证信息和参数
# 
# 注：这里用的是测试账号，有访问次数的限制，如果测试失败，请使用自己的账号信息。

# In[ ]:


""" 你的 APPID AK SK """
APP_ID = "15126848"
API_KEY = "BPaS8KCk1B6Io9EqEOw1pOH3"
SECRET_KEY = "AL3B7XOmoRZojqFivCzvxuGYDDQZ7G58"
""" 这里是参数设置，请不要改动 """
CHUNK = 1024 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 3
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 参数介绍：
# - CHUNK：指定每个缓冲区的帧数。
# - FORMAT：采样大小和格式。我们这里是pyaudio.paInt16，即16位int型。
# - CHANNELS：声道数，这里我们设定的是单声道。
# - RATE：采样频率，录音设备在一秒钟内对声音信号的采样次数，采样频率越高声音的还原就越真实越自然。这里是16000。这里是为了匹配后期语音识别的要求设置的。常用的有8kHz, 16kHz, 32kHz, 48kHz, 11.025kHz, 22.05kHz, 44.1kHz.
# - RECORD_SECONDS:录音秒数

# ### 核心函数1:
# 
# rec函数的作用是录音处理。

# In[ ]:


def rec(file_name):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("开始录音,请说话...")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("录音结束!")
    
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return file_name


# ### 核心函数2:
# 
# audio_to_text函数的作用是将录音转化为文字。

# In[ ]:


def audio_to_text(wav_file):
    with open(wav_file, 'rb') as fp:
        file_context = fp.read()
    print("正在识别语音...")
    res = client.asr(file_context, 'wav', 16000, {
        'dev_pid': 1536,
    })
    if (res["err_msg"]=="success."):
        res_str = res.get("result")[0]
    else:
        res_str = "错误，没有识别出任何内容！"
    return res_str


# ### 核心函数3:
# 
# tts函数的作用是将文字result转为语音，并且朗读出来。

# In[ ]:


def tts(txt):
    result = client.synthesis(txt, 'zh', 1, {'vol': 5,})
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('auido.mp3', 'wb') as f:
            f.write(result)
        os.system('play auido.mp3')


# ### 开始工作
# 
# 描述：当用户说“床前明月光”，虚谷号会说“疑是地上霜”，如果接上音箱，将听到女声的朗读。

# In[ ]:


#添加诗词库，用户读前一句（奇数），机器对出下一句（偶数）
shici = ['床前明月光', '疑是地上霜', '举头望明月','低头思故乡']
shici.extend(['大漠沙如雪', '燕山月似钩', '何当金络脑','快走踏清秋'])
#可以用类似VB的语法，采用+的方式
shici=shici + ['小时不识月','呼作白玉盘','又疑瑶台镜','飞在青云端']
shici=shici + ['天苍苍野茫茫','风吹草低见牛羊']
shici=shici + ['少壮不努力','老大徒伤悲']
#输出列表
print(shici)


# In[ ]:


from xugu import Pin # 从 xugu 库中导入 Pin类
import time # 导入时间模块
p = Pin(2, Pin.IN) 
tts("我是吟诗作对机器人，来考考我吧。")
while True:
    value=p.read_digital() # 读取引脚电平信息,赋值给 value
    #print(value) # 将value的值打印到终端上
    if (value==1):
        tts("请在2秒钟后朗读诗句。")
        ret_s = audio_to_text(rec("input.wav"))
        print(ret_s)
        for i in range(len(shici)//2):  
            #print(shici[i*2-1])
            if shici[i*2] in ret_s:
                back=shici[i*2+1]
                break
            else:
                back="在下才疏学浅，甘拜下风。"
        print(back)  
        #输出语音
        tts(back)
    time.sleep(0.3) # 等待0.3秒，按下按钮时间过长，可能会激活两次判断。


# ### 拓展思考：
# 
# 1.请给“诗词库”（变量shici）增加新的数据，使其可以支持更多的回答。
# 
# 2.修改变量shici的内容，让这个程序可以在其他的特定场合工作。
# 

# In[ ]:




