import pandas as pd

# Đường dẫn đến tệp tin CSV của bạn
file_path = 'DuLieu/1.csv'

# Đọc dữ liệu từ tệp tin CSV, sử dụng ',' làm ký tự phân cách
df = pd.read_csv(file_path, sep=',')

# Gộp cột thời gian và ngày thành một cột datetime mới
df['Thời gian'] = pd.to_datetime(df['LVS/Hồ/Ngày/Giờ'] + ' ' + df['LVS/Hồ chứa/Ngày'])

# Bỏ cột không cần thiết
df = df.drop(['LVS/Hồ/Ngày/Giờ', 'LVS/Hồ chứa/Ngày'], axis=1)

# Chuyển cột 'Thời gian' lên đầu tiên
column_order = ['Thời gian'] + [col for col in df if col != 'Thời gian']
df = df[column_order]

# In dữ liệu mới
print(df)

# Lưu DataFrame với cột mới vào một tệp tin CSV mới
output_file_path = 'XuLyThoiGian/1.csv'  # Thay thế 'duong_dan_ra_file_moi.csv' bằng đường dẫn thực tế của bạn
df.to_csv(output_file_path, index=False)  # index=False để không bao gồm cột chỉ số trong tệp CSV