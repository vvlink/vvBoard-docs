import time # 导入 time 模块
from xugu import Pin # 从 xugu 库中导入 Pin 类
led = Pin(13, Pin.OUT) # 初始化 Pin 类
# 等价的写法:led = Pin(“D13”, pin.OUT)
while True:
    # #用循环实现持续地开灯关灯,到达闪烁的效果
    led.write_digital(1) # 点亮连接 13 号引脚的 LED 灯
    time.sleep(1) # 持续 1 秒
    led.write_digital(0) # 关闭 LED 灯
    time.sleep(1) # 持续 1 秒
