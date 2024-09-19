import pandas as pd
import matplotlib.pyplot as plt


file_path = '/Users/Home_Ivan/Desktop/PolyU_IME/SD5913 Programming For Artists And Designers/Week2/pfad/assignment/daily_KP_MEANHKHI_2024.csv'

# 读取 CSV 文件，并跳过前两行说明内容，并忽略有格式问题的行
df = pd.read_csv(file_path, skiprows=2, encoding='utf-8', on_bad_lines='skip')


print("Columns in the dataframe:", df.columns)

# 删除空值行，确保实际存在 '數值/Value' 列
# 修改为匹配实际的列名
df.dropna(subset=['數值/Value'], inplace=True)

# 合并 Year, Month, Day 列为一个日期列
df['Date'] = pd.to_datetime(df[['年/Year', '月/Month', '日/Day']].rename(columns={
    '年/Year': 'year', '月/Month': 'month', '日/Day': 'day'
}))

print(df[['年/Year', '月/Month', '日/Day', 'Date', '數值/Value']].head())


plt.figure(figsize=(10, 6))

# 生成折线图，使用合并后的 'Date' 列和 '數值/Value' 列
plt.plot(df['Date'], df['數值/Value'], label='Daily Values', marker='o')


plt.title('Daily Mean HKHI - King\'s Park')
plt.xlabel('Date')
plt.ylabel('Mean HKHI Value')
plt.legend()


plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
