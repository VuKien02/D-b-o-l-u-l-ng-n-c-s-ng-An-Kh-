import pandas as pd

# Đọc dữ liệu từ file Excel
excel_file_path = 'AnKheData_GA_SVR.xlsx'
df_excel = pd.read_excel(excel_file_path)

# Chọn cột thời gian và cột tổng
cl1 = 'LVS/Hồ chứa/Ngày'
cl2 = 'Mực nước hồ (m)'
cl3 = 'Lưu lượng đến hồ (m³/s)'
cl4 = 'Tổng lưu lượng xả (m³/s)[Thực tế]'
df_selected = df_excel[[cl1, cl2,cl3,cl4]]

# Lưu DataFrame với cột thời gian và cột tổng vào file CSV
csv_file_path = 'AnKheData_GA_SVR.csv'
df_selected.to_csv(csv_file_path, index=False)

print(f"Đã lưu: {csv_file_path}")
