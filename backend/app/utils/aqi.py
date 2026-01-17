def calculate_aqi(pm25: float) -> int:
    # Simplified Indian AQI logic
    if pm25 <= 30:
        return 50
    elif pm25 <= 60:
        return 100
    elif pm25 <= 90:
        return 200
    elif pm25 <= 120:
        return 300
    else:
        return 400
