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
    'features': '1.3.6.1.8'
}


def get_smi_number_to_name(oid_string):
    # create a list and remove the empty value as we have `.`
    # in the beginning of the string.
    if oid_string[0] == '.':
        oid_list = oid_string.split('.')[1:]
    else:
        oid_list = oid_string.split('.')
    # temporary holding area.
    previous_oid_substring = ''

    # debug
    print oid_list

    # Lets run through the OID string.
    for oid_item_from_list in oid_list:

        # for the first time we set as we it is.
        if previous_oid_substring == '':
            oid_item_from_list = oid_item_from_list
        else:
            oid_item_from_list = previous_oid_substring + '.' + oid_item_from_list

        # If we do not find the string the `iana_smi_numbers` dictionary then we return the previous item.
        if oid_item_from_list not in iana_smi_numbers:

            # If no values in `iana` then we return the original string.
            if previous_oid_substring == '':
                return oid_string
            else:
                # converting the old OIDs to New Name based OID and return.
                new_named_oid = oid_string.replace(previous_oid_substring, iana_smi_numbers[previous_oid_substring])[1:]
                return new_named_oid

        # Setting the value we found in the holding area,
        # if we dont find the next value then we use this to return.
        previous_oid_substring = oid_item_from_list


str = ['.1.3.6.1.4.1.25506.2.3.2.3', '.1.3.6.1.4.1.25506.6.8.1', '.1.3.6.1.4.1.25506.6.8.2',
       '.1.3.6.1.4.1.25506.6.8.3', '.1.3.6.1.4.1.25506.6.8.4', '.1.3.6.1.4.1.25506.6.8.5',
       '.1.3.6.1.4.1.25506.6.8.6', '.1.0.8802.1.1.2.0.0.1', '.1.0.8802.1.1.2.1.5.4795.0.1',
       '.1.3.6.1.2.1.14.16.2.1', '.1.3.6.1.2.1.14.16.2.2', '.1.3.6.1.2.1.14.16.2.3',
       '.1.3.6.1.2.1.14.16.2.4', '.1.3.6.1.2.1.14.16.2.5', '.1.3.6.1.2.1.14.16.2.6',
       'enterprises.2620.1.3000.5.4.1', 'enterprises.2620.1.3000.10.1.1',
       'enterprises.2620.1.3000.10.1.2', 'enterprises.2620.1.3000.2.1.1']

for oids in str:
    return_oid = get_smi_number_to_name(oids)
    print return_oid
