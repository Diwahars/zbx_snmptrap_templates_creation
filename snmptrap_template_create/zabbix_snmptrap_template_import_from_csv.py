#!/usr/bin/python

__author__ = 'ahmed'

import csv
import sys
from logging import exception
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
import datetime
import logging
from xml.dom import minidom
import argparse
import codecs


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

alarm_list = []

def get_smi_number_to_name(oid_string):
    # create a list and remove the empty value as we have `.`
    # in the beginning of the string.
    if oid_string[0] == '.':
        oid_list = oid_string.split('.')[1:]
    else:
        oid_list = oid_string.split('.')
    # temporary holding area.
    previous_oid_substring = ''

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


# --------------------------------------------------------
# Generate Complete Export/Import XML Template File
# --------------------------------------------------------
def generate_template_items_xml(alarm_list, template_name, template_group_name):
    zabbix_export = Element('zabbix_export')
    version = SubElement(zabbix_export, 'version')
    version.text = '2.0'

    fmt = '%Y-%m-%dT%H:%M:%SZ'
    date = SubElement(zabbix_export, 'date')
    date.text = datetime.datetime.now().strftime(fmt)

    groups = SubElement(zabbix_export, 'groups')
    group_under_groups = SubElement(groups, 'group')
    name_under_group = SubElement(group_under_groups, 'name')
    name_under_group.text = template_group_name

    templates = SubElement(zabbix_export, 'templates')
    template_under_templates = SubElement(templates, 'template')
    template_under_template = SubElement(template_under_templates, 'template')
    template_under_template.text = template_name

    name_under_template = SubElement(template_under_templates, 'name')
    name_under_template.text = template_name

    groups_under_templates = SubElement(template_under_templates, 'groups')
    group_under_groups_template = SubElement(groups_under_templates, 'group')
    name_group_under_groups_template = SubElement(group_under_groups_template, 'name')
    name_group_under_groups_template.text = template_group_name

    application_template_under_templates = SubElement(template_under_templates, 'applications')
    application_app_under_templates = SubElement(application_template_under_templates, 'application')
    application_app_name = SubElement(application_app_under_templates, 'name')
    application_app_name.text = 'Alarms'

    items = SubElement(template_under_templates, 'items')
    triggers = SubElement(zabbix_export, 'triggers')
    SubElement(zabbix_export, 'graphs')

    #Iterate through the unique list to create XML
    for alarm_values in alarm_list:
       item_creator_type_oid(items, template_name, triggers, alarm_values)

    for alarm_values in alarm_list:
        item_creator_type_trap_name(items, template_name, triggers, alarm_values)

    SubElement(template_under_templates, 'discovery_rules')
    SubElement(template_under_templates, 'macros')
    SubElement(template_under_templates, 'templates')
    SubElement(template_under_templates, 'screens')

    return zabbix_export


def get_trap_name_from_oid(oid_to_search):
    for alarm_dict in alarm_list:
        if oid_to_search == alarm_dict['oid']:
            return alarm_dict['name']

    return oid_to_search

