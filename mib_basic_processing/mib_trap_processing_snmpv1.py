import os
import re
import argparse
from logging import exception
import logging
import csv


# dictionary to hold IANA SMI numbers.
iana_smi_numbers = {
    '1': 'iso',
    '1.3': 'org',
    '1.3.6': 'dod',
    '1.3.6.1': 'internet',
    '1.3.6.1.1': 'directory',
    '1.3.6.1.2': 'mgmt',
    '1.3.6.1.2.1': 'mib-2',
    '1.3.6.1.2.1.2.2.1.3': 'ifType',
    '1.3.6.1.2.1.10': 'transmission',
    '1.3.6.1.2.1.10.23': 'transmissionppp',
    '1.3.6.1.2.1.27': 'application',
    '1.3.6.1.2.1.28': 'mta',
    '1.3.6.1.2.2': 'pib',
    '1.3.6.1.3': 'experimental',
    '1.3.6.1.4': 'private',
    '1.3.6.1.4.1': 'enterprises',
    '1.3.6.1.5': 'security',
    '1.3.6.1.6': 'SNMPv2',
    '1.3.6.1.6.1': 'snmpDomains',
    '1.3.6.1.6.2': 'snmpProxys',
    '1.3.6.1.6.3': 'snmpModules',
    '1.3.6.1.7': 'mail',
    '1.3.6.1.8': 'features'
}

