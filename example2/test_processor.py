import pytest
from processor import process_sensor_data

# 1. Happy Path (정상 케이스)
def test_process_normal_data():
    data = [10, 20, 30, 40, 50]
    assert process_sensor_data(data) == 30.0

# 2. Boundary Values (경계값 케이스: 0과 100)
def test_process_boundary_values():
    data = [0, 50, 100]
    assert process_sensor_data(data) == 50.0

# 3. Mixed Types (유효하지 않은 데이터가 섞인 경우)
def test_process_mixed_data_types():
    # 문자열, None, 범위 밖 숫자가 포함되어도 유효한 값(50)만 평균 계산
    data = ["error", None, -10, 110, 50]
    assert process_sensor_data(data) == 50.0

# 4. Exception: Not a list (입력값이 리스트가 아닌 경우)
def test_invalid_input_type():
    with pytest.raises(ValueError, match="입력값은 리스트여야 합니다."):
        process_sensor_data(123)

# 5. Exception: No valid data (유효한 데이터가 하나도 없는 경우)
def test_no_valid_data():
    with pytest.raises(ValueError, match="유효한 센서 데이터"):
        process_sensor_data([-1, 101, "invalid"])

# 6. Float Support (실수값 지원 확인)
def test_float_data():
    data = [10.5, 20.5]
    assert process_sensor_data(data) == 15.5
