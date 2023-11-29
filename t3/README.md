# Informações utéis para o projeto
- Link do repositório do pysnmp: https://github.com/etingof/pysnmp
- Link para documentação do pysnmp: https://www.pysnmp.com/pysnmp/docs/pysnmp-hlapi-tutorial#creating-snmp-engine

# Tipos de mensagem SNMP
GetRequest (GET): The SNMP manager sends a GetRequest message to request the value of one or more specified managed objects from the SNMP agent.

GetNextRequest (GETNEXT): Similar to GetRequest, but used to retrieve the next variable in the MIB tree. This allows for efficiently walking through the MIB tree.

GetBulkRequest (GETBULK): Introduced in SNMPv2, GetBulkRequest is used to efficiently retrieve large amounts of data from the agent in a single request. This reduces the number of round-trip communications.

SetRequest (SET): The SNMP manager sends a SetRequest message to modify the value of a specified managed object on the SNMP agent.

Response (RESPONSE): The SNMP agent responds to GetRequest, GetNextRequest, GetBulkRequest, and SetRequest messages with a Response message. This message includes the requested information or an acknowledgment of the completed SetRequest.

Trap: Traps are unsolicited messages sent by SNMP agents to notify the SNMP manager of specific events or conditions. There are standard traps defined in MIB-II (such as coldStart, linkDown, linkUp) and enterprise-specific traps.

InformRequest (INFORM): Introduced in SNMPv2, InformRequest is similar to Trap, but it expects acknowledgment (Response) from the SNMP manager. This helps in ensuring reliable delivery of the notification.

Report: Introduced in SNMPv3, a Report message is used to convey information about the handling of SNMPv3 messages between the manager and agent.

OBS: Acho que a ideia é que a gente rode o programa do t1, guarde os dados na MIB e prepare ela pra
responder as bulk e get requests do manager