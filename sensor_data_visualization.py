import serial
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Configure the serial port (change COM10 to the appropriate port)
serial_port = 'COM10'
baud_rate = 115200

# Set up the serial connection
ser = serial.Serial(serial_port, baud_rate)
ser.flush()  # Clear the buffer

# Prepare data lists for visualization
accel_data = []
gyro_data = []

# Set up the plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
plt.style.use('fivethirtyeight')

def animate(i):
    while ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()  # Read a line from the serial
        print(f"Raw data from Arduino: {line}")  # Print the raw data for debugging
        if line:
            # Parse the line for accelerometer and gyroscope data
            try:
                # Example line: "A: 10.02,0.13,0.47 | G: -0.02,-0.01,-0.01"
                parts = line.split(' | ')
                if len(parts) != 2:
                    print("Data format is incorrect. Expected 2 parts separated by ' | '.")
                    continue  # Skip this line if it does not have the expected parts

                accel_part = parts[0].split(': ')[1].split(', ')
                gyro_part = parts[1].split(': ')[1].split(', ')

                # Convert to float and append to lists
                accel_data.append([float(value) for value in accel_part])
                gyro_data.append([float(value) for value in gyro_part])

                # Limit data lists to the last 100 entries
                if len(accel_data) > 100:
                    accel_data.pop(0)
                    gyro_data.pop(0)

                # Clear and update the plots
                ax1.cla()
                ax2.cla()

                # Convert data for plotting
                accel_x = [data[0] for data in accel_data]
                accel_y = [data[1] for data in accel_data]
                accel_z = [data[2] for data in accel_data]

                gyro_x = [data[0] for data in gyro_data]
                gyro_y = [data[1] for data in gyro_data]
                gyro_z = [data[2] for data in gyro_data]

                ax1.plot(accel_x, label='Accel X')
                ax1.plot(accel_y, label='Accel Y')
                ax1.plot(accel_z, label='Accel Z')
                ax1.set_title('Accelerometer Data')
                ax1.set_ylabel('Acceleration (m/s²)')
                ax1.legend(loc='upper right')

                ax2.plot(gyro_x, label='Gyro X')
                ax2.plot(gyro_y, label='Gyro Y')
                ax2.plot(gyro_z, label='Gyro Z')
                ax2.set_title('Gyroscope Data')
                ax2.set_ylabel('Gyroscope (°/s)')
                ax2.legend(loc='upper right')

            except Exception as e:
                print(f"Error parsing data: {e}")

# Create an animation that updates the plot in real-time
ani = FuncAnimation(fig, animate, interval=100)
plt.tight_layout()
plt.show()

# Cleanup
ser.close()  # Close the serial connection when done
