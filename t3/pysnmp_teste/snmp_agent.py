from datetime import datetime
from pysnmp import debug
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.proto.api import v2c
from pysnmp.smi import builder, instrum, exval
import logging

formatting = '[%(asctime)s-%(levelname)s]-(%(module)s) %(message)s'

logging.basicConfig(level=logging.DEBUG, format=formatting, )
logging.info("Starting....")

snmpEngine = engine.SnmpEngine()

config.addTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTransport().openServerMode(('0.0.0.0', 161))
)
config.addV1System(snmpEngine, 'my-area', 'public')
config.addVacmUser(snmpEngine,
                   2,
                   'my-area',
                   'noAuthNoPriv',
                   (1, 3, 6, 4),
                   (1, 3, 6, 4))


snmpContext = context.SnmpContext(snmpEngine)
logging.debug('Loading __EXAMPLE-MIB module...'),
mibBuilder = snmpContext.getMibInstrum().getMibBuilder()
(MibTable,
 MibTableRow,
 MibTableColumn,
 MibScalarInstance) = mibBuilder.importSymbols(
    'SNMPv2-SMI',
    'MibTable',
    'MibTableRow',
    'MibTableColumn',
    'MibScalarInstance'
)
logging.debug('done')


RowStatus, = mibBuilder.importSymbols('SNMPv2-TC', 'RowStatus')

mibBuilder.exportSymbols(
    '__EXAMPLE-MIB',
    # table object
    exampleTable=MibTable((1, 3, 6, 4, 1)).setMaxAccess('readcreate'),
    # table row object, also carries references to table indices
    exampleTableEntry=MibTableRow((1, 3, 6, 4, 1, 5)).setMaxAccess('readcreate').setIndexNames((0, '__EXAMPLE-MIB', 'exampleTableColumn1')),
    # table column: string index
    exampleTableColumn1=MibTableColumn((1, 3, 6, 4, 1, 5, 1), v2c.OctetString()).setMaxAccess('readcreate'),
    # table column: string value
    exampleTableColumn2=MibTableColumn((1, 3, 6, 4, 1, 5, 2), v2c.IpAddress()).setMaxAccess('readcreate'),
    # table column: integer value with default
    exampleTableColumn3=MibTableColumn((1, 3, 6, 4, 1, 5, 3), v2c.OctetString()).setMaxAccess('readcreate'),
    # table column: row status
    exampleTableStatus=MibTableColumn((1, 3, 6, 4, 1, 5, 4), v2c.OctetString()).setMaxAccess('readcreate')
)
logging.debug('done')

(exampleTableEntry,
 exampleTableColumn2,
 exampleTableColumn3,
 exampleTableStatus) = mibBuilder.importSymbols(
    '__EXAMPLE-MIB',
    'exampleTableEntry',
    'exampleTableColumn2',
    'exampleTableColumn3',
    'exampleTableStatus'
)

rowInstanceId = exampleTableEntry.getInstIdFromIndices('example record one')
mibInstrumentation = snmpContext.getMibInstrum()
mibInstrumentation.writeVars(
    ((exampleTableColumn2.name + rowInstanceId, '192.168.1.1'),
     (exampleTableColumn3.name + rowInstanceId, '00:1A:2B:3C:4D:5E'),
     (exampleTableStatus.name + rowInstanceId, 'Fabricante XYZ'))
)

logging.debug('done')
logging.debug('Snmp Agent Start')

cmdrsp.GetCommandResponder(snmpEngine, snmpContext)
cmdrsp.SetCommandResponder(snmpEngine, snmpContext)
cmdrsp.NextCommandResponder(snmpEngine, snmpContext)
cmdrsp.BulkCommandResponder(snmpEngine, snmpContext)
snmpEngine.transportDispatcher.jobStarted(1)

try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise