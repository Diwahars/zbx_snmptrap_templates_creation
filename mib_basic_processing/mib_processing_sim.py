import os
import re
from logging import exception

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
    'ztmxTrapStatistics': '1.3.6.1.4.1.169.3.185.1.9',
	'ntsp':'1.3.6.1.4.1.169.10 ',
	'ins':'1.3.6.1.4.1.169.10.1 ',
	'insErad':'1.3.6.1.4.1.169.10.1.1 ',
	'insStats':'1.3.6.1.4.1.169.10.1.2 ',
	'insNwConfig':'1.3.6.1.4.1.169.10.1.3 ',
	'insEradInfo':'1.3.6.1.4.1.169.10.1.1.10'
}

regex_string = re.compile('TRAP-TYPE$')
regex_string_ent = re.compile('ENTERPRISE')
regex_string_description = re.compile('DESCRIPTION')
regex_string_till_exp_str = re.compile('--#SEVERITY|--#TYPE|--#SUMMARY|::=')


def check_comment_trap(line_to_process):
    if line_to_process.strip()[:2] == '--' or line_to_process.strip()[:9] == 'TRAP-TYPE':
        return True
    else:
        return False


def parsing_trap(path_to_files):
    continue_check = True
    found_trap = False

    file_to_read_desc = open(path_to_files)
    for line in file_to_read_desc:
        if check_comment_trap(line):
            continue

        if regex_string.search(line) and continue_check:
            new_line_generated = line.strip().replace('TRAP-TYPE', ',').strip()
            print new_line_generated
            found_trap = True
        elif regex_string_ent.search(line) and continue_check and found_trap:
            oid_smi_name = line.replace('ENTERPRISE', '').strip()
            print oid_smi_name
        elif regex_string_description.search(line) and continue_check and found_trap:
            desc_line_to_process = line.strip().replace('DESCRIPTION', '')
            updated_desc_line = re.sub("[,-=+]", "", desc_line_to_process)
            print updated_desc_line
            continue_check = False
        elif not regex_string_till_exp_str.search(line) and not continue_check and found_trap:
            print line.strip()

        if regex_string_till_exp_str.search(line.strip()) and not continue_check and found_trap:
            if line.strip()[:3] == '::=':
                oid = line.strip().replace('::=', '').strip()
                print oid
            continue_check = True
            found_trap = False


def generate_iana_smi_oid():
    pass


def load_mib_file():
    pass


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


def generate_var_per_line():
    pass


def basic_mib_file_processing_hp(path_to_files, file_to_create):
    list_of_files = os.listdir(path_to_files)

    try:
        os.remove(file_to_create)
    except OSError:
        pass

    regex_string = re.compile('TRAP-TYPE$')
    regex_string_ent = re.compile('ENTERPRISE')
    regex_string_description = re.compile('DESCRIPTION')
    regex_string_till_exp_str = re.compile('--#SEVERITY|--#TYPE|--#SUMMARY|::=')

    continue_check = True
    found_trap = False

    file_passone = open(file_to_create + '_passone', "w")
    for file in list_of_files:
        file_to_read_desc = open(path_to_files + file)
        oid_converted_from_name = ''
        for line in file_to_read_desc:
            if line.strip()[:2] == '--' or line.strip()[:9] == 'TRAP-TYPE':
                # print "SKIPPED line --> " + str(line)
                continue

            if regex_string.search(line) and continue_check == True:
                print "WE GOT A LINE WHICH MATCH --> " + str(line)
                file_passone.write('\n' + line.strip() + '\n')
                found_trap = True
            elif regex_string_ent.search(line) and continue_check and found_trap:
                oid_smi_name = line.replace('ENTERPRISE', '').strip()
                print oid_smi_name
            elif regex_string_description.search(line) and continue_check and found_trap:
                file_passone.write(line.strip())
                continue_check = False
            elif not regex_string_till_exp_str.search(line) and continue_check == False and found_trap:
                file_passone.write(line.strip())

            if regex_string_till_exp_str.search(line.strip()) and continue_check == False and found_trap:
                if line.strip()[:3] == '::=':
                    oid = line.strip().replace('::=', '').strip()
                    print oid
                continue_check = True
                found_trap = False

        file_to_read_desc.close()
    file_passone.close()

    file_passtwo = open(file_to_create + '_passtwo.csv', "w")
    file_to_read_passone = open(file_to_create + '_passone', "r")
    for line in file_to_read_passone:
        if regex_string.search(line):
            newline_trap = line.replace('TRAP-TYPE', ',')
            file_passtwo.write(newline_trap.strip())
        elif regex_string_description.search(line):
            newline_desc = line.replace('DESCRIPTION', '')
            newline_desc_updated = re.sub("[,-=+]", "", newline_desc)
            file_passtwo.write(newline_desc_updated)
    file_passtwo.close()
    file_to_read_passone.close()


# print 'Merging MIBs'
# basic_mib_file_processing_compaq('mib_data/hp_compaq_traps_only_ilo_mibs/', 'merged_compaq_ilo_data.txt')

# print 'Merging MIBs'
# basic_mib_file_processing_hp('mib_data/hp_traps_only_mibs/', 'merged_hp_data.txt')

# print 'Merging MIBs'
# basic_mib_file_processing_hp('mib_data/hp_sim_nsc_nsk/', 'merged_sim_data.txt')


def mib_file_obj_ident_dictionary(path_to_files):
    list_of_files = os.listdir(path_to_files)

    regex_string = re.compile('OBJECT IDENTIFIER ::=')
    store_dictionary = {}

    for file in list_of_files:
        file_to_read_desc = open(path_to_files + file)
        for line in file_to_read_desc:
            # Skipping Commented line.
            if line.strip()[:2] == '--':
                continue
            if regex_string.search(line):
                object_key_line = line.strip().replace('OBJECT IDENTIFIER ::=', '').replace('{', ":").replace('}', "")
                update_key_value = object_key_line.split(':')
                store_dictionary[update_key_value[0].strip()] = \
                    update_key_value[1].split('--')[0].strip().replace(' ', '.')
        file_to_read_desc.close()
    return store_dictionary


key_value_pair = mib_file_obj_ident_dictionary('mib_data/nonstopmibs/')
print key_value_pair