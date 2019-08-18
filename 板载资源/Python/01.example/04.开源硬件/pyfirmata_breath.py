import time
import pyfirmata

delay = 0.3
brightness = 0

board = pyfirmata.Arduino("/dev/ttyS1")

led = board.get_pin('d:9:p')            
while True:
# increase
    for i in range(0, 10):
        brightness = brightness + 0.1
        print("Setting brightness to %s" % brightness)
        led.write(brightness)
        board.pass_time(delay)

# decrease
    for i in range(0, 10):
        print("Setting brightness to %s" % brightness)
        led.write(brightness) 
        brightness = brightness - 0.1     
        board.pass_time(delay)
