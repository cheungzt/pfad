import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Read the CSV file
file_path = '/Users/Home_Ivan/Desktop/PolyU_IME/SD5913 Programming For Artists And Designers/Week2/pfad/assignment/daily_KP_MEANHKHI_2024.csv'
df = pd.read_csv(file_path, skiprows=2, encoding='utf-8', on_bad_lines='skip')

print("Columns in the dataframe:", df.columns)

# Drop rows with missing values to ensure the '數值/Value' column exists
df.dropna(subset=['數值/Value'], inplace=True)

# Combine Year, Month, Day columns into a single Date column
df['Date'] = pd.to_datetime(df[['年/Year', '月/Month', '日/Day']].rename(columns={
    '年/Year': 'year', '月/Month': 'month', '日/Day': 'day'
}))

print(df[['年/Year', '月/Month', '日/Day', 'Date', '數值/Value']].head())

# Create the figure and axis for the plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_title("Daily Mean HKHI - King's Park")
ax.set_xlabel('Date')
ax.set_ylabel('Mean HKHI Value')
ax.grid(True)

# Initialize the line plot
line, = ax.plot([], [], label='Daily Values', marker='o', color='b')
ax.legend()
plt.xticks(rotation=45)

# Initialize data lists
x_data, y_data = [], []

# Set the limits for the x and y axes
ax.set_xlim(df['Date'].min(), df['Date'].max())
ax.set_ylim(df['數值/Value'].min(), df['數值/Value'].max())

# Update function for the animation
def update(frame):
    # Append the next data point to the lists
    x_data.append(df['Date'].iloc[frame])
    y_data.append(df['數值/Value'].iloc[frame])

    # Update the line with the new data
    line.set_data(x_data, y_data)
    return line,

# Create the animation; interval controls the speed and disable looping
ani = FuncAnimation(fig, update, frames=len(df), interval=100, blit=True, repeat=False)

# Display the animated plot
plt.tight_layout()
plt.show()
