import time  # 导入time模块
from xugu import LED  # 从xugu库中导入LED类
led = LED(13)  # 初始化LED类
while True:   # 用循环实现持续地开灯关灯，到达闪烁的效果
    led.on()  # 点亮连接13号引脚的LED灯
    time.sleep(1) # 持续1秒
    led.off()  # 关闭LED灯
    time.sleep(1)  # 持续1秒
