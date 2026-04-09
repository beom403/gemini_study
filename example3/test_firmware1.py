import time
import random

# [가상 HW 환경 모사] - 실제 HW가 없으므로 클래스로 모사합니다.
class VirtualI2CDevice:
    def __init__(self, address):
        self.address = address
        self.registers = {
            0x00: 0x1A, # 온도 데이터 High Byte
            0x01: 0x4B, # 온도 데이터 Low Byte (정상 범위)
            0x02: 0x01  # Config Register
        }

    def read_byte(self, reg):
        if reg not in self.registers:
            raise RuntimeError(f"Error: Invalid Register Access 0x{reg:02X}")
        return self.registers[reg]

# ---------------------------------------------------------
# [버그가 포함된 HW 테스트 펌웨어 코드]
# ---------------------------------------------------------

class SensorTester:
    def __init__(self):
        # 버그 1: 잘못된 I2C 주소 (실제 장치는 0x48이어야 함)
        self.sensor_addr = 0x99 
        self.device = VirtualI2CDevice(self.sensor_addr)
        self.threshold = 30.0

    def get_temperature(self):
        # 버그 2: 'self' 누락 (파이썬 기본 문법 에러)
        high_byte = device.read_byte(0x00) 
        low_byte = self.device.read_byte(0x01)
        
        # 버그 3: 잘못된 비트 연산 논리 (온도 변환 공식 오류)
        # 실제 공식: (High << 4) | (Low >> 4) 인데 실수로 작성됨
        raw_temp = (high_byte << 8) + low_byte
        temp_c = raw_temp * 0.0625
        return temp_c

    def run_test(self):
        print(f"--- Starting HW Test at Address {hex(self.sensor_addr)} ---")
        
        # 버그 4: 타입 불일치 (문자열과 숫자 비교)
        current_temp = "26.5" 
        current_temp = self.get_temperature()
        
        print(f"Current Temperature: {current_temp} C")
        
        if current_temp > self.threshold:
            print("[RESULT] Status: FAIL - Overheated!")
            return False
        else:
            print("[RESULT] Status: PASS")
            return True

if __name__ == "__main__":
    tester = SensorTester()
    success = tester.run_test()
    if not success:
        exit(1) # 에러 상태로 종료