# dictionary to hold IANA SMI names to numbers.
iana_smi_name_to_numbers = {
    'iso': '1',
    'org': '1.3',
    'dod': '1.3.6',
    'internet': '1.3.6.1',
    'directory': '1.3.6.1.1',
    'mgmt': '1.3.6.1.2',
    'mib-2': '1.3.6.1.2.1',
    'ifType': '1.3.6.1.2.1.2.2.1.3',
    'transmission': '1.3.6.1.2.1.10',
    'transmissionppp': '1.3.6.1.2.1.10.23',
    'application': '1.3.6.1.2.1.27',
    'mta': '1.3.6.1.2.1.28',
    'pib': '1.3.6.1.2.2',
    'experimental': '1.3.6.1.3',
    'private': '1.3.6.1.4',
    'enterprises': '1.3.6.1.4.1',
    'security': '1.3.6.1.5',
    'SNMPv2': '1.3.6.1.6',
    'snmpDomains': '1.3.6.1.6.1',
    'snmpProxys': '1.3.6.1.6.2',
    'snmpModules': '1.3.6.1.6.3',
    'mail': '1.3.6.1.7',
    'features': '1.3.6.1.8',
    'ems': '1.3.6.1.4.1.169.3.12',
    'host': '1.3.6.1.2.1.25',
    'hrDevice': '1.3.6.1.2.1.25.3',
    'hrDeviceAudio': '1.3.6.1.2.1.25.3.1.11',
    'hrDeviceClock': '1.3.6.1.2.1.25.3.1.19',
    'hrDeviceCoprocessor': '1.3.6.1.2.1.25.3.1.12',
    'hrDeviceDiskStorage': '1.3.6.1.2.1.25.3.1.6',
    'hrDeviceKeyboard': '1.3.6.1.2.1.25.3.1.13',
    'hrDeviceModem': '1.3.6.1.2.1.25.3.1.14',
    'hrDeviceNetwork': '1.3.6.1.2.1.25.3.1.4',
    'hrDeviceNonVolatileMemory': '1.3.6.1.2.1.25.3.1.21',
    'hrDeviceOther': '1.3.6.1.2.1.25.3.1.1',
    'hrDeviceParallelPort': '1.3.6.1.2.1.25.3.1.15',
    'hrDevicePointing': '1.3.6.1.2.1.25.3.1.16',
    'hrDevicePrinter': '1.3.6.1.2.1.25.3.1.5',
    'hrDeviceProcessor': '1.3.6.1.2.1.25.3.1.3',
    'hrDeviceSerialPort': '1.3.6.1.2.1.25.3.1.17',
    'hrDeviceTape': '1.3.6.1.2.1.25.3.1.18',
    'hrDeviceTypes': '1.3.6.1.2.1.25.3.1',
    'hrDeviceUnknown': '1.3.6.1.2.1.25.3.1.2',
    'hrDeviceVideo': '1.3.6.1.2.1.25.3.1.10',
    'hrDeviceVolatileMemory': '1.3.6.1.2.1.25.3.1.20',
    'hrFSAFS': '1.3.6.1.2.1.25.3.9.16',
    'hrFSAppleshare': '1.3.6.1.2.1.25.3.9.18',
    'hrFSBerkeleyFFS': '1.3.6.1.2.1.25.3.9.3',
    'hrFSBFS': '1.3.6.1.2.1.25.3.9.21',
    'hrFSDFS': '1.3.6.1.2.1.25.3.9.17',
    'hrFSDGCFS': '1.3.6.1.2.1.25.3.9.20',
    'hrFSFat': '1.3.6.1.2.1.25.3.9.5',
    'hrFSHFS': '1.3.6.1.2.1.25.3.9.7',
    'hrFSHPFS': '1.3.6.1.2.1.25.3.9.6',
    'hrFSiso9660': '1.3.6.1.2.1.25.3.9.12',
    'hrFSJournaled': '1.3.6.1.2.1.25.3.9.11',
    'hrFSMFS': '1.3.6.1.2.1.25.3.9.8',
    'hrFSNetware': '1.3.6.1.2.1.25.3.9.15',
    'hrFSNFS': '1.3.6.1.2.1.25.3.9.14',
    'hrFSNTFS': '1.3.6.1.2.1.25.3.9.9',
    'hrFSOther': '1.3.6.1.2.1.25.3.9.1',
    'hrFSRFS': '1.3.6.1.2.1.25.3.9.19',
    'hrFSRockRidge': '1.3.6.1.2.1.25.3.9.13',
    'hrFSSys5FS': '1.3.6.1.2.1.25.3.9.4',
    'hrFSTypes': '1.3.6.1.2.1.25.3.9',
    'hrFSUnknown': '1.3.6.1.2.1.25.3.9.2',
    'hrFSVNode': '1.3.6.1.2.1.25.3.9.10',
    'hrStorage': '1.3.6.1.2.1.25.2',
    'hrStorageCompactDisc': '1.3.6.1.2.1.25.2.1.7',
    'hrStorageFixedDisk': '1.3.6.1.2.1.25.2.1.4',
    'hrStorageFloppyDisk': '1.3.6.1.2.1.25.2.1.6',
    'hrStorageOther': '1.3.6.1.2.1.25.2.1.1',
    'hrStorageRam': '1.3.6.1.2.1.25.2.1.2',
    'hrStorageRamDisk': '1.3.6.1.2.1.25.2.1.8',
    'hrStorageRemovableDisk': '1.3.6.1.2.1.25.2.1.5',
    'hrStorageTypes': '1.3.6.1.2.1.25.2.1',
    'hrStorageVirtualMemory': '1.3.6.1.2.1.25.2.1.3',
    'hrSWInstalled': '1.3.6.1.2.1.25.6',
    'hrSWRun': '1.3.6.1.2.1.25.4',
    'hrSWRunPerf': '1.3.6.1.2.1.25.5',
    'hrSystem': '1.3.6.1.2.1.25.1',
    'nonstopsystems': '1.3.6.1.4.1.169.3',
    'snmp': '1.3.6.1.4.1.169.3.155',
    'snmpagent': '1.3.6.1.4.1.169.3.155.1',
    'tandem': '1.3.6.1.4.1.169',
    'zagInternal': '1.3.6.1.4.1.169.3.155.1.7',
    'zesa': '1.3.6.1.4.1.169.3.217',
    'zhrm': '1.3.6.1.4.1.169.3.180',
    'zhrmDevUnavail': '1.3.6.1.4.1.169.3.180.3',
    'zhrmInfCpuTable': '1.3.6.1.4.1.169.3.180.1.3',
    'zhrmInfDevTable': '1.3.6.1.4.1.169.3.180.1.2',
    'zhrmInfDiskTable': '1.3.6.1.4.1.169.3.180.1.6',
    'zhrmInfFSTable': '1.3.6.1.4.1.169.3.180.1.8',
    'zhrmInfNetTable': '1.3.6.1.4.1.169.3.180.1.4',
    'zhrmInfPartTable': '1.3.6.1.4.1.169.3.180.1.7',
    'zhrmInfPrnTable': '1.3.6.1.4.1.169.3.180.1.5',
    'zhrmInfStorTable': '1.3.6.1.4.1.169.3.180.1.1',
    'zhrmRefresh': '1.3.6.1.4.1.169.3.180.5',
    'zhrmSaProcess': '1.3.6.1.4.1.169.3.180.4',
    'zhrmTableInfo': '1.3.6.1.4.1.169.3.180.1',
    'zhrmThrDisk': '1.3.6.1.4.1.169.3.180.2.2',
    'zhrmThreshold': '1.3.6.1.4.1.169.3.180.2',
    'zhrmThrRAM': '1.3.6.1.4.1.169.3.180.2.1',
    'zhrmTraps': '1.3.6.1.4.1.169.3.180.7',
    'zsmp': '1.3.6.1.4.1.169.3.155',
    'zsmpagent': '1.3.6.1.4.1.169.3.155.1',
    'ztmx': '1.3.6.1.4.1.169.3.185',
    'ztmxPDUStatistics': '1.3.6.1.4.1.169.3.185.1',
    'ztmxProcess': '1.3.6.1.4.1.169.3.185.2',
    'ztmxSpecial': '1.3.6.1.4.1.169.3.185.3',
    'ztmxTrapStatistics': '1.3.6.1.4.1.169.3.185.1.9'
}

ins_mibs_dictionary = {
    'tandem': '1.3.6.1.4.1.169',
    'nonstopsystems': '1.3.6.1.4.1.169.3 ',
    'ems': '1.3.6.1.4.1.169.3.12 ',
    'ntsp': '1.3.6.1.4.1.169.10 ',
    'ins': '1.3.6.1.4.1.169.10.1 ',
    'insErad': '1.3.6.1.4.1.169.10.1.1 ',
    'insStats': '1.3.6.1.4.1.169.10.1.2 ',
    'insNwConfig': '1.3.6.1.4.1.169.10.1.3 ',
    'insEradInfo': '1.3.6.1.4.1.169.10.1.1.10'
}

