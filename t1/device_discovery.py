import sys

sys.path.append("/home/pedro/Github/GerenciaDeRedes")
from concurrent.futures import ThreadPoolExecutor
from ping3 import ping
import ipaddress
from t1.get_device_info import get_device_info
from t1.get_manufacturer import load_oui_database, get_mac_manufacturer


def is_router(ip):
    return ip.endswith(".1") or ip.endswith(".254")


def get_all_ips_in_network(network_cidr):
    try:
        network = ipaddress.IPv4Network(network_cidr, strict=False)
        ip_list = [str(ip) for ip in network.hosts()]
        return ip_list
    except ValueError as e:
        return str(e)


def ping_and_print_info(ip, timeout, devices: list):
    oui_database = load_oui_database()
    response = ping(ip, timeout)
    if response is not None and response is not False:
        device_info = get_device_info(ip)
        if device_info is not None:
            new_device = {
                "ipAddress": ip,
                "macAddress": device_info["mac"],
                "vendor": get_mac_manufacturer(device_info["mac"], oui_database),
                "status": True,
            }
            devices.append(new_device)
            print(
                f"Host: {ip} is up MAC: {device_info['mac']} Vendor: {get_mac_manufacturer(device_info['mac'], oui_database)} Is Router: {is_router(ip)}"
            )
        else:
            new_device = {
                "ipAddress": ip,
                "macAddress": None,
                "vendor": None,
                "status": False,
            }
            devices.append(new_device)
            print(
                f"Host: {ip} is up MAC: Not found Vendor: Not found Is Router: {is_router(ip)}"
            )
    else:
        new_device = {
            "ipAddress": ip,
            "macAddress": None,
            "vendor": None,
            "status": False,
        }
        devices.append(new_device)

        print(f"Host: {ip} is down")


def run_discovery():
    timeout = 5
    max_workers = 10
    network_cidr = input("Enter network CIDR: ")
    ips_in_network = get_all_ips_in_network(network_cidr)

    devices = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(ping_and_print_info, ip, timeout, devices)
            for ip in ips_in_network
        ]

    for future in futures:
        future.result()

    return devices
