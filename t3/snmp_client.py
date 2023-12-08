from pysnmp.hlapi import *


def send_snmp_request():
    target_host = "localhost"
    target_port = 162
    community_string = "public"
    sys_descr_oid = "1.3.6.1.2.1.1.1.0"  # sysDescr object OID
    sys_descr_oid = "1.3.6.4.1.5.3"  # sysDescr object OID

    errorIndication, errorStatus, errorIndex, varBinds = next(
        bulkCmd(
            SnmpEngine(),
            CommunityData(community_string, mpModel=0),
            UdpTransportTarget((target_host, target_port)),
            ContextData(),
            0,
            25,
            ObjectType(ObjectIdentity(sys_descr_oid)),
        )
    )

    # print(
    #     {
    #         "errorIndication": errorIndication,
    #         "errorStatus": errorStatus,
    #         "errorIndex": errorIndex,
    #         "varBinds": varBinds,
    #     }
    # )

    if errorIndication:
        print(f"Error: {errorIndication}")
    elif errorStatus:
        print(f"Error: {errorStatus}")
    else:
        for varBind in varBinds:
            print(f"{varBind[0]} = {varBind[1]}")


if __name__ == "__main__":
    send_snmp_request()
