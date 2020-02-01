import time
try:
    import struct
except ImportError:
    import ustruct as struct

from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_bus_device.spi_device import SPIDevice
from micropython import const

# Chip ID
BMX160_CHIP_ID = const(0xD8)

# Soft reset command
BMX160_SOFT_RESET_CMD      = const(0xb6)
BMX160_SOFT_RESET_DELAY_MS = 0.001

# Command
BMX160_COMMAND_REG_ADDR    = const(0x7E)

# BMX160 Register map
BMX160_CHIP_ID_ADDR        = const(0x00)
BMX160_ERROR_REG_ADDR      = const(0x02)
BMX160_PMU_STATUS_ADDR     = const(0x03)
BMX160_SENSOR_TIME_ADDR    = const(0x18)
BMX160_MAG_DATA_ADDR       = const(0x04)
BMX160_GYRO_DATA_ADDR      = const(0x0C)
BMX160_ACCEL_DATA_ADDR     = const(0x12)
BMX160_STATUS_ADDR         = const(0x1B)
BMX160_INT_STATUS_ADDR     = const(0x1C)
BMX160_FIFO_LENGTH_ADDR    = const(0x22)
BMX160_FIFO_DATA_ADDR      = const(0x24)
BMX160_ACCEL_CONFIG_ADDR   = const(0x40)
BMX160_ACCEL_RANGE_ADDR    = const(0x41)
BMX160_GYRO_CONFIG_ADDR    = const(0x42)
BMX160_GYRO_RANGE_ADDR     = const(0x43)
BMX160_MAG_ODR_ADDR        = const(0x44)
BMX160_FIFO_DOWN_ADDR      = const(0x45)
BMX160_FIFO_CONFIG_0_ADDR  = const(0x46)
BMX160_FIFO_CONFIG_1_ADDR  = const(0x47)
# BMX160_MAG_IF_0_ADDR       = const(0x4B)
BMX160_MAG_IF_0_ADDR       = const(0x4C)
BMX160_MAG_IF_1_ADDR       = const(0x4D)
BMX160_MAG_IF_2_ADDR       = const(0x4E)
BMX160_MAG_IF_3_ADDR       = const(0x4F)
BMX160_INT_ENABLE_0_ADDR   = const(0x50)
BMX160_INT_ENABLE_1_ADDR   = const(0x51)
BMX160_INT_ENABLE_2_ADDR   = const(0x52)
BMX160_INT_OUT_CTRL_ADDR   = const(0x53)
BMX160_INT_LATCH_ADDR      = const(0x54)
BMX160_INT_MAP_0_ADDR      = const(0x55)
BMX160_INT_MAP_1_ADDR      = const(0x56)
BMX160_INT_MAP_2_ADDR      = const(0x57)
BMX160_INT_DATA_0_ADDR     = const(0x58)
BMX160_INT_DATA_1_ADDR     = const(0x59)
BMX160_INT_LOWHIGH_0_ADDR  = const(0x5A)
BMX160_INT_LOWHIGH_1_ADDR  = const(0x5B)
BMX160_INT_LOWHIGH_2_ADDR  = const(0x5C)
BMX160_INT_LOWHIGH_3_ADDR  = const(0x5D)
BMX160_INT_LOWHIGH_4_ADDR  = const(0x5E)
BMX160_INT_MOTION_0_ADDR   = const(0x5F)
BMX160_INT_MOTION_1_ADDR   = const(0x60)
BMX160_INT_MOTION_2_ADDR   = const(0x61)
BMX160_INT_MOTION_3_ADDR   = const(0x62)
BMX160_INT_TAP_0_ADDR      = const(0x63)
BMX160_INT_TAP_1_ADDR      = const(0x64)
BMX160_INT_ORIENT_0_ADDR   = const(0x65)
BMX160_INT_ORIENT_1_ADDR   = const(0x66)
BMX160_INT_FLAT_0_ADDR     = const(0x67)
BMX160_INT_FLAT_1_ADDR     = const(0x68)
BMX160_FOC_CONF_ADDR       = const(0x69)
BMX160_CONF_ADDR           = const(0x6A)

