import pytest
from processor import process_sensor_data

# 일반적인 AI가 생성한 기본적인 테스트 코드 예시
def test_basic_average():
    # 정상적인 데이터에 대한 테스트
    assert process_sensor_data([10, 20, 30]) == 20.0

def test_empty_list():
    # 빈 리스트 처리 확인
    with pytest.raises(ValueError):
        process_sensor_data([])

def test_single_value():
    # 단일 값 처리 확인
    assert process_sensor_data([50]) == 50.0
