import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 读取 CSV 文件
file_path = '/Users/Home_Ivan/Desktop/PolyU_IME/SD5913 Programming For Artists And Designers/Week2/pfad/assignment/daily_KP_MEANHKHI_2024.csv'
df = pd.read_csv(file_path, skiprows=2, encoding='utf-8', on_bad_lines='skip')

print("Columns in the dataframe:", df.columns)

# 删除空值行，确保实际存在 '數值/Value' 列
df.dropna(subset=['數值/Value'], inplace=True)

# 合并 Year, Month, Day 列为一个日期列
df['Date'] = pd.to_datetime(df[['年/Year', '月/Month', '日/Day']].rename(columns={
    '年/Year': 'year', '月/Month': 'month', '日/Day': 'day'
}))

print(df[['年/Year', '月/Month', '日/Day', 'Date', '數值/Value']].head())

# 创建图表
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_title("Daily Mean HKHI - King's Park")
ax.set_xlabel('Date')
ax.set_ylabel('Mean HKHI Value')
ax.grid(True)

# 初始化空的折线图
line, = ax.plot([], [], label='Daily Values', marker='o', color='b')
ax.legend()
plt.xticks(rotation=45)

# 初始化数据范围
x_data, y_data = [], []

# 设置图表的 X 和 Y 轴的范围
ax.set_xlim(df['Date'].min(), df['Date'].max())
ax.set_ylim(df['數值/Value'].min(), df['數值/Value'].max())


# 更新函数
def update(frame):
    # 将数据逐步添加到列表中
    x_data.append(df['Date'].iloc[frame])
    y_data.append(df['數值/Value'].iloc[frame])

    # 更新折线图的数据
    line.set_data(x_data, y_data)
    return line,


# 创建动画，interval 控制动画的速度
ani = FuncAnimation(fig, update, frames=len(df), interval=100, blit=True)

# 显示动态图表
plt.tight_layout()
plt.show()
