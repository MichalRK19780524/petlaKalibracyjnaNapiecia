# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
from typing import Dict
import csv
import time
import lanconnection

epsilon = 0.000001
ip = '10.2.0.126'
port = 5555
bar_id = 12

default_file_name = 'stability_time3.csv'


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def save_in_file(_headers, _data: list[Dict[str, float]],
                 file_name: str = default_file_name):
    if os.path.exists(file_name):
        raise Exception("File already exists!")

    with open(file_name, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=_headers)
        writer.writeheader()
        writer.writerows(_data)


def measure(voltage: float, connection: lanconnection.LanConnection) -> (float, int, int, float, int, int):
    result = connection.do_cmd(['setdac', bar_id, voltage, voltage])
    set_master = None
    set_slave = None
    if result[0] == 'ERR':
        print('Error when setdac')
    else:
        set_master = result[1][0]
        set_slave = result[1][1]
    measured_master = connection.do_cmd(['adc', bar_id, 3])[1]
    measured_slave = connection.do_cmd(['adc', bar_id, 4])[1]
    return voltage, set_master, measured_master, voltage, set_slave, measured_slave


def measure2(connection: lanconnection.LanConnection) -> (int, int):
    measured_master = connection.do_cmd(['adc', bar_id, 3])[1]
    measured_slave = connection.do_cmd(['adc', bar_id, 4])[1]
    return measured_master, measured_slave


def stability(amount: int, voltage: float):
    connection = lanconnection.LanConnection(ip, port)
    result = connection.do_cmd(['init', bar_id])
    if result[0] == 'ERR':
        print("Error when init")

    result = connection.do_cmd(['hvon', bar_id])
    if result[0] == 'ERR':
        print("Error when hvon")

    _headers = ('Number', 'Voltage U[V]', 'master measured U[bit]', 'slave measured U[bit]')

    data = []
    for i in range(amount):
        measure_dict = {}
        result = measure(voltage, connection)
        measure_dict[_headers[0]] = i
        measure_dict[_headers[1]] = voltage
        measure_dict[_headers[2]] = result[2]
        measure_dict[_headers[3]] = result[5]
        data.append(measure_dict)
        print(i)

    save_in_file(_headers, data)

    result = connection.do_cmd(['hvoff', bar_id])
    if result[0] == 'ERR':
        print("Error when hvoff")
    connection.close_connection()


def stability2(end_date: float, step: float, voltage: float):
    connection = lanconnection.LanConnection(ip, port)
    result = connection.do_cmd(['init', bar_id])
    if result[0] == 'ERR':
        print("Error when init")

    result = connection.do_cmd(['hvon', bar_id])
    if result[0] == 'ERR':
        print("Error when hvon")

    _headers = ('date UTC since epoch [s]', 'Voltage U[V]', 'master measured U[bit]', 'slave measured U[bit]')
    time.sleep(5.0)
    current_time = time.time()
    print(current_time)
    data = []
    while current_time < end_date:
        measure_dict = {}
        time.sleep(step)
        result = measure(voltage, connection)
        current_time = time.time()
        measure_dict[_headers[0]] = current_time
        measure_dict[_headers[1]] = voltage
        measure_dict[_headers[2]] = result[2]
        measure_dict[_headers[3]] = result[5]
        data.append(measure_dict)
        print(current_time)

    save_in_file(_headers, data)

    result = connection.do_cmd(['hvoff', bar_id])
    if result[0] == 'ERR':
        print("Error when hvoff")
    connection.close_connection()


def stability3(end_date: float, step: float, voltage: float, file_name: str):
    connection = lanconnection.LanConnection(ip, port)
    result = connection.do_cmd(['init', bar_id])
    if result[0] == 'ERR':
        print("Error when init")
    print("init OK")

    result = connection.do_cmd(['hvon', bar_id])
    if result[0] == 'ERR':
        print("Error when hvon")
    print("hvon OK")

    if os.path.exists(file_name):
        raise Exception("File already exists!")

    _headers = ('date UTC since epoch [s]', 'Voltage U[V]', 'master measured U[bit]', 'slave measured U[bit]')
    with open(file_name, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=_headers)
        writer.writeheader()
        time.sleep(5.0)
        current_time = time.time()
        print(current_time)
        while current_time < end_date:
            measure_dict = {}
            time.sleep(step)
            result = measure(voltage, connection)
            current_time = time.time()
            measure_dict[_headers[0]] = current_time
            measure_dict[_headers[1]] = voltage
            measure_dict[_headers[2]] = result[2]
            measure_dict[_headers[3]] = result[5]
            writer.writerow(measure_dict)
            print(current_time)

    result = connection.do_cmd(['hvoff', bar_id])
    if result[0] == 'ERR':
        print("Error when hvoff")
    connection.close_connection()

def stability4(end_date: float, step: float, voltage: float, file_name: str):
    connection = lanconnection.LanConnection(ip, port)
    voltage_result = connection.do_cmd(['init', bar_id])
    if voltage_result[0] == 'ERR':
        print("Error when init")
    print("init OK")

    voltage_result = connection.do_cmd(['hvon', bar_id])
    if voltage_result[0] == 'ERR':
        print("Error when hvon")
    print("hvon OK")

    if os.path.exists(file_name):
        raise Exception("File already exists!")

    _headers = ('date UTC since epoch [s]', 'Voltage U[V]', 'Voltage U[bit]', 'master measured U[bit]', 'slave measured U[bit]')

    with open(file_name, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=_headers)
        writer.writeheader()
        time.sleep(10.0)
        current_time = time.time()
        print(current_time)
        voltage_result = connection.do_cmd(['setdac', bar_id, voltage, voltage])
        print(voltage_result)
        while current_time < end_date:
            measure_dict = {}
            time.sleep(step)
            result = measure2(connection)
            current_time = time.time()
            measure_dict[_headers[0]] = current_time
            measure_dict[_headers[1]] = voltage
            measure_dict[_headers[2]] = voltage_result[1][0]
            measure_dict[_headers[3]] = result[0]
            measure_dict[_headers[4]] = result[1]
            writer.writerow(measure_dict)
            print(current_time)

def voltage_in_range(start: float, stop: float, step: float):
    connection = lanconnection.LanConnection(ip, port)

    result = connection.do_cmd(['init', bar_id])
    if result[0] == 'ERR':
        print("Error when init")

    result = connection.do_cmd(['hvon', bar_id])
    if result[0] == 'ERR':
        print("Error when hvon")

    voltage = start
    _headers = ('master set U[V]', 'master set U[bit]', 'master measured U[bit]', 'slave set U[V]', 'slave set U[bit]',
                'slave measured U[bit]')
    data = []
    while voltage < stop + epsilon:
        results = measure(voltage, connection)
        voltage += step
        measure_dict = {}
        for i in range(6):
            measure_dict[_headers[i]] = results[i]
        data.append(measure_dict)

    save_in_file(_headers, data)

    result = connection.do_cmd(['hvoff', bar_id])
    if result[0] == 'ERR':
        print("Error when hvoff")
    connection.close_connection()


if __name__ == '__main__':
    # voltage_in_range(53.0, 68.0, 0.1)
    # stability(10, 59.5)
    stability4(1650021600, 0, 59.5, default_file_name)

