import pandas as pd
import matplotlib.pyplot as plt
# Processor the data
print("Data processing...")
df = pd.read_excel("student_grades.xlsx")

# Convert the 'Điểm chữ' column to numeric
# Convert A to 4, B to 3, C to 2, D to 1, F to 0
df['Điểm chữ'] = df['Điểm chữ'].replace({
    'A+': 4,
    'A': 4,
    'B+': 3.5,
    'B': 3,
    'C+': 2.5,
    'C': 2,
    'D+': 1.5,
    'D': 1,
    'F': 0
})
df['Điểm chữ'] = pd.to_numeric(df['Điểm chữ'], errors='coerce')
df = df[df['Điểm chữ'] != 0]
df = df[df['Điểm chữ'].notnull()]

# Convert the 'Số tín chỉ' column to numeric
df['Số tín chỉ'] = pd.to_numeric(df['Số tín chỉ'], errors='coerce')
# Remove rows with missing 'Số tín chỉ' values or value = 0
df = df[df['Số tín chỉ'] != 0]

# Convert the 'Điểm số' column to numeric
df['Điểm số'] = pd.to_numeric(df['Điểm số'], errors='coerce')
df['Điểm số'] = df['Điểm số'].fillna(0)
print(df)

# Calculate the average grade
df['Điểm trung bình'] = df['Điểm số'] * df['Số tín chỉ']
df['Tổng số tín chỉ'] = df['Số tín chỉ']
DTB = df['Điểm trung bình'].sum() / df['Tổng số tín chỉ'].sum()

df['Điểm trung bình hệ 4'] = df['Điểm chữ'] * df['Số tín chỉ']
DTB4 = df['Điểm trung bình hệ 4'].sum() / df['Tổng số tín chỉ'].sum()

print(f"Điểm trung bình hệ 10: {DTB}")
print(f"Điểm trung bình hệ 4: {DTB4}")

# Create plot distribute of grades by time update
