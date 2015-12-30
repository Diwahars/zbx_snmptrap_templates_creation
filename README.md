## Zabbix Template Creation using CSV file.

In `zabbix` we dont have a better way to capture `snmptraps`. we have to manually create an `item` and corresponfding `trigger` to handle a trap arriving from the device. 

Here is what we are doing to do this in more efficient way.
Create a CSV file which contains all the OID and details about it, typically using MIB browser like `ireasoning`. 

This will give us an initial CSV to start with, which can update to make sure we have a CSV required as mentioned below. 

Here is what we are doing in this script. 

1. Get all the MIB files for the Device.
2. Generate a CSV file which contains all the information for the Traps.
3. Run the python script and create a zabbix template.
4. Upload the template to zabbix.

#### Get all the MIB files for the Device.

Load MIB files

![files](http://zubayr.github.io/images/mib_load.png)

Selecting files.

![files](http://zubayr.github.io/images/mib_load_2.png)

Loading completed, select `traps` to export

![files](http://zubayr.github.io/images/mib_export_csv.png)

Export `trap`s to CSV, here the file.

![files](http://zubayr.github.io/images/mib_export_csv_file_view.png)


#### Generate a CSV file which contains all the information for the Traps.

Converting the exported CSV to the below format so that we can parse it.

![files](http://zubayr.github.io/images/mib_export_csv_custom.png)

#### Run the python script and create a zabbix template.

Checking the file.

![files](http://zubayr.github.io/images/mib_running_python_check.png)

Executing script.

![files](http://zubayr.github.io/images/mib_running_python_script.png)

New template created.

![files](http://zubayr.github.io/images/mib_running_python_script_new_template.png)

Created XML file.

![files](http://zubayr.github.io/images/mib_running_python_script_new_template_xml_view.png)


#### Upload the template to zabbix.

Importing the newly created template.

![files](http://zubayr.github.io/images/zabbix_import_1.jpg)

Choose XML template file.

![files](http://zubayr.github.io/images/zabbix_import_2.jpg)

Selecting the template xml file.

![files](http://zubayr.github.io/images/zabbix_import_3.jpg)

Import complete.

![files](http://zubayr.github.io/images/zabbix_import_4.jpg)

Here is how the template looks like.

![files](http://zubayr.github.io/images/zabbix_import_5.jpg)

### Preparing the CSV file. 

IMPORTANT thing for the script is to create the CSV file. After this all we have to do is to `import` the template and use them.
More refinement needs to be done in the `regex_expression` used in `triggers` to capture `snmptraps` more efficiently. Current `regex_expression` looks as below

    'snmptrap["(\\b' + alarm_values['oid'] + '$\\b)"]'

We are looking for the `ALARM` as a whole word, and should be the `end of line` suggested by `$` in the trapfile, which is updated by the trap which originates, default location for traps in zabbix is `/tmp/zabbix_traps.tmp`, more information on this can be found in this [link](http://zubayr.github.io/enable-snmp-trapper-in-zabbix/). 
 

#### Step 0

Before we start use iReasoning to export trap into a CSV file.
This will help us to create the file below. 

#### Step 1:

Create a file with below header. 

    MIB-MODULE,MIB File,OID,Name,Recommended Action,Comments,Description,Trigger Description,Dependency,cleartime In Days

* **MIB-MODULE** : MIB Module name information, this can be got from the export file.
* **MIB File** : File name from which the OID was extracted.
* **OID** : OID to be process and captured in zabbix `snmptrap`.
* **Name** : Trap Name
* **Recommended Action** : Recommended action or the priority which can be assigned. We can used these string in this column `Discard`, `Threshold`, `Clear`, `Log`, `Information`, `Minor`,  `Average`,`Major`, `Critical`.
* **Comments** : Any comments required, this is not used in the script. [OPTIONAL]
* **Description** : Detail description can be found in the export file generated using ireasoning MIB browser.
* **Trigger Description** : Trigger name which needs to be displayed in an event of Alarm [Max 255 characters]
* **Dependency** : Enter the OID which is dependent. 
 
Example to add dependency. 

    If `.1.3.6.1.4.1.37963.6.3.1.3.3` == Clear Trap for `.1.3.6.1.4.1.37963.6.3.1.3.2` then
        1. Set Recommended Action for oid `.1.3.6.1.4.1.37963.6.3.1.3.3` as `Clear`
        2. Set `.1.3.6.1.4.1.37963.6.3.1.3.3` as the Dependency for `.1.3.6.1.4.1.37963.6.3.1.3.2`
    Else
        1. Set Dependency for `.1.3.6.1.4.1.37963.6.3.1.3.2` as `NONE`

* **cleartime In Days** : Clear trap in days 3d (`d` regers to Days, by default the value is in `seconds`.)
    

### Understanding directory structure.

Below are the directory structure which has the file.

1. **input_csv** : As the name suggests input csv as in the format mentioned above.
2. **templates** : After executing the below script, files will be located in this directory.


### Using script in code.  

We can import the file and create small snippet. This will help in automating creation of templates if we need to create them for multiple devices. 

    import zabbix_snmptrap_template_import_from_csv
    
    file_processing_list = [{'file_path': 'input_csv/checkpoint_node_traps.csv',
                                        'template_name': 'Template SNMP Traps CHECKPOINT Nodes',
                                        'template_group': 'Custom Template Globe Touch'},
                            {'file_path': 'input_csv/cisco_node_traps.csv',
                                        'template_name': 'Template SNMP Traps CISCO Nodes',
                                        'template_group': 'Custom Template Globe Touch'},
                            {'file_path': 'input_csv/hp_hh3c_node_traps.csv',
                                        'template_name': 'Template SNMP Traps HP HH3C Nodes',
                                        'template_group': 'Custom Template Globe Touch'},
                            {'file_path': 'input_csv/p4_poland_node_traps.csv',
                                        'template_name': 'Template SNMP Traps P4 Nodes',
                                        'template_group': 'Custom Template Globe Touch'},
                            {'file_path': 'input_csv/affirmed_node_traps.csv',
                                        'template_name': 'Template SNMP Traps AFFIRMED Nodes',
                                        'template_group': 'Custom Template Globe Touch'}]
    
    for file_to_process in file_processing_list:
        print file_to_process
        xml_tree_gen_as_string = zabbix_snmptrap_template_import_from_csv.zabbix_snmptrap_template_import_from_fogg_csv \
                                    (file_to_process['file_path'], file_to_process['template_name'],
                                     file_to_process['template_group'])
        zabbix_snmptrap_template_import_from_csv.xml_pretty_me\
                                    ('templates/' + file_to_process['template_name'].lower().replace(' ', '-') +
                                                '-item-template-trigger-import.xml', xml_tree_gen_as_string)
                                                
                                                

### Using python script directly 

Below is an example command to execute the script from command.

    [ahmed@zabbix-server-master ~]$ python zabbix_snmptrap_template_import_from_csv.py \
    -e input_csv/hp_hh3c_node_traps.csv -n "Template SNMP Traps HP Nodes" -g "Custom Template Globe Touch" -d

Here are more options using `-h`.

    [ahmed@zabbix-server-master ~]$ python zabbix_snmptrap_template_import_from_csv.py -h
    usage: zabbix_snmptrap_template_import_from_csv.py [-h] -e EXPORT_CSV -n
                                                       TEMPLATE_NAME -g
                                                       TEMPLATE_GROUP [-d] [-v]
    
    optional arguments:
      -h, --help            show this help message and exit
      -e EXPORT_CSV, --export-csv EXPORT_CSV
                            OID file, Gives all OIDs on the device
      -n TEMPLATE_NAME, --template-name TEMPLATE_NAME
                            Template name as given in Zabbix server.
      -g TEMPLATE_GROUP, --template-group TEMPLATE_GROUP
                            Template Group which the Template belongs to, as in
                            Zabbix server.
      -d, --debug           Running Debug mode - More Verbose
      -v, --verbose         Running Debug mode - More Verbose
      
      
IMPORTANT thing for the script is to create the CSV file. After this all we have to do is to `import` the template and use them.
More refinement needs to be done in the `regex_expression` used in `triggers` to capture `snmptraps` more efficiently. Current `regex_expression` looks as below

    'snmptrap["(\\b' + alarm_values['oid'] + '$\\b)"]'

We are looking for the `ALARM` as a whole word, and should be the `end of line` suggested by `$` in the trapfile, which is updated by the trap which originates, default location for traps in zabbix is `/tmp/zabbix_traps.tmp`, more information on this can be found in this [link](http://zubayr.github.io/enable-snmp-trapper-in-zabbix/). 
