from adafruit_bus_device.i2c_device import I2CDevice

default_i2c_address = 0x36


_V_LSB_MV = 1.25/16.0
_I_LSB_MA = 52.083/1000.0
_CAP_LSB_MAH = 1.0/6.0
_TIME_LSB_S = 5.625

_REG_STATUS = 0x00
_REG_REP_CAP = 0x05
_REG_REP_SOC = 0x06
_REG_INT_TEMP=0x08
_REG_VCELL=0x09
_REG_CURRENT=0x0A
_REG_AVG_CURRENT=0x0B
_REG_FULL_CAP_REP=0x10
_REG_TTE= 0x11
_REG_CYCLES=0x17
_REG_TTF=0x20
_REG_FSTAT=0x3D
_REG_VFSOC=0xFF

class MAX17262H:
    def __init__(self, i2c_bus, address=default_i2c_address):
        self.i2c_device = I2CDevice(i2c_bus, address)
        self.addr = bytearray(1)
        self.buffer = bytearray(2)
    def read_register(self, register):
        self.addr[0] = register
        with self.i2c_device as i2c:
            i2c.write(self.addr)
            i2c.readinto(self.buffer)
        return (self.buffer[0] << 8) | self.buffer[1]
    def read_i16(self, register):
        value = self.read_register(register)
        return value - 0x10000   if value & 0x8000 else value
    def voltage_mv(self):
        return self.read_register(_REG_VCELL) * _V_LSB_MV
    def current_ma(self):
        return self.read_i16(_REG_CURRENT) * _I_LSB_MA
    def average_current_ma(self):
        return self.read_i16(_REG_AVG_CURRENT) * _I_LSB_MA
    def remaining_capacity_mah(self):
        return self.read_register(_REG_REP_CAP) * _CAP_LSB_MAH  
    def full_capacity_mah(self):
        return self.read_register(_REG_FULL_CAP_REP) * _CAP_LSB_MAH
    def state_of_charge(self):
        return self.read_register(_REG_REP_SOC) / 256.0
    def vfsoc(self):
        return self.read_register(_REG_VFSOC) / 256.0
    def remaining_capacity_percent(self):
        return self.read_register(_REG_REP_SOC) / 256.0
    def vfstatus(self):
        return self.read_register(_REG_FSTAT)
    def read_temperature_c(self):
        raw_temp = self.read_register(_REG_INT_TEMP)
        return (raw_temp * 0.1) - 273.15
    

