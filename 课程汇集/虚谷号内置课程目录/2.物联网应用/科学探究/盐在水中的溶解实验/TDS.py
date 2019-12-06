import siot  #导入siot库
import time  #导入time库
from xugu import Pin # 从 xugu 库中导入 Pin类

p = Pin("A0", Pin.ANALOG) # 初始化 A0 引脚,设置为输入模式

SERVER = "192.168.0.101"        #MQTT服务器IP
CLIENT_ID = ""              #在SIoT上，CLIENT_ID可以留空
IOT_pubTopic  = 'DIY/TEST01'   #“topic”为“项目名称/设备名称”
IOT_UserName ='scope'        #用户名
IOT_PassWord ='scope'     #密码

siot.init(CLIENT_ID, SERVER, user=IOT_UserName, password=IOT_PassWord) #将上述配置信息作为siot客户端参数
    
siot.connect() #连接siot服务器
while True:
  TDS = p.read_analog() #读取 A0 引脚的模拟量并赋值给变量TDS
  siot.publish(IOT_pubTopic, "%d"%TDS) #发布检测到的TDS值
  time.sleep(1) #等待1秒
