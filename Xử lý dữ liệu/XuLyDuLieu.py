import pandas as pd
from datetime import datetime, timedelta

df = pd.read_csv('An Khê/An Khê/từ 2.10 đến 31.12.2022.csv')

# Thay thế giá trị '--' bằng NaN
df.replace('--', pd.NA, inplace=True)

print(df.isnull().sum())



df = df[['LVS/Hồ/Ngày/Giờ', 'LVS/Hồ chứa/Ngày', 'Mực nước hồ (m)', 'Lưu lượng đến hồ (m³/s)', 'Tổng lưu lượng xả (m³/s)[Yêu cầu]', 'Tổng lưu lượng xả (m³/s)[Thực tế]', 'Tổng lưu lượng xả (m³/s)[+/-]']]

# Hàm chuyển đổi số nguyên thành thời gian
def int_to_time(hour_integer):
    # Chuyển đổi số nguyên thành thời gian timedelta
    time_delta = timedelta(hours=hour_integer)

    # Tạo một thời điểm bắt đầu (00:00:00)
    start_time = datetime(1900, 1, 1, 0, 0, 0)

    # Cộng thời gian timedelta vào thời điểm bắt đầu
    result_time = start_time + time_delta

    # Trả về chuỗi đại diện cho giờ
    return result_time.strftime('%H:%M:%S')

# Chuyển đổi dữ liệu trong cột 'LVS/Hồ/Ngày/Giờ'
df['LVS/Hồ/Ngày/Giờ'] = df['LVS/Hồ/Ngày/Giờ'].apply(int_to_time)

# Loại bỏ các cột có ít nhất một giá trị thiếu
df_cleaned = df.dropna(axis=1)

# Chuyển đổi dữ liệu trong cột 'LVS/Hồ/Ngày/Giờ'
df_cleaned['LVS/Hồ chứa/Ngày'] = pd.to_datetime(df_cleaned['LVS/Hồ chứa/Ngày'], format='%d/%m/%Y')
print(df_cleaned.head())

df_cleaned.to_csv('DuLieuAnKhe/17.csv', index=False)
