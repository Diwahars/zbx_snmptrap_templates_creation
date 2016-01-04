import zabbix_snmptrap_template_import_from_csv

file_processing_list = [{'file_path': 'input_csv/checkpoint_node_traps.csv',
                         'template_name': 'Template SNMP Traps CHECKPOINT Nodes',
                         'template_group': 'Custom Template GT'},
                        {'file_path': 'input_csv/cisco_node_traps.csv',
                         'template_name': 'Template SNMP Traps CISCO Nodes',
                         'template_group': 'Custom Template GT'},
                        {'file_path': 'input_csv/hp_hh3c_node_traps.csv',
                         'template_name': 'Template SNMP Traps HP HH3C Nodes',
                         'template_group': 'Custom Template GT'},
                        {'file_path': 'input_csv/p4_poland_node_traps.csv',
                         'template_name': 'Template SNMP Traps P4 Nodes',
                         'template_group': 'Custom Template GT'},
                        {'file_path': 'input_csv/affirmed_node_traps.csv',
                         'template_name': 'Template SNMP Traps AFFIRMED Nodes',
                         'template_group': 'Custom Template GT'},
                        {'file_path': 'input_csv/compaq_ilo_node_traps.csv',
                         'template_name': 'Template SNMP Traps COMPAQ ILO',
                         'template_group': 'Custom Template GT'},
                        {'file_path': 'input_csv/hges_node_traps.csv',
                         'template_name': 'Template SNMP Traps HGES Nodes',
                         'template_group': 'Custom Template GT'},
                        {'file_path': 'input_csv/ins_mib_node_traps.csv',
                         'template_name': 'Template SNMP Traps INS MIB Nodes',
                         'template_group': 'Custom Template GT'},
                        {'file_path': 'input_csv/hp_sim_node_traps.csv',
                         'template_name': 'Template SNMP Traps HP SIM Nodes',
                         'template_group': 'Custom Template GT'},
                        {'file_path': 'input_csv/billing_application.csv',
                         'template_name': 'Template SNMP Traps BILLING App Nodes',
                         'template_group': 'Custom Template GT'},
                        {'file_path': 'input_csv/ams_bru_hkg_ggsn_updated.csv',
                         'template_name': 'Template SNMP Traps GGSN Nodes',
                         'template_group': 'Custom Template GT'}]

file_processing_list_ggsn = [{'file_path': 'input_csv/ams_bru_hkg_ggsn.csv',
                         'template_name': 'Template SNMP Traps GGSN Nodes',
                         'template_group': 'Custom Template GT'}]


for file_to_process in file_processing_list:
    print file_to_process
    xml_tree_gen_as_string = zabbix_snmptrap_template_import_from_csv.zabbix_snmptrap_template_import \
        (file_to_process['file_path'], file_to_process['template_name'],
         file_to_process['template_group'])
    zabbix_snmptrap_template_import_from_csv.xml_pretty_me \
        ('templates/' + file_to_process['template_name'].lower().replace(' ', '-') +
         '-item-template-trigger-import.xml', xml_tree_gen_as_string)