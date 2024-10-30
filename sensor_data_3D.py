import serial
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# Configure the serial port
serial_port = 'COM10'  # Update this with your port
baud_rate = 115200

# Set up the serial connection
ser = serial.Serial(serial_port, baud_rate)
ser.flush()  # Clear the buffer

# Prepare data lists for visualization
accel_data = []
gyro_data = []

# Set up the 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim([-15, 15])
ax.set_ylim([-15, 15])
ax.set_zlim([-15, 15])

# Create a 3D object (a simple cube)
size = 1  # Size of the cube
cube = np.array([[size, size, size], [-size, size, size], 
                 [-size, -size, size], [size, -size, size],
                 [size, size, -size], [-size, size, -size],
                 [-size, -size, -size], [size, -size, -size]])

# Initialize the position and orientation
position = np.zeros(3)
orientation = np.zeros(3)

def animate(i):
    global position, orientation
    
    while ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()  # Read a line from the serial
        print(f"Raw data from Arduino: {line}")  # Print the raw data for debugging
        if line:
            # Parse the line for accelerometer and gyroscope data
            try:
                parts = line.split(' | ')
                if len(parts) != 2:
                    print("Data format is incorrect. Expected 2 parts separated by ' | '.")
                    continue  # Skip this line if it does not have the expected parts

                accel_part = parts[0].split(': ')[1].split(', ')
                gyro_part = parts[1].split(': ')[1].split(', ')

                # Convert to float
                accel_data.append([float(value) for value in accel_part])
                gyro_data.append([float(value) for value in gyro_part])

                # Limit data lists to the last 100 entries
                if len(accel_data) > 100:
                    accel_data.pop(0)
                    gyro_data.pop(0)

                # Calculate new position and orientation
                position += np.array(accel_data[-1]) * 0.01  # Update position based on acceleration
                orientation += np.array(gyro_data[-1]) * 0.01  # Update orientation based on gyroscope data

                # Clear the plot and draw the cube
                ax.cla()
                
                # Draw the cube at the new position
                for v in cube:
                    ax.scatter(position[0] + v[0], position[1] + v[1], position[2] + v[2], color='b')

                # Set the new orientation (using Euler angles)
                ax.view_init(elev=orientation[1], azim=orientation[0])  # Update view based on orientation

                # Set limits and labels
                ax.set_xlim([-15, 15])
                ax.set_ylim([-15, 15])
                ax.set_zlim([-15, 15])
                ax.set_title('3D Visualization of MPU6050 Data')
                ax.set_xlabel('X Axis')
                ax.set_ylabel('Y Axis')
                ax.set_zlabel('Z Axis')

            except Exception as e:
                print(f"Error parsing data: {e}")

# Create an animation that updates the plot in real-time
ani = FuncAnimation(fig, animate, interval=100)
plt.show()

# Cleanup
ser.close()  # Close the serial connection when done
