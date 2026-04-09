class VirtualI2CDevice:
    def __init__(self, address):
        if address != 0x48:
            raise RuntimeError(
                f"Error: Device not found at I2C address 0x{address:02X}"
            )
        self.address = address
        self.registers = {
            0x00: 0x1A,  # Temperature High Byte
            0x01: 0x4B,  # Temperature Low Byte
            0x02: 0x01,  # Config Register
        }

    def read_byte(self, reg):
        if reg not in self.registers:
            raise RuntimeError(f"Error: Invalid Register Access 0x{reg:02X}")
        return self.registers[reg]


class SensorTester:
    def __init__(self):
        self.sensor_addr = 0x48
        self.device = VirtualI2CDevice(self.sensor_addr)
        self.threshold = 30.0

    def get_temperature(self):
        high_byte = self.device.read_byte(0x00)
        low_byte = self.device.read_byte(0x01)

        # TMP102 style 12-bit conversion: (High << 4) | (Low >> 4)
        raw_temp = (high_byte << 4) | (low_byte >> 4)
        temp_c = raw_temp * 0.0625
        return temp_c

    def run_test(self):
        print(f"--- Starting HW Test at Address {hex(self.sensor_addr)} ---")

        current_temp = self.get_temperature()
        print(f"Current Temperature: {current_temp} C")

        if current_temp > self.threshold:
            print("[RESULT] Status: FAIL - Overheated!")
            return False

        print("[RESULT] Status: PASS")
        return True


if __name__ == "__main__":
    tester = SensorTester()
    success = tester.run_test()
    if not success:
        raise SystemExit(1)