def item_creator_type_oid(items, template_name, triggers, alarm_values):
    item = SubElement(items, 'item')
    name = SubElement(item, 'name')
    type = SubElement(item, 'type')
    SubElement(item, 'snmp_community')
    multiplier = SubElement(item, 'multiplier')
    SubElement(item, 'snmp_oid')
    key = SubElement(item, 'key')
    delay = SubElement(item, 'delay')
    history = SubElement(item, 'history')
    trends = SubElement(item, 'trends')
    status = SubElement(item, 'status')
    value_type = SubElement(item, 'value_type')
    SubElement(item, 'allowed_hosts')
    SubElement(item, 'units')
    delta = SubElement(item, 'delta')
    SubElement(item, 'snmpv3_contextname')
    SubElement(item, 'snmpv3_securityname')
    snmpv3_securitylevel = SubElement(item, 'snmpv3_securitylevel')
    snmpv3_authprotocol = SubElement(item, 'snmpv3_authprotocol')
    SubElement(item, 'snmpv3_authpassphrase')
    snmpv3_privprotocol = SubElement(item, 'snmpv3_privprotocol')
    SubElement(item, 'snmpv3_privpassphrase')
    formula = SubElement(item, 'formula')
    SubElement(item, 'delay_flex')
    SubElement(item, 'params')
    SubElement(item, 'ipmi_sensor')
    data_type = SubElement(item, 'data_type')
    authtype = SubElement(item, 'authtype')
    SubElement(item, 'username')
    SubElement(item, 'password')
    SubElement(item, 'publickey')
    SubElement(item, 'privatekey')
    SubElement(item, 'port')
    description = SubElement(item, 'description')
    inventory_link = SubElement(item, 'inventory_link')
    SubElement(item, 'valuemap')
    applications = SubElement(item, 'applications')
    application = SubElement(applications, 'application')
    application_name = SubElement(application, 'name')
    SubElement(item, 'valuemap')
    logtimefmt = SubElement(item, 'logtimefmt')



    #
    # Setting basic information for the item.
    #
    name.text = 'Alarm Notification For : ' + alarm_values['name']
    type.text = '17'
    multiplier.text = '0'
    key.text = 'snmptrap["(\\b' + alarm_values['oid'] + '$\\b)"]'
    delay.text = '0'
    history.text = '90'
    trends.text = '365'
    status.text = '0'
    value_type.text = '2'
    delta.text = '0'
    snmpv3_securitylevel.text = '0'
    snmpv3_authprotocol.text = '0'
    snmpv3_privprotocol.text = '0'
    formula.text = '1'
    data_type.text = '0'
    authtype.text = '0'
    inventory_link.text = '0'
    description.text = str(alarm_values['description'])

    application_name.text = 'Alarms'
    logtimefmt.text = 'hh:mm:ss yyyy/MM/dd'

    trigger = SubElement(triggers, 'trigger')
    trigger_expression = SubElement(trigger, 'expression')
    trigger_name = SubElement(trigger, 'name')
    SubElement(trigger, 'url')
    trigger_status = SubElement(trigger, 'status')
    trigger_priority = SubElement(trigger, 'priority')
    trigger_description = SubElement(trigger, 'description')
    trigger_type = SubElement(trigger, 'type')
    SubElement(trigger, 'dependencies')

    if (alarm_values['dependency'] == 'NONE' or alarm_values['dependency'] == '') and \
                    alarm_values['priority'] == 'Clear':
        trigger_expression.text = '{' + template_name + ':' + key.text + '.str("' + alarm_values['oid'] + '")}=1 & {' \
                                  + template_name + ':' + key.text + '.nodata(1d)}=0'

    if (alarm_values['dependency'] == 'NONE' or alarm_values['dependency'] == '') and \
                    alarm_values['priority'] != 'Clear':
        trigger_expression.text = '{' + template_name + ':' + key.text + '.str("' + alarm_values['oid'] + '")}=1 & {' \
                                  + template_name + ':' + key.text + '.nodata(' + alarm_values[
                                      'clear_time_in_days'] + ')}=0'

    elif alarm_values['dependency'] != 'NONE':
        trigger_expression.text = '{' + template_name + ':' + key.text + '.str("' + alarm_values['oid'] + '")}=1 & {' \
                                  + template_name + ':' + key.text + '.nodata(' + alarm_values['clear_time_in_days'] \
                                  + ')}=0 & {' \
                                  + template_name + ':' + 'snmptrap["(\\b' + alarm_values['dependency'] + '$\\b)"]' + \
                                  '.str("' + alarm_values['dependency'] + '")}=0'


    if alarm_values['trigger_name_description'] == '':
        trigger_name.text = 'ATTENTION : On {HOST.NAME}, An Alarm : ' + alarm_values['name'] + \
                        ' - {#SNMPVALUE}, From Module : ' + alarm_values['mib_module']
    else:
        #print alarm_values['trigger_name_description'].replace("\n", " ")
        #print "---"
        updated_name = alarm_values['trigger_name_description'].replace("\n", " ")
        trigger_name.text = updated_name

    trigger_status.text = '0'

    if alarm_values['priority'] == 'Discard':
        trigger_priority.text = '0'
    elif alarm_values['priority'] in ['Threshold', 'Clear', 'Log', 'Information']:
        trigger_priority.text = '1'
    elif alarm_values['priority'] == 'Minor':
        trigger_priority.text = '2'
    elif alarm_values['priority'] == 'Average':
        trigger_priority.text = '3'
    elif alarm_values['priority'] == 'Major':
        trigger_priority.text = '4'
    elif alarm_values['priority'] == 'Critical':
        trigger_priority.text = '5'

    trigger_description.text = description.text
    trigger_type.text = '0'


