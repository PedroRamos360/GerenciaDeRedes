from ping3 import ping
import ipaddress
from get_device_info import get_device_info
from get_manufacturer import load_oui_database, get_mac_manufacturer

oui_database = load_oui_database()

def get_all_ips_in_network(network_cidr):
    try:
        network = ipaddress.IPv4Network(network_cidr, strict=False)
        ip_list = [str(ip) for ip in network.hosts()]
        return ip_list
    except ValueError as e:
        return str(e)


def ping_ip(ip):
    response = ping(ip, 1)
    if response != None and response != False:
        for i in range(3):
            device_info = get_device_info(ip)
            if device_info != None:
                print(
                    f"Host: {ip} is up MAC: {device_info['mac']} Vendor: {get_mac_manufacturer(device_info['mac'], oui_database)} is_router: {device_info['is_router']}"
                )
                break
            else:
                print(f"Host: {ip} is up can't get device information, trying again...")

    else:
        print(f"Host: {ip} is down {response}")


# Example usage:
network_cidr = input("Enter network CIDR: ")
ips_in_network = get_all_ips_in_network(network_cidr)
print(ips_in_network)


for ip in ips_in_network:
    ping_ip(ip)