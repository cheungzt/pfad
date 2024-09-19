import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# 设置3D图形
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_zlim(-1, 1)
ax.axis('off')  # 关闭坐标轴显示

# 初始化粒子系统
num_particles = 100
angles = np.random.uniform(0, 2 * np.pi, num_particles)  # 随机角度
radii = np.random.uniform(0, 0.1, num_particles)  # 初始半径较小，模拟生成过程
z_positions = np.random.uniform(-0.1, 0.1, num_particles)  # 随机Z坐标
colors = plt.cm.plasma(np.linspace(0, 1, num_particles))  # 使用 plasma 色图

# 创建3D散点图
particles = ax.scatter(radii * np.cos(angles), radii * np.sin(angles), z_positions, c=colors, s=50, alpha=0.75)

# 贝塞尔曲线参数
num_bezier_curves = 10  # 贝塞尔曲线的数量


# 贝塞尔曲线生成函数
def create_bezier_path(points):
    codes = [Path.MOVETO] + [Path.CURVE4] * (len(points) - 1)
    return Path(points, codes)


# 生成随机的贝塞尔曲线控制点
def random_bezier_control_points():
    # 生成四个控制点，包含X, Y, Z坐标
    return np.random.uniform(-1, 1, (4, 3))


# 初始化贝塞尔曲线
bezier_paths = [create_bezier_path(random_bezier_control_points()[:, :2]) for _ in range(num_bezier_curves)]
bezier_patches = [Poly3DCollection([random_bezier_control_points()], alpha=0.5) for _ in bezier_paths]

# 添加贝塞尔曲线到3D图中
for patch in bezier_patches:
    patch.set_color(np.random.choice(['cyan', 'magenta', 'yellow', 'green', 'blue', 'orange', 'red']))
    ax.add_collection3d(patch)

# 为每条曲线设置不同的速度和变化参数
curve_speeds = np.random.uniform(0.005, 0.02, num_bezier_curves)  # 每条曲线不同的速度
curve_offsets = np.linspace(0, 2 * np.pi, num_bezier_curves)  # 每条曲线不同的初始相位

# 动态参数
max_frames = 200
spiral_speed = 0.1
expand_speed = 0.005
explosion_trigger = max_frames // 2  # 设置爆炸触发的帧数


def reset_particles_and_curves():
    """重置粒子和曲线到初始状态"""
    global angles, radii, z_positions
    angles = np.random.uniform(0, 2 * np.pi, num_particles)
    radii = np.random.uniform(0, 0.1, num_particles)  # 重置到初始小半径
    z_positions = np.random.uniform(-0.1, 0.1, num_particles)

    for patch in bezier_patches:
        control_points = random_bezier_control_points()
        patch.set_verts([control_points])


def update(frame):
    global angles, radii, z_positions

    # 更新粒子的角度和半径，形成螺旋运动效果
    if frame < explosion_trigger:
        # 生成过程：粒子慢慢扩散
        angles += spiral_speed * (1 - radii)
        radii += expand_speed * np.sin(frame / 20)
        z_positions += np.sin(frame / 20) * 0.02  # Z 轴位置轻微变化
    else:
        # 爆炸过程：粒子快速扩散
        radii += 0.1
        z_positions += np.random.uniform(-0.1, 0.1, num_particles)  # 随机Z扩散

    # 保持粒子在显示范围内
    radii = np.clip(radii, 0, 1)
    angles = np.mod(angles, 2 * np.pi)
    z_positions = np.clip(z_positions, -1, 1)

    # 更新粒子的位置
    particles._offsets3d = (radii * np.cos(angles), radii * np.sin(angles), z_positions)

    # 更新贝塞尔曲线的控制点
    for i, patch in enumerate(bezier_patches):
        # 每条曲线使用不同的速度和变化规则
        offset = curve_offsets[i]
        speed = curve_speeds[i]
        t = frame * speed + offset  # 为每条曲线设定不同的变化速度

        # 动态控制点变化，使每条曲线独立变化
        control_points = np.array([
            [0.5 * np.cos(t), 0.5 * np.sin(t), 0.5 * np.sin(t)],
            [0.8 * np.cos(t + np.pi / 3), 0.8 * np.sin(t + np.pi / 3), 0.3 * np.cos(t)],
            [0.6 * np.cos(t + 2 * np.pi / 3), 0.6 * np.sin(t + 2 * np.pi / 3), 0.2 * np.sin(t)],
            [1.0 * np.cos(t + np.pi), 1.0 * np.sin(t + np.pi), np.sin(t)]
        ])

        # 爆炸时快速散开
        if frame >= explosion_trigger:
            control_points *= 1 + (frame - explosion_trigger) * 0.05

        # 更新3D贝塞尔曲线
        patch.set_verts([control_points])

        # 随机调整线条的透明度，避免曲线的完全重叠
        patch.set_alpha(np.random.uniform(0.3, 0.7))

    # 重置动画到初始状态以形成循环
    if frame >= max_frames - 1:
        reset_particles_and_curves()


# 创建动画
animation = FuncAnimation(fig, update, frames=max_frames, interval=30, repeat=True)
plt.show()
