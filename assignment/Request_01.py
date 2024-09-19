import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt

# 请求目标网站
url = "https://www.rottentomatoes.com/browse/tv_series_browse/"  # 根据实际需求修改为正确的网址
response = requests.get(url)

# 检查请求是否成功
if response.ok:
    print("Data is ready!")

    # 解析 HTML 内容
    content = response.text
    soup = BeautifulSoup(content, "html.parser")  # 使用 BeautifulSoup 解析 HTML

    # 初始化一个空列表来存储提取的数据
    tideData = []

    # 查找所有 <td> 标签的内容，这里假设目标数据在 <td> 标签中
    tides = soup.findAll("td")

    # 检查是否找到任何 <td> 标签
    if not tides:
        print("No <td> elements found. Please check the selector.")

    # 提取每个 <td> 标签中的数值并清理
    for tide in tides:
        tideValue = tide.string  # 获取标签内的文本
        if tideValue is not None and tideValue.strip():  # 检查文本是否为空
            try:
                # 转换为浮点数并添加到列表中
                tideData.append(float(tideValue.strip()))
            except ValueError:
                # 如果转换失败，忽略该数据
                continue

    # 检查提取到的数据点数量
    if len(tideData) == 0:
        print("No numeric data extracted. Please check the HTML structure and the parsing logic.")
    else:
        # 打印提取数据的数量和前 100 个数据
        print(f"Number of data points: {len(tideData)}")
        print("First 100 data points:", tideData[:100])

        # 转换为 NumPy 数组以便于统计分析
        tide_array = np.array(tideData)

        # 基本统计分析
        print(f"平均值: {np.mean(tide_array)}")
        print(f"标准差: {np.std(tide_array)}")
        print(f"最大值: {np.max(tide_array)}")
        print(f"最小值: {np.min(tide_array)}")

        # 数据可视化
        plt.figure(figsize=(12, 6))
        plt.plot(tideData, label="Tide Data")
        plt.title("Tide Data Visualization")
        plt.xlabel("Index")
        plt.ylabel("Value")
        plt.legend()
        plt.grid(True)
        plt.show()

else:
    print(f"Failed to retrieve data, status code: {response.status_code}")
