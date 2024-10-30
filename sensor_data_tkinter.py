import tkinter as tk
import serial
import numpy as np

# Serial port configuration
serial_port = 'COM10'  # Update this with your port
baud_rate = 115200

# Set up the serial connection
ser = serial.Serial(serial_port, baud_rate)
ser.flush()  # Clear the buffer

# Initialize the Tkinter window
root = tk.Tk()
root.title("MPU6050 Position Visualization")

# Create a canvas to draw the object
canvas_width = 400
canvas_height = 400
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
canvas.pack()

# Create a rectangle (representing the object)
object_size = 20
object_id = canvas.create_rectangle(
    (canvas_width // 2 - object_size // 2, canvas_height // 2 - object_size // 2),
    (canvas_width // 2 + object_size // 2, canvas_height // 2 + object_size // 2),
    fill='blue'
)

# Initialize position
position = np.array([canvas_width // 2, canvas_height // 2])

def update_position():
    global position

    while ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()  # Read a line from the serial
        if line:
            # Parse the line for accelerometer data
            try:
                parts = line.split(' | ')
                if len(parts) != 2:
                    print("Data format is incorrect. Expected 2 parts separated by ' | '.")
                    continue

                accel_part = parts[0].split(': ')[1].split(', ')

                # Convert to float
                accel_data = np.array([float(value) for value in accel_part])

                # Update position based on acceleration (simple integration)
                position[0] += accel_data[0] * 0.01  # X position
                position[1] -= accel_data[1] * 0.01  # Y position (inverted)

                # Limit position to stay within canvas bounds
                position[0] = max(object_size // 2, min(position[0], canvas_width - object_size // 2))
                position[1] = max(object_size // 2, min(position[1], canvas_height - object_size // 2))

                # Update the position of the object on the canvas
                canvas.coords(object_id,
                              position[0] - object_size // 2, position[1] - object_size // 2,
                              position[0] + object_size // 2, position[1] + object_size // 2)

            except Exception as e:
                print(f"Error parsing data: {e}")

    # Call the update_position function again after 50 ms
    root.after(50, update_position)

# Start the update loop
update_position()

# Start the Tkinter main loop
root.mainloop()

# Cleanup
ser.close()  # Close the serial connection when done
