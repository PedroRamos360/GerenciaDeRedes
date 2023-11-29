from pysnmp.hlapi import *
import sys

sys.path.append("/home/pedro/Github/GerenciaDeRedes")

from t1.device_discovery import run_discovery

MIB = {
    "ipAddress": "1.3.6.1.4.1.9999.1",
    "macAddress": "1.3.6.1.4.1.9999.2",
    "vendor": "1.3.6.1.4.1.9999.3",
    "status": "1.3.6.1.4.1.9999.4",
    "deviceTable": "1.3.6.1.4.1.9999.5",
}


def create_varbind(oid, value):
    return ObjectType(ObjectIdentity(oid), value)


def get_device_table(device_data: list):
    return [
        create_varbind(
            MIB["deviceTable"],
            [
                create_varbind(MIB["ipAddress"], i["ipAddress"]),
                create_varbind(MIB["macAddress"], i["macAddress"]),
                create_varbind(MIB["vendor"], i["deviceName"]),
                create_varbind(MIB["status"], i["status"]),
            ],
        )
        for i in device_data
    ]


def agent():
    print("SNMP Agent running...")
    for errorIndication, errorStatus, errorIndex, varBinds in bulkCmd(
        SnmpEngine(),
        CommunityData("public"),
        UdpTransportTarget(("localhost", 161), timeout=10),
        ContextData(),
        0,
        25,
        ObjectType(ObjectIdentity(MIB["deviceTable"])),
    ):
        print("Iteration bulkcmd")
        print(
            {
                "errorIndication": errorIndication,
                "errorStatus": errorStatus,
                "errorIndex": errorIndex,
                "varBinds": varBinds,
            }
        )
        if errorIndication or errorStatus:
            print(f"Error: {errorIndication}, {errorStatus}, {errorIndex}")
            break
        else:
            # Get the list of devices using run_discovery
            device_list = run_discovery()
            print(device_list)

            # Respond with the devices
            for varBind in get_device_table(device_list):
                print(varBind)


if __name__ == "__main__":
    agent()