BMX160_ACCEL_BW_NORMAL_AVG4 = const(0x02)
BMX160_GYRO_BW_NORMAL_MODE  = const(0x02)

BMX160_SELF_TEST_ADDR                = const(0x6D)
# Self test configurations
BMX160_ACCEL_SELF_TEST_CONFIG        = const(0x2C)
BMX160_ACCEL_SELF_TEST_POSITIVE_EN   = const(0x0D)
BMX160_ACCEL_SELF_TEST_NEGATIVE_EN   = const(0x09)
BMX160_ACCEL_SELF_TEST_LIMIT         = const(8192)

# Power mode settings
# Accel power mode
BMX160_ACCEL_NORMAL_MODE             = const(0x11)
BMX160_ACCEL_LOWPOWER_MODE           = const(0x12)
BMX160_ACCEL_SUSPEND_MODE            = const(0x10)

# Gyro power mode
BMX160_GYRO_SUSPEND_MODE             = const(0x14)
BMX160_GYRO_NORMAL_MODE              = const(0x15)
BMX160_GYRO_FASTSTARTUP_MODE         = const(0x17)

# Mag power mode
BMX160_MAG_SUSPEND_MODE              = const(0x18)
BMX160_MAG_NORMAL_MODE               = const(0x19)
BMX160_MAG_LOWPOWER_MODE             = const(0x1A)

# Accel Range
BMX160_ACCEL_RANGE_2G                = const(0x03)
BMX160_ACCEL_RANGE_4G                = const(0x05)
BMX160_ACCEL_RANGE_8G                = const(0x08)
BMX160_ACCEL_RANGE_16G               = const(0x0C)

# Gyro Range
BMX160_GYRO_RANGE_2000_DPS           = const(0x00)
BMX160_GYRO_RANGE_1000_DPS           = const(0x01)
BMX160_GYRO_RANGE_500_DPS            = const(0x02)
BMX160_GYRO_RANGE_250_DPS            = const(0x03)
BMX160_GYRO_RANGE_125_DPS            = const(0x04)


# Delay in ms settings
BMX160_ACCEL_DELAY_MS                = const(5)
BMX160_GYRO_DELAY_MS                 = const(81)
BMX160_ONE_MS_DELAY                  = const(1)
BMX160_MAG_COM_DELAY                 = const(10)
BMX160_GYRO_SELF_TEST_DELAY          = const(20)
BMX160_ACCEL_SELF_TEST_DELAY         = const(50)

# Output Data Rate settings
# Accel Output data rate
BMX160_ACCEL_ODR_RESERVED            = const(0x00)
BMX160_ACCEL_ODR_0_78HZ              = const(0x01)
BMX160_ACCEL_ODR_1_56HZ              = const(0x02)
BMX160_ACCEL_ODR_3_12HZ              = const(0x03)
BMX160_ACCEL_ODR_6_25HZ              = const(0x04)
BMX160_ACCEL_ODR_12_5HZ              = const(0x05)
BMX160_ACCEL_ODR_25HZ                = const(0x06)
BMX160_ACCEL_ODR_50HZ                = const(0x07)
BMX160_ACCEL_ODR_100HZ               = const(0x08)
BMX160_ACCEL_ODR_200HZ               = const(0x09)
BMX160_ACCEL_ODR_400HZ               = const(0x0A)
BMX160_ACCEL_ODR_800HZ               = const(0x0B)
BMX160_ACCEL_ODR_1600HZ              = const(0x0C)
BMX160_ACCEL_ODR_RESERVED0           = const(0x0D)
BMX160_ACCEL_ODR_RESERVED1           = const(0x0E)
BMX160_ACCEL_ODR_RESERVED2           = const(0x0F)

# Gyro Output data rate
BMX160_GYRO_ODR_RESERVED             = const(0x00)
BMX160_GYRO_ODR_25HZ                 = const(0x06)
BMX160_GYRO_ODR_50HZ                 = const(0x07)
BMX160_GYRO_ODR_100HZ                = const(0x08)
BMX160_GYRO_ODR_200HZ                = const(0x09)
BMX160_GYRO_ODR_400HZ                = const(0x0A)
BMX160_GYRO_ODR_800HZ                = const(0x0B)
BMX160_GYRO_ODR_1600HZ               = const(0x0C)
BMX160_GYRO_ODR_3200HZ               = const(0x0D)


