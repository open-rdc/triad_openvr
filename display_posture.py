import triad_openvr
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy.spatial.transform import Rotation as R

class VRTrackerApp3D:
    def __init__(self):
        # Initialize OpenVR
        self.vr = triad_openvr.triad_openvr()
        self.vr.print_discovered_objects()

        # Initialize the 3D plot
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim(-0.5, 0.5)
        self.ax.set_ylim(-0.5, 0.5)
        self.ax.set_zlim(-0.5, 0.5)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")
        
        # Initialize the tracker's position and orientation marker
        self.tracker_marker, = self.ax.plot([0], [0], [0])  # Blue dot for position
        self.orientation_arrow = None

        # Use FuncAnimation to call update_position every 40 ms
        self.anim = FuncAnimation(self.fig, self.update_position, interval=40)
        plt.show()

    def update_position(self, frame):
        if "tracker_1" in self.vr.devices:
            # Get position and orientation (Euler angles)
            pose = self.vr.devices["tracker_1"].get_pose_quaternion()
            x, y, z = -pose[0], pose[2], pose[1] 
            r_w, r_x, r_y, r_z =  pose[3], -pose[4], pose[6], pose[5]

            print(f"x={x:.4f}, y={y:.4f}, z={z:.4f}, r_w={r_w:.4f}, r_x={r_x:.4f}, r_y={r_y:.4f}, r_z={r_z:.4f}")

            # Calculate orientation direction vector
            direction = self.calculate_orientation_vector(r_w, r_x, r_y, r_z)
            dx, dy, dz = direction * 0.5  # Scale for visibility

            # Update or create the orientation arrow
            if self.orientation_arrow:
                self.orientation_arrow.remove()
            self.orientation_arrow = self.ax.quiver(
                x, y, z, dx, dy, dz, color='r', arrow_length_ratio=0.1
            )

    def calculate_orientation_vector(self, r_w, r_x, r_y, r_z):
        # Create a rotation object from the quaternion
        quaternion = R.from_quat([r_x, r_y, r_z, r_w])

        # Apply the quaternion rotation to the initial Z-axis vector (0, 0, 1)
        initial_direction = np.array([0, 0, 1])
        rotated_vector = quaternion.apply(initial_direction)

        return rotated_vector

# Run the application
VRTrackerApp3D()
