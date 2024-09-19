import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import PathPatch
from matplotlib.path import Path

# 设置图形
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.axis('off')  # 关闭坐标轴显示

# 初始化粒子系统
num_particles = 100
angles = np.random.uniform(0, 2 * np.pi, num_particles)  # 随机角度
radii = np.random.uniform(0, 1, num_particles)  # 随机半径
colors = plt.cm.plasma(np.linspace(0, 1, num_particles))  # 使用 plasma 色图

# 创建散点图
particles = ax.scatter(radii * np.cos(angles), radii * np.sin(angles), c=colors, s=50, alpha=0.75)

# 贝塞尔曲线参数
num_bezier_curves = 20  # 贝塞尔曲线的数量


# 贝塞尔曲线生成函数
def create_bezier_path(points):
    codes = [Path.MOVETO] + [Path.CURVE4] * (len(points) - 1)
    return Path(points, codes)


# 生成随机的贝塞尔曲线
def random_bezier_control_points():
    # 生成随机的控制点，横纵坐标均在 -1 到 1 之间
    return np.random.uniform(-1, 1, (4, 2))


# 初始化贝塞尔曲线的路径
bezier_paths = [create_bezier_path(random_bezier_control_points()) for _ in range(num_bezier_curves)]
bezier_patches = [PathPatch(path, lw=2, alpha=0.5) for path in bezier_paths]

# 将贝塞尔曲线添加到图中
for patch in bezier_patches:
    patch.set_color(np.random.choice(['cyan', 'magenta', 'yellow', 'green', 'blue', 'orange', 'red']))
    ax.add_patch(patch)

# 动态参数
max_frames = 20
spiral_speed = 1
expand_speed = 0.005


def update(frame):
    global angles, radii

    # 更新粒子的角度和半径，形成螺旋运动效果
    angles += spiral_speed * (1 - radii)
    radii += expand_speed * np.sin(frame / 20)

    # 保持粒子在显示范围内
    radii = np.mod(radii, 1)
    angles = np.mod(angles, 2 * np.pi)

    # 更新粒子的位置
    particles.set_offsets(np.c_[radii * np.cos(angles), radii * np.sin(angles)])

    # 更新贝塞尔曲线的控制点，控制点随帧数变化
    for patch in bezier_patches:
        new_points = random_bezier_control_points()
        new_path = create_bezier_path(new_points)
        patch.set_path(new_path)

        # 随机调整线条颜色和透明度
        patch.set_color(plt.cm.viridis(np.random.rand()))
        patch.set_alpha(np.random.uniform(0.3, 0.7))


# 创建动画
animation = FuncAnimation(fig, update, frames=max_frames, interval=30, repeat=True)
plt.show()
