from pysnmp.hlapi import *

errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(
        SnmpEngine(),
        CommunityData("public", mpModel=0),
        UdpTransportTarget(("demo.snmplabs.com", 161)),
        ContextData(),
        ObjectType(ObjectIdentity("1.3.6.1.2.1.17.7.1.2.2.1.2")),
    )
)

if errorIndication or errorStatus:
    print(errorIndication or errorStatus)
else:
    for varBind in varBinds:
        print(" = ".join([x.prettyPrint() for x in varBind]))
