from concurrent.futures import ThreadPoolExecutor
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

def ping_and_print_info(ip):
    response = ping(ip, 1)
    if response is not None and response is not False:
        for i in range(3):
            device_info = get_device_info(ip)
            if device_info is not None:
                print(
                    f"Host: {ip} is up MAC: {device_info['mac']} Vendor: {get_mac_manufacturer(device_info['mac'], oui_database)} is router: {device_info['is_router']}"
                )
                break
            else:
                print(f"Host: {ip} is up can't get device information, trying again...")
    else:
        print(f"Host: {ip} is down")

if __name__ == "__main__":
    network_cidr = input("Enter network CIDR: ")
    ips_in_network = get_all_ips_in_network(network_cidr)

    
    with ThreadPoolExecutor(max_workers=10) as executor:  
        futures = [executor.submit(ping_and_print_info, ip) for ip in ips_in_network]

    for future in futures:
        future.result()
