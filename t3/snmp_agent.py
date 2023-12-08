from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context, cmdgen
from pysnmp.proto.api import v2c
from pysnmp import error
import logging
import sys

from pysnmp.proto.rfc1155 import ObjectName

sys.path.append("/home/pedro/Github/GerenciaDeRedes")

from t1.device_discovery import run_discovery

formatting = "[%(asctime)s-%(levelname)s]-(%(module)s) %(message)s"

logging.basicConfig(
    level=logging.DEBUG,
    format=formatting,
)
logging.info("Starting....")

snmpEngine = engine.SnmpEngine()

config.addTransport(
    snmpEngine, udp.domainName, udp.UdpTransport().openServerMode(("localhost", 162))
)
config.addV1System(snmpEngine, "my-area", "public")
config.addVacmUser(snmpEngine, 2, "my-area", "noAuthNoPriv", (1, 3, 6, 4), (1, 3, 6, 4))


snmpContext = context.SnmpContext(snmpEngine)
logging.debug("Loading __DISCOVERY-MIB module..."),
mibBuilder = snmpContext.getMibInstrum().getMibBuilder()
(MibTable, MibTableRow, MibTableColumn, MibScalarInstance) = mibBuilder.importSymbols(
    "SNMPv2-SMI", "MibTable", "MibTableRow", "MibTableColumn", "MibScalarInstance"
)
# logging.debug('done')


(RowStatus,) = mibBuilder.importSymbols("SNMPv2-TC", "RowStatus")

mibBuilder.exportSymbols(
    "__DISCOVERY-MIB",
    exampleTable=MibTable((1, 3, 6, 4, 1)).setMaxAccess("readcreate"),
    exampleTableEntry=MibTableRow((1, 3, 6, 4, 1, 5))
    .setMaxAccess("readcreate")
    .setIndexNames((0, "__DISCOVERY-MIB", "exampleTableColumn1")),
    exampleTableColumn1=MibTableColumn(
        (1, 3, 6, 4, 1, 5, 1), v2c.OctetString()
    ).setMaxAccess("readcreate"),
    exampleTableColumn2=MibTableColumn(
        (1, 3, 6, 4, 1, 5, 2), v2c.IpAddress()
    ).setMaxAccess("readcreate"),
    exampleTableColumn3=MibTableColumn(
        (1, 3, 6, 4, 1, 5, 3), v2c.OctetString()
    ).setMaxAccess("readcreate"),
    exampleTableStatus=MibTableColumn(
        (1, 3, 6, 4, 1, 5, 4), v2c.OctetString()
    ).setMaxAccess("readcreate"),
)
# logging.debug('done')

(
    exampleTableEntry,
    exampleTableColumn2,
    exampleTableColumn3,
    exampleTableStatus,
) = mibBuilder.importSymbols(
    "__DISCOVERY-MIB",
    "exampleTableEntry",
    "exampleTableColumn2",
    "exampleTableColumn3",
    "exampleTableStatus",
)

rowInstanceId = exampleTableEntry.getInstIdFromIndices("example record one")
mibInstrumentation = snmpContext.getMibInstrum()
mibInstrumentation.writeVars(
    (
        (exampleTableColumn2.name + rowInstanceId, "192.168.1.1"),
        (exampleTableColumn3.name + rowInstanceId, "00:1A:2B:3C:4D:5E"),
        (exampleTableStatus.name + rowInstanceId, "Fabricante XYZ"),
    )
)

logging.debug("== Snmp Agent Start == \n")

from pysnmp.proto import rfc1902


class MyNextCommandResponder(cmdrsp.NextCommandResponder):
    def handleMgmtOperation(self, snmpEngine, stateReference, contextName, PDU, acInfo):
        (acFun, acCtx) = acInfo
        # Construct the desired varbind (1.3.6.4.1.5.3, "ok")
        print("Buscando dispositivos na rede...")
        devices = run_discovery("10.0.0.123/29")
        str_devices = ""
        for device in devices:
            mac = device.macAddress
            str_devices += f"\nIP: {device.ipAddress} STATUS: {device.status} MAC: {device.macAddress} VENDOR: {device.vendor}"

        response_varbind = (
            rfc1902.ObjectName((1, 3, 6, 4, 1, 5, 4)),
            rfc1902.OctetString(str_devices),
        )

        # Send the varbind directly
        self.sendVarBinds(snmpEngine, stateReference, 0, 0, [response_varbind])

        # Release state information
        self.releaseStateInformation(stateReference)


MyNextCommandResponder(snmpEngine, snmpContext)
snmpEngine.transportDispatcher.jobStarted(1)

try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise
