import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Đọc file CSV
file_path = "AnKhe2019_2022.csv"  # Thay đổi đường dẫn đến file CSV của bạn
df = pd.read_csv(file_path, parse_dates=['Thời gian'])

# Trích xuất biến mục tiêu
target_variable = 'Lưu lượng đến hồ (m³/s)'
data_to_forecast = df[target_variable].values.reshape(-1, 1)

# Bao gồm các đặc trưng đầu vào bổ sung
additional_features = ['Mực nước hồ (m)', 'Tổng (m)']
additional_data = df[additional_features].values

# Chuẩn hóa dữ liệu
scaler_target = MinMaxScaler()
scaler_features = MinMaxScaler()

data_scaled_target = scaler_target.fit_transform(data_to_forecast)
data_scaled_features = scaler_features.fit_transform(additional_data)

# Tạo chuỗi với nhiều đặc trưng
sequence_length = 10  # Điều chỉnh nếu cần
X_target = []
X_features = []
y = []
for i in range(len(data_scaled_target) - sequence_length):
    seq_target = data_scaled_target[i:i + sequence_length]
    seq_features = data_scaled_features[i:i + sequence_length]
    label = data_scaled_target[i + sequence_length]
    
    X_target.append(seq_target)
    X_features.append(seq_features)
    y.append(label)

X_target = np.array(X_target)
X_features = np.array(X_features)
y = np.array(y)

# Chia dữ liệu thành tập huấn luyện và tập kiểm thử
train_size = int(len(X_target) * 0.80)
test_size = len(X_target) - train_size
X_target_train, X_target_test = X_target[0:train_size], X_target[train_size:len(X_target)]
X_features_train, X_features_test = X_features[0:train_size], X_features[train_size:len(X_target)]
y_train, y_test = y[0:train_size], y[train_size:len(X_target)]

# Xây dựng mô hình LSTM với một lớp ẩn
model = Sequential()
model.add(LSTM(units=50, activation='relu', input_shape=(sequence_length, 1)))
model.add(Dense(units=1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Huấn luyện mô hình
model.fit(X_target_train, y_train, epochs=50, batch_size=32)

# Đưa ra dự đoán
X_target_test_reshaped = X_target_test.reshape((X_target_test.shape[0], X_target_test.shape[1], 1))
predictions = model.predict(X_target_test_reshaped)

# Đảo ngược biến đổi để lấy tỷ lệ gốc
predictions_actual = scaler_target.inverse_transform(predictions.reshape(-1, 1))
y_test_actual = scaler_target.inverse_transform(y_test.reshape(-1, 1))

# Tính toán và in ra các độ đo đánh giá
rmse = np.sqrt(mean_squared_error(y_test_actual, predictions_actual))
r2 = r2_score(y_test_actual, predictions_actual)
mae = mean_absolute_error(y_test_actual, predictions_actual)

print(f"Root Mean Squared Error (RMSE): {rmse}")
print(f"R-squared (R2): {r2}")
print(f"Mean Absolute Error (MAE): {mae}")

# Vẽ biểu đồ kết quả
plt.plot(y_test_actual, label='Thực tế')
plt.plot(predictions_actual, label='Dự đoán', linestyle='--')
plt.legend()
plt.show()
