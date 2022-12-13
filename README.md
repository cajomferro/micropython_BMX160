# micropython_BMX160
This is a fork from CircuitPython_BMX160 that works with Micropython without requiring other libraries.

For reference, see the datasheet for the device [here](https://ae-bst.resource.bosch.com/media/_tech/media/datasheets/BST-BMX160-DS000.pdf)

THIS IS STILL WORK IN PROGRESS. USE AT YOUR OWN RISK.

## Example setup and usage:

```python
import time
from micropython import const
from machine import I2C
from i2c_device import I2CDevice
from bmx160 import BMX160_I2C
 
 # set up BMX160 through I2C # note: SPI is not currently supported
i2c = I2C(1, scl=Pin("SCL"), sda=Pin("SDA"))
device = I2CDevice(i2c, const(0x68))
bmx = BMX160_I2C(device)

# conservative warm-up time
time.sleep(0.1) 

# Just call e.g. bmx.gyro to read the gyro value
print("gyroscope:", bmx.gyro)
print("accelerometer:", bmx.accel)
print("magnetometer:", bmx.mag)
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
