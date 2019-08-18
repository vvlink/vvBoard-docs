from dhtc import DHT #从dhtc库中导入DHT类
import time #导入时间模块
dht = DHT() #创建DHT对象，初始化DHT类
test = 12 #计数
while test > 0:
	t = dht.read() #将读取到的温湿度的值保存在变量t中
	print(t) #将温湿度的值打印到终端
	time.sleep(2.5) #睡眠2.5秒
	test-=1 #计数自减1