# Auxiliary sensor Output data rate
BMX160_MAG_ODR_RESERVED              = const(0x00)
BMX160_MAG_ODR_0_78HZ                = const(0x01)
BMX160_MAG_ODR_1_56HZ                = const(0x02)
BMX160_MAG_ODR_3_12HZ                = const(0x03)
BMX160_MAG_ODR_6_25HZ                = const(0x04)
BMX160_MAG_ODR_12_5HZ                = const(0x05)
BMX160_MAG_ODR_25HZ                  = const(0x06)
BMX160_MAG_ODR_50HZ                  = const(0x07)
BMX160_MAG_ODR_100HZ                 = const(0x08)
BMX160_MAG_ODR_200HZ                 = const(0x09)
BMX160_MAG_ODR_400HZ                 = const(0x0A)
BMX160_MAG_ODR_800HZ                 = const(0x0B)

# Accel, gyro and aux. sensor length and also their combined length definitions in FIFO
BMX160_FIFO_G_LENGTH                 = const(6)
BMX160_FIFO_A_LENGTH                 = const(6)
BMX160_FIFO_M_LENGTH                 = const(8)
BMX160_FIFO_GA_LENGTH                = const(12)
BMX160_FIFO_MA_LENGTH                = const(14)
BMX160_FIFO_MG_LENGTH                = const(14)
BMX160_FIFO_MGA_LENGTH               = const(20)

# I2C address
BMX160_I2C_ADDR            = const(0x68)
BMX160_I2C_ALT_ADDR        = const(0x69)  # alternate address
# Interface settings
BMX160_SPI_INTF            = const(1)
BMX160_I2C_INTF            = const(0)
BMX160_SPI_RD_MASK         = const(0x80)
BMX160_SPI_WR_MASK         = const(0x7F)

# Error related
BMX160_OK                  = const(0)

