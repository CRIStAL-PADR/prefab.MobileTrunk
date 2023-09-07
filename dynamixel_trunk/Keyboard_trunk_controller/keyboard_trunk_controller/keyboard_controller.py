import os
import rclpy
from dynamixel_sdk_custom_interfaces.msg import SetPosition

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
        
NUM_CABLES = 9
DXL_MAXIMUM_POSITION_VALUE = 4100
dxl_velocity = [0] * NUM_CABLES

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

def main():
    rclpy.init()
    node = rclpy.create_node('Keyboard_Controller')
    
    publishers = []
    positions = {}  # Store positions for each cable
    for i in range(1, NUM_CABLES + 1):
        topic_name = f'Robot/Cable{i}/state/displacement'
        publisher = node.create_publisher(SetPosition, topic_name, 10)
        publishers.append(publisher)
        positions[i] = 0  # Initial position for each cable
    
           # Publish initial position 0 for each motor
        initial_position_msg = SetPosition()
        initial_position_msg.id = i
        initial_position_msg.position = positions[i]
        publishers[i - 1].publish(initial_position_msg)
        
         
    current_cable = None
    try:
        while True:
            print("Enter a cable ID (1-9), or press ESC to quit:")
            key = getch()
            if key == chr(0x1b):  # ESC key to quit
                break
            elif key.isdigit():
                cable_number = int(key)
                if 1 <= cable_number <= NUM_CABLES:
                    current_cable = cable_number
                    print(f"Selected Cable {current_cable}")
                
                while current_cable:
                    print(f"Current Cable: {current_cable}")
                    print("Press + to increase position, - to decrease, or press any digit to change cable:")
                    key = getch()
                    if key == chr(0x1b):  # ESC key to quit
                        break
                    elif key == '+':
                        positions[current_cable] += 100  # Increase position by 100
                        positions[current_cable] = clamp(positions[current_cable], 0, DXL_MAXIMUM_POSITION_VALUE)
                        print(f"Position increased by 100. New position: {positions[current_cable]}")
                    elif key == '-':
                        positions[current_cable] -= 100  # Decrease position by 100
                        positions[current_cable] = clamp(positions[current_cable], 0, DXL_MAXIMUM_POSITION_VALUE)
                        print(f"Position decreased by 100. New position: {positions[current_cable]}")
                    elif key.isdigit():
                        current_cable = int(key)
                        print(f"Selected Cable {current_cable}")
                    else:
                        print("Invalid key. Press +, -, or any digit.")
                    
                    msg = SetPosition()
                    msg.id = current_cable
                    msg.position = positions[current_cable]
                    publishers[current_cable - 1].publish(msg)
                    print(f"Published position for Cable {current_cable}: {msg.position}")

    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()

