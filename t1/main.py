from ping3 import ping
import ipaddress
import concurrent.futures
from mac_address_from_ip import get_device_info
import math


def get_all_ips_in_network(network_cidr):
    try:
        network = ipaddress.IPv4Network(network_cidr, strict=False)
        ip_list = [
            str(ip) for ip in network.hosts()
        ]
        return ip_list
    except ValueError as e:
        return str(e)

def ping_ip(ip):
    response = ping(ip)
    if response != None and response != False:
        device_info = get_device_info(ip)
        if (device_info != None):
            print (f"Host: {ip} is up MAC: {device_info.mac} is_router: {device_info.is_router}")
        else:
            print (f"Host: {ip} is up can't get device information")

    else: 
        print (f"Host: {ip} is down {response}")

# Example usage:
network_cidr = "192.168.130.0/24"
ips_in_network = get_all_ips_in_network(network_cidr)
print(ips_in_network)

if ips_in_network:
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(ping_ip, ips_in_network)
else:
    print(f"Invalid network CIDR: {network_cidr}")
    
