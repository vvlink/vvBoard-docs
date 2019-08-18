from pyfirmata import Arduino, util
from time import sleep
board = Arduino('/dev/ttyS1')
while True:
    board.digital[9].write(1)
    sleep(1)
    board.digital[9].write(0)
    sleep(1)
