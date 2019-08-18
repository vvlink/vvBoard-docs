from mtx import MTX
import time
mtx = MTX()
val = "123abc"
while True:
    if mtx.burn_complete:
        mtx.write(val)
    time.sleep(6)
