from pysnmp.hlapi import *

# MIB definition
MIB = {
    "ipAddress": "1.3.6.1.4.1.9999.1",
    "macAddress": "1.3.6.1.4.1.9999.2",
    "deviceName": "1.3.6.1.4.1.9999.3",
    "status": "1.3.6.1.4.1.9999.4",
    "deviceTable": "1.3.6.1.4.1.9999.5",
}

# Dummy data
device_data = [
    {
        "ipAddress": "192.168.1.1",
        "macAddress": "00:11:22:33:44:55",
        "deviceName": "Device1",
        "status": 1,
    },
    {
        "ipAddress": "192.168.1.2",
        "macAddress": "11:22:33:44:55:66",
        "deviceName": "Device2",
        "status": 2,
    },
]


def create_varbind(oid, value):
    return ObjectType(ObjectIdentity(oid), value)


def get_device_table():
    return [
        create_varbind(
            MIB["deviceTable"],
            [
                create_varbind(MIB["ipAddress"], i["ipAddress"]),
                create_varbind(MIB["macAddress"], i["macAddress"]),
                create_varbind(MIB["deviceName"], i["deviceName"]),
                create_varbind(MIB["status"], i["status"]),
            ],
        )
        for i in device_data
    ]


def agent():
    for errorIndication, errorStatus, errorIndex, varBinds in bulkCmd(
        SnmpEngine(),
        CommunityData("public"),
        UdpTransportTarget(("localhost", 161)),
        ContextData(),
        0,
        25,
        ObjectType(ObjectIdentity(MIB["deviceTable"])),
    ):
        if errorIndication or errorStatus:
            print(f"Error: {errorIndication}, {errorStatus}, {errorIndex}")
            break
        else:
            for varBind in varBinds:
                print(varBind)


if __name__ == "__main__":
    agent()
