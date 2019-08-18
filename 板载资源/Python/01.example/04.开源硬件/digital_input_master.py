from xugu import Pin, SerialMgt # 从 xugu 库中导入 Pin、SerialMgt 类
import time # 导入时间模块
p = Pin(4, Pin.IN) # 初始化 4 号引脚,设置为数字输入模式
ser = SerialMgt() #初始化串口
while True:
    value=p.read_digital() # 读取 4 号引脚电平信息,赋值给 value
    print(value) # 将value的值打印到终端上
    ser.write(str(value).encode()) # 将value的值写入到串口
    time.sleep(0.1) # 持续100ms