def item_creator_type_trap_name(items, template_name, triggers, alarm_values):
    item = SubElement(items, 'item')
    name = SubElement(item, 'name')
    type = SubElement(item, 'type')
    SubElement(item, 'snmp_community')
    multiplier = SubElement(item, 'multiplier')
    SubElement(item, 'snmp_oid')
    key = SubElement(item, 'key')
    delay = SubElement(item, 'delay')
    history = SubElement(item, 'history')
    trends = SubElement(item, 'trends')
    status = SubElement(item, 'status')
    value_type = SubElement(item, 'value_type')
    SubElement(item, 'allowed_hosts')
    SubElement(item, 'units')
    delta = SubElement(item, 'delta')
    SubElement(item, 'snmpv3_contextname')
    SubElement(item, 'snmpv3_securityname')
    snmpv3_securitylevel = SubElement(item, 'snmpv3_securitylevel')
    snmpv3_authprotocol = SubElement(item, 'snmpv3_authprotocol')
    SubElement(item, 'snmpv3_authpassphrase')
    snmpv3_privprotocol = SubElement(item, 'snmpv3_privprotocol')
    SubElement(item, 'snmpv3_privpassphrase')
    formula = SubElement(item, 'formula')
    SubElement(item, 'delay_flex')
    SubElement(item, 'params')
    SubElement(item, 'ipmi_sensor')
    data_type = SubElement(item, 'data_type')
    authtype = SubElement(item, 'authtype')
    SubElement(item, 'username')
    SubElement(item, 'password')
    SubElement(item, 'publickey')
    SubElement(item, 'privatekey')
    SubElement(item, 'port')
    description = SubElement(item, 'description')
    inventory_link = SubElement(item, 'inventory_link')
    SubElement(item, 'valuemap')
    applications = SubElement(item, 'applications')
    application = SubElement(applications, 'application')
    application_name = SubElement(application, 'name')
    SubElement(item, 'valuemap')
    logtimefmt = SubElement(item, 'logtimefmt')



    #
    # Setting basic information for the item.
    #
    name.text = 'Alarm Notification For : ' + alarm_values['name']
    type.text = '17'
    multiplier.text = '0'
    key.text = 'snmptrap["(' + alarm_values['name'] + '$)"]'
    delay.text = '0'
    history.text = '90'
    trends.text = '365'
    status.text = '0'
    value_type.text = '2'
    delta.text = '0'
    snmpv3_securitylevel.text = '0'
    snmpv3_authprotocol.text = '0'
    snmpv3_privprotocol.text = '0'
    formula.text = '1'
    data_type.text = '0'
    authtype.text = '0'
    inventory_link.text = '0'
    description.text = str(alarm_values['description'])

    application_name.text = 'Alarms'
    logtimefmt.text = 'hh:mm:ss yyyy/MM/dd'

    trigger = SubElement(triggers, 'trigger')
    trigger_expression = SubElement(trigger, 'expression')
    trigger_name = SubElement(trigger, 'name')
    SubElement(trigger, 'url')
    trigger_status = SubElement(trigger, 'status')
    trigger_priority = SubElement(trigger, 'priority')
    trigger_description = SubElement(trigger, 'description')
    trigger_type = SubElement(trigger, 'type')
    SubElement(trigger, 'dependencies')

    if (alarm_values['dependency'] == 'NONE' or alarm_values['dependency'] == '') and \
                    alarm_values['priority'] == 'Clear':
        trigger_expression.text = '{' + template_name + ':' + key.text + '.str("' + alarm_values['name'] + '")}=1 & {' \
                                  + template_name + ':' + key.text + '.nodata(1d)}=0'

    if (alarm_values['dependency'] == 'NONE' or alarm_values['dependency'] == '') and \
                    alarm_values['priority'] != 'Clear':
        trigger_expression.text = '{' + template_name + ':' + key.text + '.str("' + alarm_values['name'] + '")}=1 & {' \
                                  + template_name + ':' + key.text + '.nodata(' + alarm_values[
                                      'clear_time_in_days'] + ')}=0'

    elif alarm_values['dependency'] != 'NONE':
        dependency_trap_name = get_trap_name_from_oid(alarm_values['dependency'])
        trigger_expression.text = '{' + template_name + ':' + key.text + '.str("' + alarm_values['name'] + '")}=1 & {' \
                                  + template_name + ':' + key.text + '.nodata(' + alarm_values['clear_time_in_days'] \
                                  + ')}=0 & {' \
                                  + template_name + ':' + 'snmptrap["(' + dependency_trap_name + '$)"]' + \
                                  '.str("' + dependency_trap_name + '")}=0'


    if alarm_values['trigger_name_description'] == '':
        trigger_name.text = 'ATTENTION : On {HOST.NAME}, An Alarm : ' + alarm_values['name'] + \
                        ' - {#SNMPVALUE}, From Module : ' + alarm_values['mib_module']
    else:
        updated_name = alarm_values['trigger_name_description'].replace("\n", " ")
        trigger_name.text = updated_name

    trigger_status.text = '0'

    if alarm_values['priority'] == 'Discard':
        trigger_priority.text = '0'
    elif alarm_values['priority'] in ['Threshold', 'Clear', 'Log', 'Information']:
        trigger_priority.text = '1'
    elif alarm_values['priority'] == 'Minor':
        trigger_priority.text = '2'
    elif alarm_values['priority'] == 'Average':
        trigger_priority.text = '3'
    elif alarm_values['priority'] == 'Major':
        trigger_priority.text = '4'
    elif alarm_values['priority'] == 'Critical':
        trigger_priority.text = '5'

    trigger_description.text = description.text
    trigger_type.text = '0'


