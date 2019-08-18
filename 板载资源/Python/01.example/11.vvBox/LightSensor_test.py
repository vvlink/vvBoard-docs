from xugu import Pin #从xugu库中导入Pin类
import time #导入时间模块
lightSensor_pin = "a1" #定义模拟输入引脚
led_pin = 11 #定义LED控制引脚
lightSensor = Pin(lightSensor_pin,Pin.ANALOG) #创建Pin对象
led = Pin(led_pin,Pin.OUT) #创建Pin对象
test = 30 #计数
while test > 0:
    value = lightSensor.read_analog() #读取A1脚的模拟输入值
    print(value)
    if value > 200: #判断A1脚获取的值是否大于200
        led.write_digital(1) #点亮蓝色的LED灯
    else:
        led.write_digital(0) #熄灭LED灯
    time.sleep(1) #睡眠1秒
    test -= 1 #计数自减1
led.write_digital(0)