sim_mib_dictionary = {
    'bt2Traps': '1.3.6.1.4.1.11.2.3.7.11.33.1.2.7',
    'coloradosprings': '1.3.6.1.4.1.1123.3',
    'compaq': '1.3.6.1.4.1.232',
    'cpqPower': '1.3.6.1.4.1.232.165',
    'cpqDaCntlr': '1.3.6.1.4.1.232.3.2.2',
    'cpqDaCntlrPerf': '1.3.6.1.4.1.232.3.2.7',
    'cpqDaComponent': '1.3.6.1.4.1.232.3.2',
    'cpqDaInterface': '1.3.6.1.4.1.232.3.2.1',
    'cpqDaLogDrv': '1.3.6.1.4.1.232.3.2.3',
    'cpqDaLogDrvPerf': '1.3.6.1.4.1.232.3.2.8',
    'cpqDaMibRev': '1.3.6.1.4.1.232.3.1',
    'cpqDaOsCommon': '1.3.6.1.4.1.232.3.2.1.4',
    'cpqDaOsNetWare3x': '1.3.6.1.4.1.232.3.2.1.1',
    'cpqDaPhyDrv': '1.3.6.1.4.1.232.3.2.5',
    'cpqDaPhyDrvThr': '1.3.6.1.4.1.232.3.2.6',
    'cpqDaSpareDrv': '1.3.6.1.4.1.232.3.2.4',
    'cpqDaTapeCounters': '1.3.6.1.4.1.232.3.2.10',
    'cpqDaTapeDrv': '1.3.6.1.4.1.232.3.2.9',
    'cpqDaTapeLibrary': '1.3.6.1.4.1.232.3.2.11',
    'cpqDaTrap': '1.3.6.1.4.1.232.3.3',
    'cpqDriveArray': '1.3.6.1.4.1.232.3',
    'cpqExtArrRsrcVol': '1.3.6.1.4.1.232.16.2.8',
    'cpqExtArrSnapshot': '1.3.6.1.4.1.232.16.2.9',
    'cpqFcaCntlr': '1.3.6.1.4.1.232.16.2.2',
    'cpqFcaComponent': '1.3.6.1.4.1.232.16.2',
    'cpqFcaHostCntlr': '1.3.6.1.4.1.232.16.2.7',
    'cpqFcaInterface': '1.3.6.1.4.1.232.16.2.1',
    'cpqFcaLogDrv': '1.3.6.1.4.1.232.16.2.3',
    'cpqFcaMibRev': '1.3.6.1.4.1.232.16.1',
    'cpqFcaOsCommon': '1.3.6.1.4.1.232.16.2.1.4',
    'cpqFcaPhyDrv': '1.3.6.1.4.1.232.16.2.5',
    'cpqFcaPhyDrvThr': '1.3.6.1.4.1.232.16.2.6',
    'cpqFcaSpareDrv': '1.3.6.1.4.1.232.16.2.4',
    'cpqFcSwitch': '1.3.6.1.4.1.232.16.4.1',
    'cpqFcSwitchComponent': '1.3.6.1.4.1.232.16.4',
    'cpqFcTapeCntlr': '1.3.6.1.4.1.232.16.3.1',
    'cpqFcTapeComponent': '1.3.6.1.4.1.232.16.3',
    'cpqFcTapeCounters': '1.3.6.1.4.1.232.16.3.4',
    'cpqFcTapeDrive': '1.3.6.1.4.1.232.16.3.3',
    'cpqFcTapeLibrary': '1.3.6.1.4.1.232.16.3.2',
    'cpqFibreArray': '1.3.6.1.4.1.232.16',
    'cpqHealth': '1.3.6.1.4.1.232.6',
    'cpqHeAsr': '1.3.6.1.4.1.232.6.2.5',
    'cpqHeComponent': '1.3.6.1.4.1.232.6.2',
    'cpqHeCorrectableMemory': '1.3.6.1.4.1.232.6.2.3',
    'cpqHeCriticalError': '1.3.6.1.4.1.232.6.2.2',
    'cpqHeEventLog': '1.3.6.1.4.1.232.6.2.11',
    'cpqHeFltTolPwrSupply': '1.3.6.1.4.1.232.6.2.9',
    'cpqHeInterface': '1.3.6.1.4.1.232.6.2.1',
    'cpqHeIRC': '1.3.6.1.4.1.232.6.2.10',
    'cpqHeMgmtDisplay': '1.3.6.1.4.1.232.6.2.12',
    'cpqHeMibRev': '1.3.6.1.4.1.232.6.1',
    'cpqHeOsCommon': '1.3.6.1.4.1.232.6.2.1.4',
    'cpqHeOsNetWare3x': '1.3.6.1.4.1.232.6.2.1.1',
    'cpqHePostMsg': '1.3.6.1.4.1.232.6.2.7',
    'cpqHePowerConverter': '1.3.6.1.4.1.232.6.2.13',
    'cpqHePowerMeter': '1.3.6.1.4.1.232.6.2.15',
    'cpqHeResilientMemory': '1.3.6.1.4.1.232.6.2.14',
    'cpqHeSysUtil': '1.3.6.1.4.1.232.6.2.8',
    'cpqHeThermal': '1.3.6.1.4.1.232.6.2.6',
    'cpqHeTrap': '1.3.6.1.4.1.232.6.3',
    'cpqHoClients': '1.3.6.1.4.1.232.11.2.12',
    'cpqHoComponent': '1.3.6.1.4.1.232.11.2',
    'cpqHoFileSys': '1.3.6.1.4.1.232.11.2.4',
    'cpqHoFwVer': '1.3.6.1.4.1.232.11.2.14',
    'cpqHoGeneric': '1.3.6.1.4.1.232.11.2.8',
    'cpqHoHWInfo': '1.3.6.1.4.1.232.11.2.15',
    'cpqHoIfPhysMap': '1.3.6.1.4.1.232.11.2.5',
    'cpqHoInfo': '1.3.6.1.4.1.232.11.2.2',
    'cpqHoInterface': '1.3.6.1.4.1.232.11.2.1',
    'cpqHoMemory': '1.3.6.1.4.1.232.11.2.13',
    'cpqHoMibRev': '1.3.6.1.4.1.232.11.1',
    'cpqHoOsCommon': '1.3.6.1.4.1.232.11.2.1.4',
    'cpqHostOs': '1.3.6.1.4.1.232.11',
    'cpqHoSwPerf': '1.3.6.1.4.1.232.11.2.9',
    'cpqHoSWRunning': '1.3.6.1.4.1.232.11.2.6',
    'cpqHoSwVer': '1.3.6.1.4.1.232.11.2.7',
    'cpqHoSystemStatus': '1.3.6.1.4.1.232.11.2.10',
    'cpqHoTrapInfo': '1.3.6.1.4.1.232.11.2.11',
    'cpqHoUtil': '1.3.6.1.4.1.232.11.2.3',
    'cpqIde': '1.3.6.1.4.1.232.14',
    'cpqIdeAtaDisk': '1.3.6.1.4.1.232.14.2.4',
    'cpqIdeAtapiDevice': '1.3.6.1.4.1.232.14.2.5',
    'cpqIdeComponent': '1.3.6.1.4.1.232.14.2',
    'cpqIdeController': '1.3.6.1.4.1.232.14.2.3',
    'cpqIdeIdent': '1.3.6.1.4.1.232.14.2.2',
    'cpqIdeInterface': '1.3.6.1.4.1.232.14.2.1',
    'cpqIdeLogicalDrive': '1.3.6.1.4.1.232.14.2.6',
    'cpqIdeMibRev': '1.3.6.1.4.1.232.14.1',
    'cpqIdeOsCommon': '1.3.6.1.4.1.232.14.2.1.4',
    'cpqNic': '1.3.6.1.4.1.232.18',
    'cpqNicComponent': '1.3.6.1.4.1.232.18.2',
    'cpqNicIfLogMap': '1.3.6.1.4.1.232.18.2.2',
    'cpqNicIfPhysAdapter': '1.3.6.1.4.1.232.18.2.3',
    'cpqNicIfVlanMap': '1.3.6.1.4.1.232.18.2.4',
    'cpqNicInterface': '1.3.6.1.4.1.232.18.2.1',
    'cpqNicMibRev': '1.3.6.1.4.1.232.18.1',
    'cpqNicOsCommon': '1.3.6.1.4.1.232.18.2.1.4',
    'cpqNicVirusThrottle': '1.3.6.1.4.1.232.18.2.5',
    'cpqOsCache': '1.3.6.1.4.1.232.19.2.5',
    'cpqOsCommon': '1.3.6.1.4.1.232.19.2.1.4',
    'cpqOsComponent': '1.3.6.1.4.1.232.19.2',
    'cpqOsInterface': '1.3.6.1.4.1.232.19.2.1',
    'cpqOsLogicalDisk': '1.3.6.1.4.1.232.19.2.8',
    'cpqOsMemory': '1.3.6.1.4.1.232.19.2.4',
    'cpqOsMibRev': '1.3.6.1.4.1.232.19.1',
    'cpqOsNetworkInterface': '1.3.6.1.4.1.232.19.2.10',
    'cpqOsPagingFile': '1.3.6.1.4.1.232.19.2.6',
    'cpqOsPhysicalDisk': '1.3.6.1.4.1.232.19.2.7',
    'cpqOsProcess': '1.3.6.1.4.1.232.19.2.12',
    'cpqOsProcessor': '1.3.6.1.4.1.232.19.2.3',
    'cpqOsServer': '1.3.6.1.4.1.232.19.2.9',
    'cpqOsSystem': '1.3.6.1.4.1.232.19.2.2',
    'cpqOsTcp': '1.3.6.1.4.1.232.19.2.11',
    'cpqPwrThreshold': '1.3.6.1.4.1.232.11.2.16',
    'cpqRecovery': '1.3.6.1.4.1.232.13',
    'cpqSasComponent': '1.3.6.1.4.1.232.5.5',
    'cpqSasHba': '1.3.6.1.4.1.232.5.5.1',
    'cpqSasLogDrv': '1.3.6.1.4.1.232.5.5.3',
    'cpqSasPhyDrv': '1.3.6.1.4.1.232.5.5.2',
    'cpqSasTapeDrv': '1.3.6.1.4.1.232.5.5.4',
    'cpqSbDevice': '1.3.6.1.4.1.232.7.2',
    'cpqSbScsiBus': '1.3.6.1.4.1.232.7',
    'cpqSbScsiMibRev': '1.3.6.1.4.1.232.7.1',
    'cpqScsi': '1.3.6.1.4.1.232.5',
    'cpqScsiCd': '1.3.6.1.4.1.232.5.2.6',
    'cpqScsiCntlr': '1.3.6.1.4.1.232.5.2.2',
    'cpqScsiComponent': '1.3.6.1.4.1.232.5.2',
    'cpqScsiInterface': '1.3.6.1.4.1.232.5.2.1',
    'cpqScsiLogDrv': '1.3.6.1.4.1.232.5.2.3',
    'cpqScsiMibRev': '1.3.6.1.4.1.232.5.1',
    'cpqScsiOsCommon': '1.3.6.1.4.1.232.5.2.1.4',
    'cpqScsiOsNetWare': '1.3.6.1.4.1.232.5.2.1.1',
    'cpqScsiPhyDrv': '1.3.6.1.4.1.232.5.2.4',
    'cpqScsiTarget': '1.3.6.1.4.1.232.5.2.5',
    'cpqScsiTrap': '1.3.6.1.4.1.232.5.3',
    'cpqSeCabinet': '1.3.6.1.4.1.232.1.2.19',
    'cpqSeCell': '1.3.6.1.4.1.232.1.2.16',
    'cpqSeComplex': '1.3.6.1.4.1.232.1.2.20',
    'cpqSeComponent': '1.3.6.1.4.1.232.1.2',
    'cpqSeEisaNvram': '1.3.6.1.4.1.232.1.2.5',
    'cpqSeFixedDisk': '1.3.6.1.4.1.232.1.2.12',
    'cpqSeFloppyDisk': '1.3.6.1.4.1.232.1.2.11',
    'cpqSeInterface': '1.3.6.1.4.1.232.1.2.1',
    'cpqSeIOC': '1.3.6.1.4.1.232.1.2.17',
    'cpqSeIsaCmos': '1.3.6.1.4.1.232.1.2.4',
    'cpqSeKeyboard': '1.3.6.1.4.1.232.1.2.7',
    'cpqSeLED': '1.3.6.1.4.1.232.1.2.21',
    'cpqSeMemory': '1.3.6.1.4.1.232.1.2.3',
    'cpqSeMibRev': '1.3.6.1.4.1.232.1.1',
    'cpqSeOsCommon': '1.3.6.1.4.1.232.1.2.1.4',
    'cpqSeParallelPort': '1.3.6.1.4.1.232.1.2.10',
    'cpqSePartition': '1.3.6.1.4.1.232.1.2.18',
    'cpqSePCCard': '1.3.6.1.4.1.232.1.2.14',
    'cpqSePci': '1.3.6.1.4.1.232.1.2.13',
    'cpqSeProcessor': '1.3.6.1.4.1.232.1.2.2',
    'cpqSeRom': '1.3.6.1.4.1.232.1.2.6',
    'cpqServerManager': '1.3.6.1.4.1.232.4',
    'cpqService': '1.3.6.1.4.1.232.164',
    'cpqServiceIncident': '1.3.6.1.4.1.232.164.2',
    'cpqServiceMibRev': '1.3.6.1.4.1.232.164.1',
    'cpqSeSerialPort': '1.3.6.1.4.1.232.1.2.9',
    'cpqSeUSBDevice': '1.3.6.1.4.1.232.1.2.22',
    'cpqSeUSBPort': '1.3.6.1.4.1.232.1.2.15',
    'cpqSeVideo': '1.3.6.1.4.1.232.1.2.8',
    'cpqSiAsset': '1.3.6.1.4.1.232.2.2.2',
    'cpqSiBoardRev': '1.3.6.1.4.1.232.2.2.5',
    'cpqSiComponent': '1.3.6.1.4.1.232.2.2',
    'cpqSiDockingStation': '1.3.6.1.4.1.232.2.2.11',
    'cpqSiFru': '1.3.6.1.4.1.232.2.2.12',
    'cpqSiHotPlugSlot': '1.3.6.1.4.1.232.2.2.9',
    'cpqSiInterface': '1.3.6.1.4.1.232.2.2.1',
    'cpqSiMibRev': '1.3.6.1.4.1.232.2.1',
    'cpqSiMonitor': '1.3.6.1.4.1.232.2.2.8',
    'cpqSiMP': '1.3.6.1.4.1.232.2.2.16',
    'cpqSiOsCommon': '1.3.6.1.4.1.232.2.2.1.4',
    'cpqSiRack': '1.3.6.1.4.1.232.2.2.15',
    'cpqSiRackEnclosure': '1.3.6.1.4.1.232.2.2.13',
    'cpqSiRackServer': '1.3.6.1.4.1.232.2.2.6',
    'cpqSiSecurity': '1.3.6.1.4.1.232.2.2.3',
    'cpqSiServerBlade': '1.3.6.1.4.1.232.2.2.14',
    'cpqSiSystemBattery': '1.3.6.1.4.1.232.2.2.10',
    'cpqSiSystemBoard': '1.3.6.1.4.1.232.2.2.4',
    'cpqSiVideo': '1.3.6.1.4.1.232.2.2.7',
    'cpqSmAlert': '1.3.6.1.4.1.232.4.2.5',
    'cpqSmAsyncComm': '1.3.6.1.4.1.232.4.2.4',
    'cpqSmCntlr': '1.3.6.1.4.1.232.4.2.2',
    'cpqSmComponent': '1.3.6.1.4.1.232.4.2',
    'cpqSmInterface': '1.3.6.1.4.1.232.4.2.1',
    'cpqSmMibRev': '1.3.6.1.4.1.232.4.1',
    'cpqSmObjData': '1.3.6.1.4.1.232.4.2.3',
    'cpqSmOsNetWare3x': '1.3.6.1.4.1.232.4.2.1.1',
    'cpqSmTrap': '1.3.6.1.4.1.232.4.3',
    'cpqSsBoxExtended': '1.3.6.1.4.1.232.8.2.2',
    'cpqSsDrvBox': '1.3.6.1.4.1.232.8.2',
    'cpqSsMibRev': '1.3.6.1.4.1.232.8.1',
    'cpqSsRaidSystem': '1.3.6.1.4.1.232.8.4',
    'cpqSsStorageSys': '1.3.6.1.4.1.232.8',
    'cpqSsTrap': '1.3.6.1.4.1.232.8.3',
    'cpqStdEquipment': '1.3.6.1.4.1.232.1',
    'cpqSystemInfo': '1.3.6.1.4.1.232.2',
    'cpqTapeComponent': '1.3.6.1.4.1.232.5.4',
    'cpqTapeCounters': '1.3.6.1.4.1.232.5.4.2',
    'cpqTapeLibrary': '1.3.6.1.4.1.232.5.4.3',
    'cpqTapePhyDrv': '1.3.6.1.4.1.232.5.4.1',
    'cpqUps': '1.3.6.1.4.1.232.12',
    'cpqUpsBasic': '1.3.6.1.4.1.232.12.2.2',
    'cpqUpsComponent': '1.3.6.1.4.1.232.12.2',
    'cpqUpsFamily': '1.3.6.1.4.1.232.12.2.3',
    'cpqUpsInterface': '1.3.6.1.4.1.232.12.2.1',
    'cpqUpsMibRev': '1.3.6.1.4.1.232.12.1',
    'cpqUpsOsCommon': '1.3.6.1.4.1.232.12.2.1.4',
    'cpqWcrm': '1.3.6.1.4.1.232.167',
    'cpqWcrmControl': '1.3.6.1.4.1.232.167.5',
    'cpqWcrmMibRev': '1.3.6.1.4.1.232.167.1',
    'cpqWcrmSetup': '1.3.6.1.4.1.232.167.3',
    'cpqWcrmSetupGeneral': '1.3.6.1.4.1.232.167.3.1',
    'cpqWcrmStatus': '1.3.6.1.4.1.232.167.2',
    'cpqWcrmStatusInternalMsg': '1.3.6.1.4.1.232.167.2.3.7',
    'cpqWcrmStatusInternalOutputs': '1.3.6.1.4.1.232.167.2.3.6',
    'cpqWcrmStatusInternalSensors': '1.3.6.1.4.1.232.167.2.3.5',
    'cpqWcrmStatusSensorInternal': '1.3.6.1.4.1.232.167.2.3',
    'cpqWcrmStatusSensorWaterCoolUnit': '1.3.6.1.4.1.232.167.2.4',
    'cpqWcrmStatusWaterCoolUnitMsg': '1.3.6.1.4.1.232.167.2.4.7',
    'cpqWcrmStatusWaterCoolUnitOutputs': '1.3.6.1.4.1.232.167.2.4.6',
    'cpqWcrmStatusWaterCoolUnitSensors': '1.3.6.1.4.1.232.167.2.4.5',
    'cpqWcrmTimerTable1': '1.3.6.1.4.1.232.167.3.1.8',
    'cpqWcrmTrapControl': '1.3.6.1.4.1.232.167.4',
    'cpqWcrmTraps': '1.3.6.1.4.1.232.167.4.7',
    'cpqWinOsMgmt': '1.3.6.1.4.1.232.19',
    'dot1dBase': '1.3.6.1.2.1.17.1',
    'dot1dBridge': '1.3.6.1.2.1.17',
    'dot1dSr': '1.3.6.1.2.1.17.3',
    'dot1dStatic': '1.3.6.1.2.1.17.5',
    'dot1dStp': '1.3.6.1.2.1.17.2',
    'dot1dTp': '1.3.6.1.2.1.17.4',
    'ems': '1.3.6.1.4.1.169.3.12',
    'enterprises': '1.3.6.1.4.1',
    'hp': '1.3.6.1.4.1.11',
    'hpIpf02Events': '1.3.6.1.4.1.11.2.23.45',
    'hpIpfE0Events': '1.3.6.1.4.1.11.2.23.35',
    'hpnsa': '1.3.6.1.4.1.11.2.23',
    'hpOVNNMTraps': 'hpOpenView.0',
    'nm': '1.3.6.1.4.1.11.2',
    'nonstopsystems': '1.3.6.1.4.1.169.3',
    'openView': '1.3.6.1.4.1.11.2.17',
    'openViewTrapVars': '1.3.6.1.4.1.11.2.17.2',
    'scsi': '1.3.6.1.4.1.1123.3.1',
    'serverNet': '1.3.6.1.4.1.169.8',
    'serverNetSwitch': '1.3.6.1.4.1.169.8.3',
    'snetSwitchConfigData': '1.3.6.1.4.1.169.8.3.2.1',
    'snetSwitchErrorStatusData': '1.3.6.1.4.1.169.8.3.2.5',
    'snetSwitchInfo': '1.3.6.1.4.1.169.8.3.2',
    'snetSwitchNetworkData': '1.3.6.1.4.1.169.8.3.1',
    'snetSwitchPerformanceData': '1.3.6.1.4.1.169.8.3.2.4',
    'snetSwitchPortData': '1.3.6.1.4.1.169.8.3.2.2',
    'snetSwitchRoutingData': '1.3.6.1.4.1.169.8.3.2.3',
    'snetSwitchTrapEnables': '1.3.6.1.4.1.169.8.3.1.7',
    'snmp': '1.3.6.1.4.1.169.3.155',
    'snmpagent': '1.3.6.1.4.1.169.3.155.1',
    'symbios': '1.3.6.1.4.1.1123',
    'symc8xx': '1.3.6.1.4.1.1123.3.1.2',
    'symTrap': '1.3.6.1.4.1.1123.3.1.2.2',
    'tandem': '1.3.6.1.4.1.169',
    'zesa': '1.3.6.1.4.1.169.3.217',
    'zhrm': '1.3.6.1.4.1.169.3.180',
    'zhrmDevUnavail': '1.3.6.1.4.1.169.3.180.3',
    'zhrmInfCpuTable': '1.3.6.1.4.1.169.3.180.1.3',
    'zhrmInfDevTable': '1.3.6.1.4.1.169.3.180.1.2',
    'zhrmInfDiskTable': '1.3.6.1.4.1.169.3.180.1.6',
    'zhrmInfFSTable': '1.3.6.1.4.1.169.3.180.1.8',
    'zhrmInfNetTable': '1.3.6.1.4.1.169.3.180.1.4',
    'zhrmInfPartTable': '1.3.6.1.4.1.169.3.180.1.7',
    'zhrmInfPrnTable': '1.3.6.1.4.1.169.3.180.1.5',
    'zhrmInfStorTable': '1.3.6.1.4.1.169.3.180.1.1',
    'zhrmRefresh': '1.3.6.1.4.1.169.3.180.5',
    'zhrmSaProcess': '1.3.6.1.4.1.169.3.180.4',
    'zhrmTableInfo': '1.3.6.1.4.1.169.3.180.1',
    'zhrmThrDisk': '1.3.6.1.4.1.169.3.180.2.2',
    'zhrmThreshold': '1.3.6.1.4.1.169.3.180.2',
    'zhrmThrRAM': '1.3.6.1.4.1.169.3.180.2.1',
    'zhrmTraps': '1.3.6.1.4.1.169.3.180.7'
}

