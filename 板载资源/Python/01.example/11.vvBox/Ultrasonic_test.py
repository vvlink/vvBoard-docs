from dhtc import HC #从dhtc模块中导入HC类
import time #导入时间模块
hc = HC() #创建HC对象
test = 30 #计数
while test>0:
	l = hc.read() #读取距离
	print(l) #在终端上输出距离
	time.sleep(1) #睡眠一秒
	test-=1 #计数自减1