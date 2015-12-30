import os


def merge_csv(path_to_files, file_to_create):

    list_of_files = os.listdir(path_to_files)

    try:
        os.remove(file_to_create)
    except OSError:
        pass

    file_merge_desc = open(file_to_create, "a")
    for file in list_of_files:
        file_to_read_desc = open(path_to_files + file)
        file_to_read_desc.next()
        file_to_read_desc.next()
        for line in file_to_read_desc:
            file_merge_desc.write(line)
        file_to_read_desc.close()
    file_merge_desc.close()

print 'Merging HP MIBs'
merge_csv('hp/', 'merge_csv/hp_hh3c_merge.csv')

print 'Merging CISCO MIBs'
merge_csv('cisco/', 'merge_csv/cisco_merge.csv')

print 'Merging P4 MIBs'
merge_csv('p4_poland/', 'merge_csv/p4_poland_merge.csv')

print 'Merging ULTICOM MIBs'
merge_csv('ulticom/', 'merge_csv/ulticom_merge.csv')

print 'Merging HGES MIBs'
merge_csv('hges_mibs/', 'merge_csv/hges_merge.csv')

print 'Merging HGES MIBs'
merge_csv('billing_application/', 'merge_csv/billing_apps_merge.csv')