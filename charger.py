from adafruit_bus_device.i2c_device import I2CDevice

default_addr = 0x4B

_REG_CHARGE_STATUS = 0x0C

class MP2731:
    def __init__(self, i2c, addr=default_addr):
        self._device = I2CDevice(i2c, addr)

    def read_u8(self,reg):
        self._addr = reg
        with self._device as i2c:
            i2c.write_then_readinto(self._addr,self._buf)
            return self._buf[0]

    @property
    def charge_status(self):
        return self.read_u8(_REG_CHARGE_STATUS)