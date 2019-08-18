from xugu import Pin, XuguLog, SerialMgt # 从 xugu 库中导入 Pin、XuguLog、SerialMgt 类
import time # 导入时间模块
test = 20 # 计数
p = Pin("A0", Pin.ANALOG) # 初始化 A0 引脚,设置为输入模式
ser = SerialMgt() #初始化串口
f=XuguLog('read_analog_20_times.log') #当不指定路径时，log文件保存在与digital_input.py同级路径下
#f=XuguLog('/home/scope/analog_input.log') # 初始化日志对象，当指定路径时log文件保存在指定路径下
while test > 0:
    value = p.read_analog() #读取 A0 引脚的电压值
    f. write(str(value)) # 将变量 value 写入到日志文件中
    print(value) # 将value的值打印到终端
    ser.write(str(value).encode()) # 将value的值写入串口
    test -= 1 # 计数自减1
    time.sleep(0.5) # 持续500ms
