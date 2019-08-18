from xugu import * #导入xugu库
import time #导入时间模块
pin_r = Pin(9,Pin.OUT) #选择soc控制引脚
pin_g = Pin(10,Pin.OUT) #选择soc控制引脚
pin_b = Pin(11,Pin.OUT) #选择soc控制引脚
test = 20 #计数
l = [0,1] #IO口高低电平列表
while test > 0:
	pin_r.write_digital(l[0]) #默认写入列表的第一个参数
	time.sleep(1) #休眠一秒
	pin_g.write_digital(l[0]) #默认写入列表的第一个参数
	time.sleep(1) #休眠一秒
	pin_b.write_digital(l[0]) #默认写入列表的第一个参数
	l = l[: : -1] #列表参数交换
	time.sleep(1) #休眠一秒
	test-=1 #计数自减1
