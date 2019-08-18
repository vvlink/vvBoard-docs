from xugu import Pin # 从 xugu 库中导入 Pin 类
p = Pin(10, Pin.OUT) # 初始化 Pin 类,将 10 号数字引脚设置为输出模式
# p = Pin(“D10”, Pin.OUT)
p.write_digital(0) # 设置 10 号引脚为低电平
