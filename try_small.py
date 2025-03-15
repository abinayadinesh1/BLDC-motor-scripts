from pymodbus.client import ModbusSerialClient
import time

# Configure the Modbus client
client = ModbusSerialClient(
    port='/dev/ttyUSB0',  # Adjust if your device is different
    baudrate=9600,
    bytesize=8,
    parity='N',
    stopbits=1,
    timeout=1
)


# Set to internal mode (Modbus control)
print("Setting to internal mode...")
mode_set = client.write_register(0x0136, 1)
print(f"Set mode result: {mode_set}")

# Save the parameters
save = client.write_register(0x80FF, 0x55AA)
print(f"Save parameters result: {save}")

clear_fault = client.write_register(0x0076, 0)
print(f"Clear fault result: {clear_fault}")

# Set starting torque higher
torque_set = client.write_register(0x00D6, 30)  # Higher than default

# Set speed to 2000 RPM
speed_set = client.write_register(0x0056, 2000)

# Start motor in reverse (since you mentioned it showed reverse status)
start = client.write_register(0x0066, 2)

# Wait and check actual speed
time.sleep(2)
speed = client.read_holding_registers(0x005F)
print(f"Actual speed: {speed.registers[0] if hasattr(speed, 'registers') else 'Unknown'}")

fault = client.read_holding_registers(0x0076)
if hasattr(fault, 'registers'):
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
