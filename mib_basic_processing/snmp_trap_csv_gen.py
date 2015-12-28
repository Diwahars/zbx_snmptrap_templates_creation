import mib_trap_processing_snmpv1

file_processing_list = [{'file_path': 'mib_data/hp_sim_nsc_nsk/',
                         'csv_name': 'output/output_csv_hp_sim.csv'},
                        {'file_path': 'mib_data/ilo/',
                         'csv_name': 'output/output_csv_hp_ilo.csv'},
                        {'file_path': 'mib_data/ins/',
                         'csv_name': 'output/output_csv_ins.csv'},
                        {'file_path': 'mib_data/nonstopmibs/',
                         'csv_name': 'output/output_csv_nonstopmibs.csv'}]

for file_to_process in file_processing_list:
    print file_to_process
    mib_trap_processing_snmpv1.creating_file(file_to_process['csv_name'],
        mib_trap_processing_snmpv1.file_processing(file_to_process['file_path']))

