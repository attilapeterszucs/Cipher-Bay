from pymodbus.client import ModbusTcpClient

HOST = "127.0.0.1"
PORT = 5020

client = ModbusTcpClient(host=HOST, port=PORT)

if not client.connect():
    print("Connection failed")
    exit(1)

# FC03, read holding register at address 0
fc03_address = 0
fc03 = client.read_holding_registers(address=fc03_address, count=1)
if not fc03.isError():
    value = fc03.registers[0]
    if value == 1000:
        print(f"FC03 HR[{fc03_address}] = {value} - expected value")
    else:
        print(f"FC03 HR[{fc03_address}] = {value} - unexpected value")
else:
    print(f"FC03 error: {fc03}")

# FC04, read input register at address 1
fc04_address = 1
fc04 = client.read_input_registers(address=fc04_address, count=1)
if not fc04.isError():
    value = fc04.registers[0]
    if value == 2000:
        print(f"FC04 IR[{fc04_address}] = {value} - expected value")
    else:
        print(f"FC04 IR[{fc04_address}] = {value} - unexpected value")
else:
    print(f"FC04 error: {fc04}")

client.close()