regex_string = re.compile('TRAP-TYPE$')
regex_string_ent = re.compile('ENTERPRISE')
regex_string_description = re.compile('DESCRIPTION')
regex_string_till_exp_str = re.compile('--#SEVERITY|--#TYPE|--#SUMMARY|::=')


def merge_dictionary():

    # Merging Dictionaries.
    merged_dictionary = sim_mib_dictionary.copy()
    merged_dictionary.update(iana_smi_name_to_numbers)
    merged_dictionary.update(ins_mibs_dictionary)
    return merged_dictionary

# making it public as this data uis static
merged_data = merge_dictionary()


def check_comment_trap(line_to_process):

    # Skipping lines.
    if line_to_process.strip()[:2] == '--' or line_to_process.strip()[:9] == 'TRAP-TYPE' \
            or line_to_process.strip() == '':
        return True
    else:
        return False


def get_oid_from_name(enterprise_name):

    # Searching for OIDs.
    if enterprise_name in merged_data:
        return merged_data[enterprise_name]
    else:
        return enterprise_name


def parsing_trap(path_to_files):

    # Setting check list.
    continue_check = True
    found_trap = False
    file_trap_list = []

    # Processing File.
    file_to_read_desc = open(path_to_files)

    # Processing.
    for line in file_to_read_desc:

        if check_comment_trap(line):
            # Ignoring comments and other lines.
            continue

        if regex_string.search(line) and continue_check == True:
            file_dictionary = {}
            file_dictionary['filename'] = str(path_to_files).split('/')[-1:][0]
            new_line_generated = line.strip().replace('TRAP-TYPE', '').strip()
            file_dictionary['trap_name'] = new_line_generated
            found_trap = True

        elif regex_string_ent.search(line) and continue_check and found_trap:
            oid_smi_name = line.replace('ENTERPRISE', '').strip()
            file_dictionary['trap_oid_enterprise_name'] = oid_smi_name

        elif regex_string_description.search(line) and continue_check and found_trap:
            desc_line_to_process = line.strip().replace('DESCRIPTION', '').strip()
            updated_desc_line = re.sub("[,-=+\"]", "", desc_line_to_process)
            file_dictionary['description'] = updated_desc_line
            continue_check = False

        elif not regex_string_till_exp_str.search(line) and continue_check == False and found_trap:
            if 'description' in file_dictionary:
                file_dictionary['description'] = re.sub("[,-=+\"]", '', file_dictionary['description']).strip() + ' ' + \
                                                 re.sub("[,-=+\"]", '', line.strip()).strip()
            else:
                file_dictionary['description'] = re.sub("[,-=+\"]", '', line.strip()).strip()

        if regex_string_till_exp_str.search(line.strip()) and continue_check == False and found_trap:
            if line.strip()[:3] == '::=':
                oid = line.strip().replace('::=', '').strip()
                if '--' in oid:
                    file_dictionary['singlet_oid'] = oid.strip(' ').split('--')[0].strip()
                else:
                    file_dictionary['singlet_oid'] = oid

            file_dictionary['oid'] = get_oid_from_name(file_dictionary['trap_oid_enterprise_name']).strip() + '.0.' \
                                     + file_dictionary['singlet_oid']

            file_dictionary['comment'] = ''
            file_dictionary['priority'] = 'Average'
            file_dictionary['dependency'] = 'NONE'
            file_dictionary['clear_time_in_days'] = '3d'

            description_len_limit = 85

            if len(file_dictionary['description']) < description_len_limit:
                file_dictionary['trigger_name_description'] = file_dictionary['description'] + '.'
            else:
                file_dictionary['trigger_name_description'] = file_dictionary['description'][:description_len_limit] +\
                                                              '...'

            continue_check = True
            found_trap = False

            # Debugging.
            #logging.DEBUG(str(file_dictionary))

            file_trap_list.append(file_dictionary)
    return file_trap_list


