def process_sensor_data(data):
    """
    센서 데이터 리스트를 처리합니다.
    - 유효 범위: 0 ~ 100
    - 유효한 데이터의 평균을 반환합니다.
    - 입력이 리스트가 아니거나 유효한 데이터가 없으면 ValueError를 발생시킵니다.
    """
    if not isinstance(data, list):
        raise ValueError("입력값은 리스트여야 합니다.")
    
    # 숫자형 데이터(int, float)이며 0~100 사이인 값만 필터링
    valid_readings = [r for r in data if isinstance(r, (int, float)) and 0 <= r <= 100]
    
    if not valid_readings:
        raise ValueError("유효한 센서 데이터(0-100)가 없습니다.")
    
    return sum(valid_readings) / len(valid_readings)
