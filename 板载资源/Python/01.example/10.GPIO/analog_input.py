from xugu import Pin, SerialMgt # 从 xugu 库中导入 Pin、SerialMgt 类
p = Pin("A0", Pin.ANALOG) # 初始化 A0 引脚,设置为输入模式
ser = SerialMgt() #初始化串口
value = p.read_analog() #读取 A0 引脚的电压值
ser.write(str(value).encode()) # 将value的值写入串口
