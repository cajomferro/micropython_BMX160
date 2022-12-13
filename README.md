# micropython_BMX160
This is a fork from CircuitPython_BMX160 that works with Micropython without requiring other libraries.

For reference, see the datasheet for the device [here](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmx160-ds0001.pdf).

THIS IS STILL WORK IN PROGRESS. USE AT YOUR OWN RISK.

## Example setup and usage

Upload the three modules: `i2c_device.py`, `bmx160.py`, and `main.py`.

Note that you might need to adjust some I2C settings depending on your target Micropython board. 
Check the `main.py` file.

```python
# Basic usage (use the Makefile below to run the example)
from micropython import const
from machine import Pin, I2C
from i2c_device import I2CDevice
from bmx160 import BMX160_I2C

BMX160_I2C_ADRR = const(0x68)
i2c = I2C(1, scl=Pin("SCL"), sda=Pin("SDA"))
device = I2CDevice(i2c, BMX160_I2C_ADRR)
bmx = BMX160_I2C(device)
print(f"gyro: {bmx.gyro}, accel: {bmx.accel}, mag: {bmx.mag}")
```

### Running the example `app.py`

In order to use the `Makefile` you will need to install the [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) library on your host machine first.
As an alternative use any serial app (e.g., screen).

```python
# From host machine:
$: make upload # make upload DEFAULT_PORT=YOUR_SERIAL_PORT_HERE to override
$: make console #  make console DEFAULT_PORT=YOUR_SERIAL_PORT_HERE to override

# now inside REPL
>>> CTRL-D # reset
MPY: soft reboot
gyro: (-0.06103516, 0.5340576, 0.7629395), accel: (0.0, 0.0, 0.0), mag: (5.0625, 17.5625, 22.6875)
gyro: (-0.2593994, 0.4272461, 0.869751), accel: (0.0, 0.0, 0.0), mag: (7.0625, 20.0625, 22.5625)
gyro: (-0.213623, 0.3814697, 0.9307861), accel: (-3.98874, 4.412514, -7.970297), mag: (6.0625, 18.5625, 22.9375)
gyro: (-0.2288818, 0.3967285, 0.9002686), accel: (-4.055778, 4.486734, -8.094796), mag: (5.5625, 17.5625, 22.6875)
gyro: (-0.2288818, 0.3662109, 0.9460449), accel: (-4.050989, 4.48434, -8.09719), mag: (6.5625, 19.5625, 22.8125)
gyro: (-0.213623, 0.3814697, 0.9307861), accel: (-4.053383, 4.486734, -8.087613), mag: (6.5625, 19.0625, 22.8125)
gyro: (-0.2593994, 0.3967285, 0.9155273), accel: (-4.050989, 4.491522, -8.092402), mag: (5.5625, 18.5625, 23.0625)
gyro: (-0.2746582, 0.3662109, 0.8850098), accel: (-4.050989, 4.489128, -8.085219), mag: (5.5625, 18.5625, 23.0625)
gyro: (-0.213623, 0.3662109, 0.9002686), accel: (-4.053383, 4.489128, -8.092402), mag: (6.0625, 18.5625, 22.9375)
gyro: (-0.2288818, 0.3356934, 0.9155273), accel: (-4.046201, 4.48434, -8.092402), mag: (6.0625, 17.5625, 22.8125)
>>> CTRL-C # stop
>>> Ctrl-] # exit shell (CTRL-´ on latin keyboard) 
```

## Sensors

A call to e.g. `bmx.gyro` returns a tuple: `(gyro_x, gyro_y, gyro_z)`.

#### Gyroscope
- getter: `bmx.gyro`
- units: °/sec
- default range: ±250 °/sec
- default data-rate: 25 Hz

#### Magnetometer
- getter: `bmx.mag`
- units: µT
- fixed range: ±1150µT (x/y) ±2500µT (z) (see Section 1.2 Table 4)
- default data-rate: 25 Hz
- default mode: low-power (see Section 2.2.1.2 and Table 11)

#### Accelerometer
- getter: `bmx.accel`
- units: m/s (note: this differs from the .c implementation, which returns in g)
- default range: ±2g
- default data-rate: 25 Hz

#### Temperature Sensor
- getter: `bmx.temp` / `bmx.temperature`
- units: °C

#### Timer
- resolution: 39µs
- resets every 654.311385s (see section 2.3.1 Table 12)

#### Other things
- Access error register: `bmx.error_status` returns a binary string following Section 2.11.2
- PMU (power management unit) mode fo each device with `bmx.status_acc_pmu`, `bmx.status_gyr_pmu`, `bmx.status_mag_pmu`
- Status register: `bmx.status` returns a binary string following Section 2.11.6, individual bits of which can also be gotten (as booleans) with getters named after the entries in that table. E.g. `bmx.drdy_acc`
- Note: Right now, encountering an *chip error* while e.g. changing settings, simply prints a warning.
