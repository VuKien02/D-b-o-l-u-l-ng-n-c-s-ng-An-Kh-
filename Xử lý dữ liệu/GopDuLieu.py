import os
import pandas as pd

# Thư mục chứa các file CSV
folder_path = 'XuLyThoiGian'

# Lấy danh sách các tệp trong thư mục
file_list = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Khởi tạo DataFrame trống để lưu trữ dữ liệu ghép
merged_data = pd.DataFrame()

# Đọc và ghép dữ liệu từ các file CSV trong thư mục
for file in file_list:
    file_path = os.path.join(folder_path, file)
    data = pd.read_csv(file_path)
    
    # Gộp dữ liệu vào DataFrame đã khởi tạo
    merged_data = pd.concat([merged_data, data], ignore_index=True)

# Sắp xếp DataFrame theo cột 'Thời gian' tăng dần
merged_data = merged_data.sort_values(by='Thời gian')

# Lưu dữ liệu ghép và đã sắp xếp vào một file mới
# merged_data.to_csv('merged_data_sorted.csv', index=False)

# Đọc dữ liệu từ tệp CSV gốc
file_path_input1 = 'merged_data_sorted.csv'
file_path_input2 = 'TongLuongNuocCacTram.csv'
df1 = pd.read_csv(file_path_input1)
df2 = pd.read_csv(file_path_input2)

# Ghép DataFrame dựa trên cột thời gian
merged_df = pd.merge(df1, df2, on='Thời gian', how='inner')  # 'thoi_gian' là tên cột thời gian

# Bỏ cột "Tổng lưu lượng xả (m³/s)"
merged_df = merged_df.drop("Tổng lưu lượng xả (m³/s)[Thực tế]", axis=1)

# Lưu DataFrame đã ghép vào một tệp CSV mới
file_path_output = 'DuLieuAnKhe2.csv'
merged_df.to_csv(file_path_output, index=False)
