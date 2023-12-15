import re


def load_oui_database():
    oui_database = {}
    with open("mac_vendors.txt", "r") as file:
        for line in file:
            parts = line.strip().split("\t")
            if len(parts) >= 2:
                oui = parts[0].strip()
                manufacturer = parts[1].strip()
                oui_database[oui] = manufacturer
    return oui_database


def get_mac_manufacturer(mac_address, oui_database):
    mac_address = re.sub(r"[^0-9a-fA-F]", "", mac_address)
    oui = mac_address[:6].upper()

    manufacturer = oui_database.get(oui, "Manufacturer not found")
    return manufacturer
