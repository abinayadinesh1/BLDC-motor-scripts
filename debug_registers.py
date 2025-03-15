from pymodbus.client import ModbusSerialClient
import time

registers_to_test = [
    (0x0056, "Speed setting"),
    (0x0066, "Motor running status"),
    (0x0076, "Fault code"),
    (0x0086, "Overcurrent time"),
    (0x0096, "Temperature"),
    (0x00A6, "Driver address"),
    (0x00B6, "Actual motor current"),
    (0x00C6, "Actual motor voltage"),
    (0x00D6, "Starting torque"),
    (0x00E6, "Acceleration time"),
    (0x00F6, "Baud rate"),
    (0x0106, "Auto restart"),
    (0x0116, "Pole pairs"),
    (0x0126, "Max current"),
    (0x0136, "Control mode")
]

for reg, name in registers_to_test:
    try:
        print(f"\nReading {name} (register 0x{reg:04X})...")
        result = client.read_holding_registers(reg, 1)
        if result and hasattr(result, 'registers'):
            print(f"Success! Value: {result.registers[0]}")
        else:
            print("No valid response")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(0.5)  # Add delay between requests
