from pysnmp.hlapi import *

errorIndication, errorStatus, errorIndex, varBinds = next(
    sendNotification(
        SnmpEngine(),
        CommunityData("public"),
        UdpTransportTarget(("demo.snmplabs.com", 162)),
        ContextData(),
        "trap",
        NotificationType(ObjectIdentity("SNMPv2-MIB", "coldStart")),
    )
)

if errorIndication:
    print(errorIndication)
