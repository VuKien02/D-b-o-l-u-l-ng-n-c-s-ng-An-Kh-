import pandas as pd
from sklearn.linear_model import LinearRegression

# Đường dẫn đến tệp tin CSV của bạn
file_path = 'DuLieuAnKhe.csv'  # Thay thế 'XuLyThoiGian/1.csv' bằng đường dẫn thực tế của bạn

# Đọc dữ liệu từ tệp tin CSV, sử dụng ',' làm ký tự phân cách và chuyển cột 'Thời gian' thành datetime
df = pd.read_csv(file_path, sep=',', parse_dates=['Thời gian'])

# Tạo một chuỗi thời gian liên tục dựa trên khoảng thời gian giữa các mốc đo
min_time = df['Thời gian'].min()
max_time = df['Thời gian'].max()
continuous_time = pd.date_range(start=min_time, end=max_time, freq='1H')

# Tìm mốc đo thời gian nào bị thiếu
missing_time = continuous_time[~continuous_time.isin(df['Thời gian'])]

if missing_time.empty:
    print("Không có mốc đo thời gian nào bị thiếu.")
else:
    print("Các mốc đo thời gian bị thiếu:")
    print(missing_time)

    # Dự đoán giá trị thiếu cho cột 'Tổng lưu lượng xả' sử dụng mô hình Linear Regression
    model = LinearRegression()

    # Chọn các cột để huấn luyện mô hình
    features = ['Mực nước hồ (m)', 'Lưu lượng đến hồ (m³/s)']
    target = 'Tổng lưu lượng xả (m³/s)[Thực tế]'

    for missing_timestamp in missing_time:
        # Tìm mẫu trước và sau mốc thời gian bị thiếu
        prev_sample = df[df['Thời gian'] < missing_timestamp].tail(1)
        next_sample = df[df['Thời gian'] > missing_timestamp].head(1)

        # Lấy giá trị trung bình của mẫu trước và mẫu sau
        avg_values = (prev_sample[features].values + next_sample[features].values) / 2

        # Tạo dữ liệu bị thiếu và gán giá trị trung bình
        missing_data = pd.DataFrame(index=[missing_timestamp], columns=df.columns)
        missing_data['Thời gian'] = missing_timestamp
        missing_data[features] = avg_values

        # Huấn luyện mô hình
        model.fit(df[features], df[target])

        # Gán giá trị dự đoán của mô hình cho cột 'Tổng lưu lượng xả'
        missing_data[target] = model.predict(avg_values.reshape(1, -1))[0]

        # Gộp dữ liệu đã có và dữ liệu được dự đoán
        df = pd.concat([df, missing_data], ignore_index=True)

# Giới hạn dữ liệu ở mốc 2 số sau dấu phẩy
df = df.round({'Mực nước hồ (m)': 2, 'Lưu lượng đến hồ (m³/s)': 2, 'Tổng lưu lượng xả (m³/s)[Thực tế]': 2})

# Sắp xếp theo thời gian tăng dần
df = df.sort_values(by='Thời gian')

# Lưu dữ liệu đã hoàn thiện vào một tệp tin CSV mới
df.to_csv('duong_dan_den_file_hoan_thien.csv', index=False)
