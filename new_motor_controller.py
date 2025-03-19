#!/usr/bin/env python3
import time
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException
class MotorController:
    def __init__(self, port, baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=1):
        """Initialize the motor controller with RS485 parameters."""
        self.client = ModbusSerialClient(
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout
        )
        self.device_id = 1  # Default device ID
    def connect(self):
        """Connect to the Modbus device."""
        if not self.client.connect():
            print("Failed to connect!")
            return False
        print("Connected successfully")
        return True
    def close(self):
        """Close the connection."""
        self.client.close()
        print("Connection closed")
    def write_register(self, address, value):
        """Write a value to a specific register."""
        try:
            result = self.client.write_register(address, value, unit=self.device_id)
            if hasattr(result, 'isError') and result.isError():
                print(f"Error writing to register {address}: {result}")
                return False
            print(f"Successfully wrote value {value} to register {address}")
            return True
        except ModbusException as e:
            print(f"Modbus error: {e}")
            return False
    # Motor control commands
    def start(self):
        """Start the motor (01 06 00 66 00 01 A8 12)"""
        return self.write_register(0x66, 0x01)
    def stop(self):
        """Stop the motor (01 06 00 66 00 00 69 D5)"""
        return self.write_register(0x66, 0x00)
    def reverse_rotation(self):
        """Set motor to reverse rotation (01 06 00 66 00 02 E8 14)"""
        return self.write_register(0x66, 0x02)
    def braking(self):
        """Apply braking to the motor (01 06 00 66 00 03 29 D4)"""
        return self.write_register(0x66, 0x03)
    def set_speed(self, rpm):
        """Set motor speed in RPM (01 06 00 56 03 E8 69 64 for 1000 RPM)"""
        return self.write_register(0x56, rpm)
    def clear_fault(self):
        """Clear fault status (01 06 00 76 00 00 68 10)"""
        return self.write_register(0x76, 0x00)
def main():
    port = '/dev/ttyUSB0'  
    print(f"Connecting to motor controller on {port}...")
    controller = MotorController(port=port)
    if not controller.connect():
        print("Failed to connect. Exiting.")
        return
    try:
        while True:
            print("\nMotor Control Menu:")
            print("1. Start Motor")
            print("2. Stop Motor")
            print("3. Reverse Rotation")
            print("4. Apply Braking")
            print("5. Set Speed (RPM)")
            print("6. Clear Fault")
            print("0. Exit")
            choice = input("\nEnter your choice (0-6): ")
            if choice == '1':
                controller.start()
            elif choice == '2':
                controller.stop()
            elif choice == '3':
                controller.reverse_rotation()
            elif choice == '4':
                controller.braking()
            elif choice == '5':
                rpm = int(input("Enter speed in RPM: "))
                controller.set_speed(rpm)
            elif choice == '6':
                controller.clear_fault()
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")
            time.sleep(0.5)  # Small delay between commands
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        controller.close()
if __name__ == "__main__":
    main()
