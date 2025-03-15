print("program starting")
from pymodbus.client import ModbusSerialClient
import time

client = ModbusSerialClient(
    port = "/dev/ttyUSB0",
    baudrate = 9600,
    bytesize = 8,
    parity = "N",
    stopbits = 1,
    timeout = 1
)

def save_parameters():
    result = client.write_register(0x80FF, 0x55AA)
    print("Parameters saved.")

def set_speed(speed):
    if speed < 0 or speed > 4000:
        print("Speed must be between 0 and 4000.")
        return False
    result = client.write_register(0x0056, speed)
    print("Speed set to {speed}: ", result)
    return result

def start_motor():
    result = client.write_register(0x0066, 1)
    print("Motor started: ", result)
    return result

def stop_motor():
    result = client.write_register(0x0066, 0)
    print("Motor stopped: ", result)
    return result

def reverse_motor():
    result = client.write_register(0x0066, 2)
    print("Motor reversed: ", result)
    return result

def brake_motor():
    result = client.write_register(0x0066, 3)
    print("Motor braked: ", result)
    return result

def clear_fault():
    result = client.write_register(0x0076, 0)
    print("Fault cleared: ", result)
    return result

def interactive_control():
    while True:
        print("\nMotor Control Menu:")
        print("1. Set speed")
        print("2. Start Motor (Forward)")
        print("3. Reverse Motor")
        print("4. Stop Motor")
        print("5. Brake Motor")
        print("6. Clear Fault")
        print("7. Save Parameters")
        print("8. Exit")

        choice = input("Enter your choice (1-8)")

        if choice == "1":
            speed = int(input("Enter speed (0-4000): "))
        elif choice == "2":
            start_motor()
        elif choice == "3":
            reverse_motor()
        elif choice == "4":
            stop_motor()
        elif choice == "5":
            brake_motor()
        elif choice == "6":
            clear_fault()
        elif choice == "7":
            save_parameters()
        elif choice == "8":
            break
        else:
            print("Please choose a number between 1-8")


if __name__ == "__main__":
    print("Program Started")
    connection = client.connect()
    print("Connection status: ", connection)

    if connection:
        try:
            # interactive_control()
            clear_fault()
            set_speed(1000)
            save_parameters()
            start_motor()

            print("Motor running for 5 seconds...")
            time.sleep(5)

            stop_motor()

        except Exception as e:
            print("Error: ", e)

        client.close()
    else:
        print("Failed to connect to the motor driver via Modbus")


