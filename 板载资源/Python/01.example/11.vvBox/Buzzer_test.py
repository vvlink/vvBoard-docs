from xugu import * #导入xugu库
import time #导入时间模块
buzzer = Pin(12,Pin.OUT) #创建Pin对象
test = 30 #计数
while test > 0:
    buzzer.write_digital(1) #拉高soc的12脚
    time.sleep(0.1) #睡眠100毫秒
    buzzer.write_digital(0) #拉低soc的12脚
    time.sleep(0.1)
    test -= 1 #计数自减1
buzzer.write_digital(0) #拉低soc的12脚
