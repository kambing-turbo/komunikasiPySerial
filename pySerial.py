import serial.tools.list_ports

# Mendapatkan daftar port yang tersedia
ports = serial.tools.list_ports.comports()
serial_inst = serial.Serial()

ports_list = []

for port in ports:
    ports_list.append(str(port))
    print(str(port))

# Meminta input dari pengguna
val = input('Select Port (e.g., COM3 or /dev/ttyACM0): ')

port_var = None
for port in ports_list:
    if val in port:
        port_var = val
        print(f'Selected port: {port_var}')
        break

if port_var is None:
    print(f'Port {val} not found in available ports.')
else:
    # Mengonfigurasi dan membuka port serial
    serial_inst.port = port_var
    serial_inst.baudrate = 9600  # Sesuaikan dengan baud rate yang digunakan
    
    if not serial_inst.is_open:
        serial_inst.open()
        print(f'Connected to {port_var}')

try:
    while True:
        command = input('Arduino Command (e.g., ON, OFF, EXIT): ').upper()
        print(command)
        serial_inst.write(command.encode('utf-8'))

        if command == 'EXIT':
            break
except serial.SerialException as e:
    print(f'Error: {e}')
except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    if serial_inst.is_open:
        serial_inst.close()
        print(f'Disconnected from {port_var}')
