# mpremote connect /dev/tty.usbmodem0000000000001 cp main.py :

import uasyncio
from micropython import const
from machine import Pin, I2C
from i2c_device import I2CDevice
from bmx160 import BMX160_I2C

BMX160_I2C_ADRR = const(0x68)


async def read_bmx160(bmx, period_ms):
    while True:
        print(f"gyro: {bmx.gyro}, accel: {bmx.accel}, mag: {bmx.mag}")
        await uasyncio.sleep_ms(period_ms)


async def main(bmx):
    await uasyncio.sleep_ms(100)  # conservative warm-up time
    uasyncio.create_task(read_bmx160(bmx, 200))
    await uasyncio.sleep(60 * 10)  # run this program for 10 minutes


i2c = I2C(1, scl=Pin("SCL"), sda=Pin("SDA"))
device = I2CDevice(i2c, BMX160_I2C_ADRR)
bmx = BMX160_I2C(device)

uasyncio.run(main(bmx))
