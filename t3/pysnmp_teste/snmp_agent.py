#Trabalho 3 de Gerência de Redes
#Grupo: Jordano Xavier, Pedro Henrique Warken e Renan Bick


from pysnmp.hlapi import *

# Definição das informações dos dispositivos (simuladas)
devices = [
    {'ipAddress': '192.168.1.1', 'macAddress': '00:11:22:33:44:55', 'deviceName': 'Device 1', 'status': 1},
    {'ipAddress': '192.168.1.2', 'macAddress': 'AA:BB:CC:DD:EE:FF', 'deviceName': 'Device 2', 'status': 2}
]

# Função para retornar a lista de dispositivos descobertos
def get_device_table():
    table = []
    for device in devices:
        ip = device['ipAddress']
        mac = bytes.fromhex(device['macAddress'].replace(':', ''))
        name = device['deviceName']
        status = device['status']

        entry = {
            'ipAddress': ip,
            'macAddress': OctetString(mac),
            'deviceName': OctetString(name),
            'status': Integer32(status)
        }
        table.append(entry)

    return table

def snmp_agent():
    # Cria um agente SNMP
    snmp_engine = SnmpEngine()

    # Define os OIDs da MIB
    ipAddress_oid = ObjectIdentity('DEVICE-DISCOVERY', '1')
    macAddress_oid = ObjectIdentity('DEVICE-DISCOVERY', '2')
    deviceName_oid = ObjectIdentity('DEVICE-DISCOVERY', '3')
    status_oid = ObjectIdentity('DEVICE-DISCOVERY', '4')
    deviceTable_oid = ObjectIdentity('DEVICE-DISCOVERY', '5')

    # Cria o gerador para responder às solicitações SNMP
    snmp_gen = getCmd(
        snmp_engine,
        CommunityData('public', mpModel=0),
        UdpTransportTarget(('127.0.0.1', 161)),
        ContextData(),
        ObjectType(ipAddress_oid),
        ObjectType(macAddress_oid),
        ObjectType(deviceName_oid),
        ObjectType(status_oid),
        ObjectType(deviceTable_oid)
    )

    # Processa as solicitações SNMP
    for (errorIndication, errorStatus, errorIndex, varBinds) in snmp_gen:
        if errorIndication:
            print(errorIndication)
            break
        elif errorStatus:
            print(f'{errorStatus.prettyPrint()} at {errorIndex}')
            break
        else:
            # Retorna a tabela de dispositivos descobertos quando solicitado
            if varBinds[0][0] == ipAddress_oid:
                device_table = get_device_table()
                for entry in device_table:
                    for oid, value in entry.items():
                        print(f'{oid} = {value}')

if __name__ == '__main__':
    snmp_agent()