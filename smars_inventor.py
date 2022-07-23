from inventor import Inventor2040W, NUM_LEDS
from time import sleep
import pimoroni_i2c
from vl53l1x import VL53L1X
import breakout_vl53l5cx

PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}

i2c = pimoroni_i2c.PimoroniI2C(**PINS_BREAKOUT_GARDEN, baudrate=2_000_000)
print(i2c.scan())
board = Inventor2040W()

# vl53l1x = VL53L0X(i2c)
vl53l1x = VL53L1X(i2c)

while True:
        print(vl53l1x.distance)
        sleep(0.5)

BRIGHTNESS = 0.4
UPDATES = 50
SPEED = 50



def led_test(cycles):
    global offset, SPEED, BRIGHTNESS, NUM_LEDS
    offset = 0.0
    print(f'NUM_LEDS:{NUM_LEDS}')
    
    for _ in range(1, cycles):
        offset += SPEED / 1000.0
        for i in range(NUM_LEDS):
            hue = float(i) / NUM_LEDS
            board.leds.set_hsv(i, hue+offset, 1.0, BRIGHTNESS)
        print(f'offset: {offset}')
        sleep(1.0 / UPDATES)
        
        
def motor_test(duration):
    for m in board.motors:
        m.enable()
    sleep(0.1)

    for m in board.motors:
        m.full_negative()
    sleep(duration)

    for m in board.motors:
        m.stop()
    sleep(0.1)

# motor_test(5)
# led_test(1000)
