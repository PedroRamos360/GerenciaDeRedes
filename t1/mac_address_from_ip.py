from scapy.all import ARP, Ether, srp

def get_device_info(ip_address):
    arp = ARP(pdst=ip_address)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    results, _ = srp(packet, timeout=2, verbose=False)

    device_info = None
    for received in results:
        device_info = {
            "mac": received.hwsrc,
            "is_router": received.psrc != ip_address
        }

    return device_info