from xugu import Pin # 从 xugu 库中导入 Pin 类
p = Pin(10, Pin.OUT) # 初始化 Pin 类,将 10 号数字引脚设置为输出模式
#等价的写法: p = Pin(“D10”, Pin.OUT)
p.write_digital(1) # 设置 10 号引脚为高电平
