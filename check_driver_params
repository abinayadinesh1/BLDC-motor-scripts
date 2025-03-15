#!/usr/bin/env python3
from pymodbus.client import ModbusSerialClient
import time

print("Checking driver parameters...")

# Configure the Modbus client
client = ModbusSerialClient(
    port='/dev/ttyUSB0',  # Adjust if your device is different
    baudrate=9600,
    bytesize=8,
    parity='N',
    stopbits=1,
    timeout=1
)

# Connect to the driver
print("Connecting to motor driver...")
connection = client.connect()
print(f"Connection status: {connection}")

if connection:
    try:
        # Read number of motor pole pairs (register 0x0116)
        print("\nReading motor pole pairs...")
        pole_pairs = client.read_holding_registers(0x0116)
        if pole_pairs and hasattr(pole_pairs, 'registers'):
            print(f"Motor pole pairs: {pole_pairs.registers[0]}")
        else:
            print("Failed to read motor pole pairs")
        
        # Read control mode (register 0x0136)
        print("\nReading control mode...")
        mode = client.read_holding_registers(0x0136)
        if mode and hasattr(mode, 'registers'):
            mode_value = mode.registers[0]
            if mode_value == 1:
                print("Control mode: Internal (Modbus) mode")
            elif mode_value == 0:
                print("Control mode: External (GPIO) mode")
            else:
                print(f"Unknown control mode: {mode_value}")
        else:
            print("Failed to read control mode")
        
        # Read starting torque (register 0x00D6)
        print("\nReading starting torque setting...")
        torque = client.read_holding_registers(0x00D6)
        if torque and hasattr(torque, 'registers'):
            print(f"Starting torque setting: {torque.registers[0]}")
        else:
            print("Failed to read starting torque")
        
        # Read maximum continuous protection current (register 0x0126)
        print("\nReading maximum continuous protection current...")
        current = client.read_holding_registers(0x0126)
        if current and hasattr(current, 'registers'):
            print(f"Maximum continuous protection current: {current.registers[0]}")
        else:
            print("Failed to read maximum current")
        
        # Try to set the internal mode explicitly if not already set
        print("\nSetting driver to internal (Modbus) mode...")
        mode_set = client.write_register(0x0136, 1)
        print(f"Set mode result: {mode_set}")
        
        # Save parameters
        print("\nSaving parameters...")
        save = client.write_register(0x80FF, 0x55AA)
        print(f"Save parameters result: {save}")
        
        # Try with higher starting torque
        print("\nSetting higher starting torque...")
        torque_set = client.write_register(0x00D6, 30)  # Increase from default 18H
        print(f"Set torque result: {torque_set}")
        
        # Try setting proper pole pairs (if needed)
        print("\nSetting motor pole pairs...")

        # Our motor has 5 pole pairs
        pairs_set = client.write_register(0x0116, 5)  
        print(f"Set pole pairs result: {pairs_set}")
        
        # Save parameters again
        print("\nSaving parameters again...")
        save = client.write_register(0x80FF, 0x55AA)
        print(f"Save parameters result: {save}")
        
    except Exception as e:
        print(f"Error during parameter check: {e}")
    finally:
        client.close()
        print("\nConnection closed")
else:
    print("Failed to connect to the motor driver")