def xml_pretty_me(file_name_for_prettify, string_to_prettify):
    #
    # Open a file and write to it and we are done.
    #
    logging.debug("Creating File %s", file_name_for_prettify)

    xml = minidom.parseString(string_to_prettify)
    pretty_xml_as_string = xml.toprettyxml()
    output_file = open(file_name_for_prettify, 'w')
    output_file.write(pretty_xml_as_string)
    logging.debug("Creation Complete")
    output_file.close()


def read_from_csv(csv_file_name):
    try:
        reader = csv.reader(open(csv_file_name, 'r'))
        return reader
    except exception:
        print("Something went wrong in reading file" + str(exception))
        exit()


def zabbix_snmptrap_template_import(file_name, template_name, template_group_name):
    csv_reader = read_from_csv(file_name)
    for alarm_data in csv_reader:

        # Skipping First Line
        if alarm_data[0] == "MIB-MODULE":
            continue

        oid_dictionary = {'mib_module': alarm_data[0].strip(), 'mib_module_file': alarm_data[1].strip()}

        # Converting OID to Name based OID.
        oid_dictionary['oid'] = get_smi_number_to_name(alarm_data[2].strip())

        # Setting columns as it is from the File.
        oid_dictionary['name'] = alarm_data[3].strip()
        oid_dictionary['priority'] = alarm_data[4].strip()
        oid_dictionary['comment'] = alarm_data[5].strip()
        oid_dictionary['description'] = alarm_data[6].strip('"')
        oid_dictionary['trigger_name_description'] = alarm_data[7].strip()

        # Converting OID to Name based OID.
        # [Similar to the OID above as this is similar.]
        if alarm_data[8].strip() != '':
            oid_dictionary['dependency'] = str(get_smi_number_to_name(alarm_data[8].strip()))
        else:
            oid_dictionary['dependency'] = ''

        # Setting columns as it is from the file.
        oid_dictionary['clear_time_in_days'] = str(alarm_data[9].strip())
        logging.debug('oid_dictionary:' + str(oid_dictionary))

        # Creating list of dictionary to hold the data.
        alarm_list.append(oid_dictionary)


    # pass on the listed dictionary to xml processor, this will return a XML.
    xml_tree = generate_template_items_xml(alarm_list, template_name, template_group_name)

    # Cleaning list
    del alarm_list[:]

    # Converting XML object to String.
    xml_tree_as_string = ElementTree.tostring(xml_tree)

    # Return.
    return xml_tree_as_string


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=
                                     ''' ''')

    parser.add_argument('-e', '--export-csv', help='OID file, Gives all OIDs on the device', required=True)
    parser.add_argument('-n', '--template-name', help='Template name as given in Zabbix server.', required=True)
    parser.add_argument('-g', '--template-group',
                        help='Template Group which the Template belongs to, as in Zabbix server.',
                        required=True)

    parser.add_argument('-d', '--debug', help='Running Debug mode - More Verbose', action="store_true")
    parser.add_argument('-v', '--verbose', help='Running Debug mode - More Verbose', action="store_true")
    args = parser.parse_args()

    csv_file_name = args.export_csv
    zabbix_template_name = args.template_name
    zabbix_template_group_name = args.template_group

    if args.debug or args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # Processing CSV to XML.
    xml_tree_gen_as_string = zabbix_snmptrap_template_import(csv_file_name, zabbix_template_name,
                                                             zabbix_template_group_name)

    # Lets make the XML pretty.
    xml_pretty_me('templates/' + zabbix_template_name.lower().replace(' ', '-') + '-item-template-trigger-import.xml',
                  xml_tree_gen_as_string)