def remove_file(file_remove):
    try:
        os.remove(file_remove)
    except OSError:
        pass


def get_files_from_directory(path_to_files):
    try:
        list_of_files = os.listdir(path_to_files)
        return list_of_files

    except exception:
        print("Something went wrong in directory parsing" + str(exception))
        exit()


def file_processing(path_to_files):

    # Generating list from directory.
    file_list = get_files_from_directory(path_to_files)
    mib_trap_data_list = []

    for item in file_list:

        # Debug information
        #logging.DEBUG("Processing File : " + str(item))

        # Processing File.
        file_trap_list = parsing_trap(path_to_files + item)
        mib_trap_data_list = mib_trap_data_list + file_trap_list

    return mib_trap_data_list


def mib_file_obj_ident_dictionary(path_to_files):
    list_of_files = os.listdir(path_to_files)

    regex_string = re.compile('OBJECT IDENTIFIER ::=')
    store_dictionary = {}

    for file in list_of_files:
        file_to_read_desc = open(path_to_files + file)
        for line in file_to_read_desc:
            # Skipping Commented line.
            if line.strip()[:2] == '--':
                #logging.DEBUG("SKIPPING LINE : " + line)
                continue
            if regex_string.search(line):
                object_key_line = line.strip().replace('OBJECT IDENTIFIER ::=', '').replace('{', ":").replace('}', "")
                update_key_value = object_key_line.split(':')
                store_dictionary[update_key_value[0].strip()] = \
                    update_key_value[1].split('--')[0].strip().replace(' ', '.')

                #logging.INFO(store_dictionary)

        file_to_read_desc.close()
    return store_dictionary


