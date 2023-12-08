from scapy.all import ARP, Ether, srp

def get_device_info(ip_address):
    arp = ARP(pdst=ip_address)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    results, _ = srp(packet, timeout=3, verbose=False)

    device_info = []
    for sent, received in results:
        device_info.append({
            "mac": received.hwsrc,
        })

    if len(device_info) == 0:
        return None
    else:
        return device_info[0]

