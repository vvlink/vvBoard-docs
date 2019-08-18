from xugu import Pin  # 从xugu库中导入Pin类
p = Pin(10, Pin.OUT)  # 初始化10号引脚设置为输出模式
p.write_analog(128)  # 给引脚设置模拟值128
