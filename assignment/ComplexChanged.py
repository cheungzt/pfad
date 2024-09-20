import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Set up 3D figure
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_zlim(-1, 1)
ax.axis('off')  # Turn off axis display

# Initialize the particle system
num_particles = 100
angles = np.random.uniform(0, 2 * np.pi, num_particles)  # Random angles
radii = np.random.uniform(0, 0.1, num_particles)  # Small initial radius to simulate creation
z_positions = np.random.uniform(-0.1, 0.1, num_particles)  # Random Z positions
colors = plt.cm.plasma(np.linspace(0, 1, num_particles))  # Use the plasma colormap

# Create 3D scatter plot for particles
particles = ax.scatter(radii * np.cos(angles), radii * np.sin(angles), z_positions, c=colors, s=50, alpha=0.75)

# Number of Bezier curves
num_bezier_curves = 10


# Function to generate random Bezier control points
def random_bezier_control_points():
    # Generate four control points with X, Y, Z coordinates
    return np.random.uniform(-1, 1, (4, 3))


# Initialize Bezier curves
bezier_patches = [Poly3DCollection([random_bezier_control_points()], alpha=0.5) for _ in range(num_bezier_curves)]

# Add Bezier curves to the 3D plot
for patch in bezier_patches:
    patch.set_color(np.random.choice(['cyan', 'magenta', 'yellow', 'green', 'blue', 'orange', 'red']))
    ax.add_collection3d(patch)

# Set different speeds and offsets for each curve
curve_speeds = np.random.uniform(0.01, 0.04, num_bezier_curves)  # Faster curve speed
curve_offsets = np.linspace(0, 2 * np.pi, num_bezier_curves)  # Different initial phase for each curve

# Animation parameters
max_frames = 200
spiral_speed = 0.2  # Faster spiral speed
expand_speed = 0.01  # Faster expansion speed
explosion_trigger = max_frames // 2  # Frame count to trigger the explosion


def reset_particles_and_curves():
    """Reset particles and curves to their initial state."""
    global angles, radii, z_positions
    angles = np.random.uniform(0, 2 * np.pi, num_particles)
    radii = np.random.uniform(0, 0.1, num_particles)  # Reset to initial small radius
    z_positions = np.random.uniform(-0.1, 0.1, num_particles)

    for patch in bezier_patches:
        control_points = random_bezier_control_points()
        patch.set_verts([control_points])


def update(frame):
    global angles, radii, z_positions

    # Update particle angles and radii to create a spiral motion effect
    if frame < explosion_trigger:
        # Creation phase: particles slowly expand
        angles += spiral_speed * (1 - radii)
        radii += expand_speed * np.sin(frame / 20)
        z_positions += np.sin(frame / 20) * 0.03  # Z position changes slightly
    else:
        # Explosion phase: particles expand rapidly
        radii += 0.2  # Increase expansion speed
        z_positions += np.random.uniform(-0.1, 0.1, num_particles)  # Random Z expansion

    # Keep particles within display range
    radii = np.clip(radii, 0, 1)
    angles = np.mod(angles, 2 * np.pi)
    z_positions = np.clip(z_positions, -1, 1)

    # Update particle positions
    particles._offsets3d = (radii * np.cos(angles), radii * np.sin(angles), z_positions)

    # Update Bezier curve control points
    for i, patch in enumerate(bezier_patches):
        # Each curve uses different speed and change rules
        offset = curve_offsets[i]
        speed = curve_speeds[i]
        t = frame * speed + offset  # Set different change speeds for each curve

        # Dynamic control point change, making each curve vary independently
        control_points = np.array([
            [0.5 * np.cos(t), 0.5 * np.sin(t), 0.5 * np.sin(t)],
            [0.8 * np.cos(t + np.pi / 3), 0.8 * np.sin(t + np.pi / 3), 0.3 * np.cos(t)],
            [0.6 * np.cos(t + 2 * np.pi / 3), 0.6 * np.sin(t + 2 * np.pi / 3), 0.2 * np.sin(t)],
            [1.0 * np.cos(t + np.pi), 1.0 * np.sin(t + np.pi), np.sin(t)]
        ])

        # During explosion, curves spread quickly
        if frame >= explosion_trigger:
            control_points *= 1 + (frame - explosion_trigger) * 0.1

        # Update the 3D Bezier curves
        patch.set_verts([control_points])

        # Randomly adjust curve transparency to prevent complete overlap
        patch.set_alpha(np.random.uniform(0.3, 0.7))

    # Reset animation to the initial state for looping
    if frame >= max_frames - 1:
        reset_particles_and_curves()


# Create the animation
animation = FuncAnimation(fig, update, frames=max_frames, interval=20, repeat=True)  # Reduced interval for faster speed
plt.show()
