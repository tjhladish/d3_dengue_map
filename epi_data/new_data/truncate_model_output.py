#!/usr/bin/python
from sys import argv, exit

new_start_day = 365*15 # cut first 15 years off the beginning of the runs

if len(argv) < 2:
    print "\n\tUsage:\ttruncate_model_output.py csv_file1 [csv_file2 [...]]\n"
    exit()

for epi_data_filename in argv[1:]:
    print "processing:", epi_data_filename
    output_filename = epi_data_filename[:-3] + 'trunc.csv' # replace csv trunc.csv
    fo = open(output_filename, 'w')
    for line in file(epi_data_filename):
        p = line.strip().split(',')
        day = int(p[0]) - new_start_day
        if day >= 0:
            fo.write(','.join([str(day)] + p[1:]) + '\n')
    fo.close()
