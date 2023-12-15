import sys
from typing import List

sys.path.append("/home/pedro/Github/GerenciaDeRedes/entrega_t3/descoberta_dispositivos")
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
            devices.append(new_device)
        else:
            new_device = Device(ip, "-", "-", "off")
            devices.append(new_device)
    else:
        new_device = Device(ip, "-", "-", "off")
        devices.append(new_device)


def run_discovery(network_cidr: str):
    timeout = 0.2
    ips_in_network = get_all_ips_in_network(network_cidr)

    devices: List[Device] = []

    for ip in ips_in_network:
        ping_and_print_info(ip, timeout, devices)

    return devices
