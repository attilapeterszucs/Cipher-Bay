import sys
from pymodbus.client import ModbusTcpClient

MODBUS_PORT = 502

# Exact checks: (address, expected_value)
FC03_CHECKS = []
FC04_CHECKS = [
    (0, 0),
    (1, 200),
]

# Range checks: (address, min_value, max_value)
FC03_RANGE_CHECKS = []
FC04_RANGE_CHECKS = [
    (1, 0, 1000),
    (2, 0, 52),
]


def check_exact(client, fc, address, expected):
    # Read holding registers for FC03, input registers for FC04
    if fc == "FC03":
        response = client.read_holding_registers(address=address, count=1)
    else:
        response = client.read_input_registers(address=address, count=1)

    if response.isError():
        print(f"[{fc}] address {address} - error: {response}")
        return {"Path": ["modbus", fc], "Passed": False}

    value = response.registers[0]
    passed = value == expected
    print(f"[{fc}] address {address} - value={value}, expected={expected}, passed={passed}")
    return {"Path": ["modbus", fc], "Passed": passed}


def check_range(client, fc, address, min_value, max_value):
    if fc == "FC03":
        response = client.read_holding_registers(address=address, count=1)
    else:
        response = client.read_input_registers(address=address, count=1)

    if response.isError():
        print(f"[{fc}] address {address} - error: {response}")
        return {"Path": ["modbus", fc], "Passed": False}

    value = response.registers[0]
    passed = min_value <= value <= max_value
    print(f"[{fc}] address {address} - value={value}, range=[{min_value},{max_value}], passed={passed}")
    return {"Path": ["modbus", fc], "Passed": passed}


def run_checks(host):
    results = []

    client = ModbusTcpClient(host=host, port=MODBUS_PORT)

    if not client.connect():
        # If connection fails, mark all checks as failed
        for address, _ in FC03_CHECKS:
            results.append({"Path": ["modbus", "FC03"], "Passed": False})
            print(f"[FC03] address {address} - connection failed")
        for address, _, _ in FC03_RANGE_CHECKS:
            results.append({"Path": ["modbus", "FC03"], "Passed": False})
            print(f"[FC03] address {address} - connection failed")
        for address, _ in FC04_CHECKS:
            results.append({"Path": ["modbus", "FC04"], "Passed": False})
            print(f"[FC04] address {address} - connection failed")
        for address, _, _ in FC04_RANGE_CHECKS:
            results.append({"Path": ["modbus", "FC04"], "Passed": False})
            print(f"[FC04] address {address} - connection failed")
        return results

    try:
        for address, expected in FC03_CHECKS:
            results.append(check_exact(client, "FC03", address, expected))
        for address, min_value, max_value in FC03_RANGE_CHECKS:
            results.append(check_range(client, "FC03", address, min_value, max_value))
        for address, expected in FC04_CHECKS:
            results.append(check_exact(client, "FC04", address, expected))
        for address, min_value, max_value in FC04_RANGE_CHECKS:
            results.append(check_range(client, "FC04", address, min_value, max_value))
    finally:
        client.close()

    return results


def main():
    args = sys.argv[1:]

    if len(args) != 1:
        print(f"Usage: {sys.argv[0]} <HOST>")
        sys.exit(1)

    host = args[0]
    results = run_checks(host)
    print(results)


if __name__ == "__main__":
    main()