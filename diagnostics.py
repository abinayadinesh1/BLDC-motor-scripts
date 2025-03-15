#!/usr/bin/env python3
from pymodbus.client import ModbusSerialClient
import time

print("Starting motor diagnostics...")

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
        # Read motor status (register 0x0066)
        print("\nReading motor status...")
        status = client.read_holding_registers(0x0066, 1, unit=1)
        if status and hasattr(status, 'registers'):
            status_code = status.registers[0]
            status_desc = {
                0: "Stopped",
                1: "Forward rotation",
                2: "Reverse rotation",
                3: "Braking"
            }
            print(f"Motor status: {status_desc.get(status_code, f'Unknown ({status_code})')}")
        else:
            print("Failed to read motor status")
        
        # Read actual motor speed (register 0x005F)
        print("\nReading actual motor speed...")
        speed = client.read_holding_registers(0x005F, 1, unit=1)
        if speed and hasattr(speed, 'registers'):
            print(f"Actual motor speed: {speed.registers[0]} RPM")
        else:
            print("Failed to read motor speed")
        
        # Read fault codes (register 0x0076)
        print("\nReading fault codes...")
        fault = client.read_holding_registers(0x0076, 1, unit=1)
        if fault and hasattr(fault, 'registers'):
            fault_code = fault.registers[0]
            fault_desc = {
                0: "No fault",
                1: "Overcurrent",
                2: "Over temperature",
                3: "Overpressure",
                4: "Undervoltage",
                5: "Sensor abnormality",
                6: "Overspeed",
                8: "Stalled",
                9: "Peak current"
            }
            print(f"Fault status: {fault_desc.get(fault_code, f'Unknown fault ({fault_code})')}")
        else:
            print("Failed to read fault code")
        
        # Read internal temperature (register 0x0096)
        print("\nReading internal temperature...")
        temp = client.read_holding_registers(0x0096, 1, unit=1)
        if temp and hasattr(temp, 'registers'):
            print(f"Internal temperature: {temp.registers[0]}°C")
        else:
            print("Failed to read temperature")
        
        # Read actual motor voltage (register 0x00C6)
        print("\nReading motor voltage...")
        voltage = client.read_holding_registers(0x00C6, 1, unit=1)
        if voltage and hasattr(voltage, 'registers'):
            actual_voltage = voltage.registers[0] / 4  # According to manual, divide by 4
            print(f"Actual motor voltage: {actual_voltage}V")
        else:
            print("Failed to read voltage")
        
        # Try setting motor to run and check status
        print("\nAttempting to start motor...")
        
        # First set speed
        set_speed = client.write_register(0x0056, 1000)  # 1000 RPM
        print(f"Set speed result: {set_speed}")
        
        # Start motor
        start = client.write_register(0x0066, 1)  # Start forward
        print(f"Start motor result: {start}")
        
        # Wait a moment
        print("Waiting for motor to respond...")
        time.sleep(2)
        
        # Read status again
        status = client.read_holding_registers(0x0066, 1, unit=1)
        if status and hasattr(status, 'registers'):
            status_code = status.registers[0]
            print(f"Motor status after start command: {status_desc.get(status_code, f'Unknown ({status_code})')}")
        else:
            print("Failed to read motor status after start command")
        
        # Read actual speed again
        speed = client.read_holding_registers(0x005F, 1, unit=1)
        if speed and hasattr(speed, 'registers'):
            print(f"Actual motor speed after start command: {speed.registers[0]} RPM")
        else:
            print("Failed to read motor speed after start command")
        
        # Stop motor
        stop = client.write_register(0x0066, 0)  # Stop
        print(f"Stop motor result: {stop}")
        
    except Exception as e:
        print(f"Error during diagnostics: {e}")
    finally:
        client.close()
        print("\nConnection closed")
else:
    print("Failed to connect to the motor driver")

