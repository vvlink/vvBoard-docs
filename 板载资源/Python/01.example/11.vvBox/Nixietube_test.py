from tm1637 import TM1637
import time
tm1637 = TM1637()
val = "0123456789"
com = "0123"
i = 0
j = 0
tm1637.clearDisplay()
while True:
    for letter in com:
        for letter in val:
            tm1637.display(com[i],val[j])
            time.sleep(1)
            j += 1
        i += 1
        j = 0
    i = 0
    tm1637.clearDisplay()
    time.sleep(1)