class BMX160:
    """
    Driver for the BMX160 accelerometer, magnetometer, gyroscope.

    In the buffer, bytes are allocated as follows:
        - mag 0-5
        - rhall 6-7 (not relevant?)
        - gyro 8-13
        - accel 14-19
        - sensor time 20-22
    """

    _BUFFER = bytearray(40)
    _smallbuf = bytearray(6)

    _gyro_bandwidth = NORMAL
    _gyro_powermode = NORMAL
    _gyro_odr = 25    # Hz
    _gyro_range = 250 # deg/sec

    _accel_bandwidth = NORMAL
    _accel_powermode = NORMAL
    _accel_odr = 25  # Hz
    _accel_range = 2 # g

    _mag_bandwidth = NORMAL
    _mag_powermode = NORMAL
    _mag_odr = 25    # Hz
    _mag_range = 250 # deg/sec


    def __init__(self):
        # soft reset & reboot
        self.write_u8(BMX160_COMMAND_REG_ADDR, BMX160_SOFT_RESET_CMD)
        time.sleep(BMX160_SOFT_RESET_DELAY_MS)
        # Check ID registers.
        ID = self.read_u8(BMX160_CHIP_ID_ADDR)
        if ID != BMX160_CHIP_ID:
            raise RuntimeError('Could not find BMX160, check wiring!')

        # set the default settings
        self.settings = self.default_settings()
        self.init_mag()
        self.apply_sensor_params()


    ######################## SENSOR API ########################

    def read_all(self): return self.read_bytes(BMX160_MAG_DATA_ADDR, 20, self._BUFFER)

    def query_error(self): return self.read_u8(BMX160_ERROR_REG_ADDR)

    ### ACTUAL API
    @property
    def gyro(self):  return decode_sensor(self.gyro_raw(), self._gyro_range)

    @property
    def accel(self): return decode_sensor(self.accel_raw(), self._accel_range)

    @property
    def mag(self):   return decode_sensor(self.mag_raw(), self._mag_range)

    @property
    def sensortime(self):
        tbuf = self.sensortime_raw()
        t0, t1, t2 = tbuf[:3]
        t = (t2 << 16) | (t1 << 8) | t0
        t *= 0.000039 # the time resolution is 39 microseconds
        return t


    # NOTE, these share a buffer! Can't call two in a row! Either make a wrapper for a buffer slice
    # to allow partial passing or copy the buffer to return or completely hide this API
    def gyro_raw(self):  return self.read_bytes(BMX160_GYRO_DATA_ADDR, 6, self._smallbuf)
    def accel_raw(self): return self.read_bytes(BMX160_ACCEL_DATA_ADDR, 6, self._smallbuf)
    def mag_raw(self):   return self.read_bytes(BMX160_MAG_DATA_ADDR, 6, self._smallbuf)
    def sensortime_raw(self):  return self.read_bytes(BMX160_SENSOR_TIME_ADDR, 3, self._smallbuf)

    ######################## SETTINGS RELATED ########################
    def clear_settings(self): self.settings.clear()


            # self.set_sensor_param("mag", key, val)

    def default_settings(self):
        """
        Basically copied from the C version.
        """
        accel_settings = {
                          "bw": BMX160_ACCEL_BW_NORMAL_AVG4,
                          "odr": BMX160_ACCEL_ODR_25HZ,
                          "power": BMX160_ACCEL_NORMAL_MODE,
                          # "range": BMX160_ACCEL_RANGE_2G
                          }
        gyro_settings = {
                         "bw": BMX160_GYRO_BW_NORMAL_MODE,
                         "odr": BMX160_GYRO_ODR_25HZ,
                         "power": BMX160_GYRO_NORMAL_MODE,
                         # "range": BMX160_GYRO_RANGE_2000_DPS
                         }

        mag_settings = {
                         # "bw": BMX160_MAG_BW_NORMAL_MODE,
                         # "odr": BMX160_MAG_ODR_100HZ,
                         # "power": BMX160_MAG_NORMAL_MODE,
                         # "range": BMX160_GYRO_RANGE_2000_DPS
                         }

        return {"accel": accel_settings, "gyro": gyro_settings, "mag": mag_settings}

    @property
    def gyro_range(self):
        return self._gyro_range

    @gyro_range.setter
    def gyro_range(self, range):
        """
        Set the range of the gyroscope. The possible ranges are
        2000, 1000, 500, 250, and 125 degree/second. Note, setting a value between the possible ranges
        will round *downwards*. A value of e.g. 250 means the sensor can measure +/-250 deg/sec
        """
        if range >= 2000:
            range = 2000
            bmxconst = BMX160_GYRO_RANGE_2000_DPS
        elif range >= 1000:
            range = 1000
            bmxconst = BMX160_GYRO_RANGE_1000_DPS
        elif range >= 500:
            range = 500
            bmxconst = BMX160_GYRO_RANGE_500_DPS
        elif range >= 250:
            range = 250
            bmxconst = BMX160_GYRO_RANGE_250_DPS
        else:
            range = 125
            bmxconst = BMX160_GYRO_RANGE_125_DPS

        self.write_u8(BMX160_GYRO_RANGE_ADDR, bmxconst)
        if self.query_error() == BMX160_OK:
            self._gyro_range = range

    @property
    def accel_range(self):
        return self._accel_range

    @accel_range.setter
    def accel_range(self, range):
        """
        Set the range of the accelerometer. The possible ranges are 16, 8, 4, and 2 Gs.
        Note, setting a value between the possible ranges will round *downwards*.
        A value of e.g. 2 means the sensor can measure +/-2 G
        """
        if range >= 16:
            range = 16
            bmxconst = BMX160_ACCEL_RANGE_16G
        elif range >= 8:
            range = 8
            bmxconst = BMX160_ACCEL_RANGE_8G
        elif range >= 4:
            range = 4
            bmxconst = BMX160_ACCEL_RANGE_4G
        else:
            range = 2
            bmxconst = BMX160_ACCEL_RANGE_2G

        self.write_u8(BMX160_ACCEL_RANGE_ADDR, bmxconst)
        if self.query_error() == BMX160_OK:
            self._accel_range = range

    def init_mag(self):
        # see pg 25 of: https://ae-bst.resource.bosch.com/media/_tech/media/datasheets/BST-BMX160-DS000.pdf
        self.write_u8(BMX160_COMMAND_REG_ADDR, BMX160_MAG_NORMAL_MODE)
        time.sleep(0.00065) # datasheet says wait for 650microsec
        self.write_u8(BMX160_MAG_IF_0_ADDR, 0x80)
        # put mag into sleep mode
        self.write_u8(BMX160_MAG_IF_3_ADDR, 0x01)
        self.write_u8(BMX160_MAG_IF_2_ADDR, 0x4B)
        # set x-y to regular power preset
        self.write_u8(BMX160_MAG_IF_3_ADDR, 0x04)
        self.write_u8(BMX160_MAG_IF_2_ADDR, 0x51)
        # set z to regular preset
        self.write_u8(BMX160_MAG_IF_3_ADDR, 0x0E)
        self.write_u8(BMX160_MAG_IF_2_ADDR, 0x52)
        # prepare MAG_IF[1-3] for mag_if data mode
        self.write_u8(BMX160_MAG_IF_3_ADDR, 0x02)
        self.write_u8(BMX160_MAG_IF_2_ADDR, 0x4C)
        self.write_u8(BMX160_MAG_IF_1_ADDR, 0x42)
        # Set ODR to 25 Hz
        self.write_u8(BMX160_MAG_ODR_ADDR, BMX160_MAG_ODR_25HZ)
        self.write_u8(BMX160_MAG_IF_0_ADDR, 0x00)
        # put in low power mode.
        self.write_u8(BMX160_COMMAND_REG_ADDR, BMX160_MAG_LOWPOWER_MODE)
        time.sleep(0.1) # takes this long to warm up (empirically)


    ## UTILS:
    def decode_sensor(arr, range):
        x = (arr[1] << 8) | arr[0]
        y = (arr[3] << 8) | arr[2]
        z = (arr[5] << 8) | arr[4]

        # divide by typemax(Int16) and multiply by range
        x *= range / 32768.0
        y *= range / 32768.0
        z *= range / 32768.0
        # NOTE: This may be the wrong conversion! It might need to be something like (x + typemin(Int16)) / typemin(Int16)

        return (x, y, z)