def creating_file(file_name, trap_list):

    csv_file_generator = open(file_name, "wb")
    csv_file_generator.write(
        "MIB-MODULE,MIB File,OID,Name,Recommended Action,Comments,Description,"
        "Trigger Description,Dependency,cleartime In Days")

    for row_data in trap_list:
        csv_file_generator.write('\n')
        csv_file_generator.write(
            row_data['filename'] + ',' + row_data['trap_oid_enterprise_name'] + ',.' + row_data['oid'] \
                        + ',' + row_data['trap_name'] + ',' + row_data['priority'] + ',' + row_data['comment']
                        + ',' + row_data['description'] + ',' + row_data['trigger_name_description']
                        + ',' + row_data['dependency'] + ',' + row_data['clear_time_in_days'])

    csv_file_generator.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=
                                     ''' ''')

    parser.add_argument('-c', '--csv-file-name', help='CSV File name to be generated', required=True)
    parser.add_argument('-p', '--path-to-mibs', help='Path to MIB files. Example: /file/path/to/mibs/', required=True)
    args = parser.parse_args()

    csv_file_name = args.csv_file_name
    path_to_mibs = args.path_to_mibs

    if path_to_mibs[-1:] != '/':
        path_to_mibs = path_to_mibs + '/'

    creating_file(csv_file_name, file_processing(path_to_mibs))

