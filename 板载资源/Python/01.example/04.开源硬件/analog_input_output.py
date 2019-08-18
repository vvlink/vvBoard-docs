from xugu import Pin                     #从xugu库中导入Pin类
p = Pin("A0",Pin.ANALOG)                 #创建Pin对象,并初始化A0引脚
p10 = Pin(10,Pin.PWM)                    #创建Pin对象，并初始化10号引脚
p10.write_analog(int(p.read_analog()/4)) #根据A0的模拟电位值，设置对应引脚的电位值