class BMX160_I2C(BMX160):
    """Driver for the BMX160 connect over I2C."""

    def __init__(self, i2c):

        try:
            self.i2c_device = I2CDevice(i2c, BMX160_I2C_ADDR)
        except:
            self.i2c_device = I2CDevice(i2c, BMX160_I2C_ALT_ADDR)

        super().__init__()

    def read_u8(self, address):
        with self.i2c_device as i2c:
            self._BUFFER[0] = address & 0xFF
            i2c.write_then_readinto(self._BUFFER, self._BUFFER, out_end=1, in_start=1, in_end=2)
        return self._BUFFER[1]

    def read_bytes(self, address, count, buf):
        with self.i2c_device as i2c:
            buf[0] = address & 0xFF
            i2c.write_then_readinto(buf, buf, out_end=1, in_end=count)
        return buf

    def write_u8(self, address, val):
        with self.i2c_device as i2c:
            self._BUFFER[0] = address & 0xFF
            self._BUFFER[1] = val & 0xFF
            i2c.write(self._BUFFER, end=2, stop=True)


class BMX160_SPI(BMX160):
    """Driver for the BMX160 connect over SPI."""
    def __init__(self, spi, cs):
        self.i2c_device = SPIDevice(spi, cs)
        super().__init__()

    def read_u8(self, address):
        with self.i2c_device as spi:
            self._BUFFER[0] = (address | 0x80) & 0xFF
            spi.write(self._BUFFER, end=1)
            spi.readinto(self._BUFFER, end=1)
        return self._BUFFER[0]

    def read_bytes(self, address, count, buf):
        with self.i2c_device as spi:
            buf[0] = (address | 0x80) & 0xFF
            spi.write(buf, end=1)
            spi.readinto(buf, end=count)
        return buf

    def write_u8(self, address, val):
        with self.i2c_device as spi:
            self._BUFFER[0] = (address & 0x7F) & 0xFF
            self._BUFFER[1] = val & 0xFF
            spi.write(self._BUFFER, end=2)

