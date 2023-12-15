import sys
from typing import List

from concurrent.futures import ThreadPoolExecutor
from ping3 import ping
import ipaddress
from get_device_info import get_device_info
from get_manufacturer import load_oui_database, get_mac_manufacturer


def is_router(ip):
    return ip.endswith(".1") or ip.endswith(".254")


def get_all_ips_in_network(network_cidr):
    try:
        network = ipaddress.IPv4Network(network_cidr, strict=False)
        ip_list = [str(ip) for ip in network.hosts()]
        return ip_list
    except ValueError as e:
        return str(e)


class Device:
    def __init__(self, ipAddress: str, macAddress: str, vendor: str, status: str):
        self.ipAddress = ipAddress
        self.macAddress = macAddress
        self.vendor = vendor
        self.status = status


def ping_and_print_info(ip, timeout, devices: list):
    oui_database = load_oui_database()
    response = ping(ip, timeout)
    if response is not None and response is not False:
        device_info = get_device_info(ip)
        if device_info is not None:
            new_device = Device(
                ip,
                device_info["mac"],
                get_mac_manufacturer(device_info["mac"], oui_database),
                "on",
            )
            print(
                ip,
                new_device.macAddress,
                new_device.vendor,
                new_device.status,
            )
            devices.append(new_device)
        else:
            new_device = Device(ip, "-", "-", "off")
            print(
                new_device.ipAddress,
                new_device.macAddress,
                new_device.vendor,
                new_device.status,
            )
            devices.append(new_device)
    else:
        new_device = Device(ip, "-", "-", "off")
        print(
            new_device.ipAddress,
            new_device.macAddress,
            new_device.vendor,
            new_device.status,
        )
        devices.append(new_device)


def run_discovery(network_cidr: str):
    timeout = 0.1
    max_workers = 1
    ips_in_network = get_all_ips_in_network(network_cidr)

    devices: List[Device] = []

    # with ThreadPoolExecutor(max_workers=max_workers) as executor:
    #     futures = [
    #         executor.submit(ping_and_print_info, ip, timeout, devices)
    #         for ip in ips_in_network
    #     ]

    # for future in futures:
    #     future.result()
    for ip in ips_in_network:
        ping_and_print_info(ip, timeout, devices)

    return devices


if __name__ == "__main__":
    run_discovery("192.168.0.1/24")
