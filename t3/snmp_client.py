from pysnmp.hlapi import *


def send_snmp_request():
    target_host = "localhost"
    target_port = 162
    community_string = "public"
    sys_descr_oid = "1.3.6.4.1.5.3"  # sysDescr object OID

    errorIndication, errorStatus, errorIndex, varBinds = next(
        nextCmd(
            SnmpEngine(),
            CommunityData(community_string, mpModel=0),
            UdpTransportTarget((target_host, target_port), timeout=30),
            ContextData(),
            ObjectType(ObjectIdentity(sys_descr_oid)),
        )
    )

    if errorIndication:
        print(f"Error: {errorIndication}")
    elif errorStatus:
        print(f"Error: {errorStatus}")
    else:
        for varBind in varBinds:
            print(f"{varBind[0]} = {varBind[1]}")


if __name__ == "__main__":
    send_snmp_request()
