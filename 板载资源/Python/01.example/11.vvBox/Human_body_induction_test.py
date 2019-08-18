from xugu import Pin #从xugu库中导入Pin类
import time #导入时间模块
pin = Pin(4,Pin.IN) #创建Pin对象
test = 30
while test>0:
	value = pin.read_digital() #读取对应Pin脚的电平值
	if value:
		print("find human!!!") #电平为1代表发现人
	else:
		print("no human!!!") #电平为0代表没发现人
	time.sleep(1) #睡眠1秒
	test-=1
