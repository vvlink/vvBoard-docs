from xugu import Pin #从xugu库中导入Pin类
import time #导入时间模块
potentiometer_pin = "a0" #定义模拟输入引脚
potentiometer = Pin(potentiometer_pin,Pin.ANALOG) #创建Pin对象
test = 30 #计数
while test > 0:
    value = potentiometer.read_analog() #读取A0脚的模拟输入值
    print(value) #将读取的值打印到终端
    time.sleep(1) #睡眠1秒
    test -= 1 #计数自减1
