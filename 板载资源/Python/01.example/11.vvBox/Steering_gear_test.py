from xugu import * #倒入xugu库
import time #倒入时间模块
servo = Servo(3) #选择soc控制引脚
test = 10 #计数
l = [180,0] #角度列表
while test>0:
	servo.write_angle(l[0]) #默认写入列表的第一个参数
	l = l[: : -1] #列表参数交换
	time.sleep(1) #休眠一秒
	test-=1 #计数自减1
