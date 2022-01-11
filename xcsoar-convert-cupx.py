#!/usr/bin/python3

import csv
import sys
import argparse
import os
import binwalk
import shutil
import os, re

# generate temporary directory
temp_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temp")
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# copy cupx_file into temporary directory
cupx_file = sys.argv[1]
cupx_file_name = os.path.basename(cupx_file)
cupx_file_path = os.path.join(temp_dir, cupx_file_name)
shutil.copy(cupx_file_name, cupx_file_path)
cupx_file_extracted_path = temp_dir + '/' + '_' + cupx_file + '.extracted'

# binwalk cupx_file and extract all files

for module in binwalk.scan(cupx_file_path, quiet=True,signature=True,extract=True):
    print ("%s Results: " % module.name)

# look for points.cup file without case sensitivity
for filename in os.listdir(cupx_file_extracted_path):
    if re.search (r"points.cup", filename, re.IGNORECASE):
        cup_file = filename

# look for pics directory without case sensitivity
for directory in os.listdir(cupx_file_extracted_path):
    if re.search (r"pics", directory, re.IGNORECASE):
        pics_dir = directory


# Takes a POINTS.CUP file in cupx format and converts it to a waypoints_details
# file.

input_file = open(cupx_file_extracted_path + "/" + cup_file, 'r')

# convert to unix line format
input_file_content = input_file.read()
input_file_content = input_file_content.replace('\r\n', '\n')
input_file_content = input_file_content.replace('\r', '\n')

# create output directory
if not os.path.exists("output"):
    os.makedirs("output")

cup_unix_file = open("output" + '/' + cupx_file_name + ".cup", 'w')
cup_unix_file.write(input_file_content)
cup_unix_file.close()

cup_unix_file = "output" + '/' + cupx_file_name + ".cup"

# create output sub directories
for subdir in ["pics","docs"]:
    if not os.path.exists("output" + "/" + subdir):
        os.makedirs("output" + "/" + subdir)

# Create a corresponding waypoints_details file
with open(cup_unix_file, 'r') as csv_in_file:
    csv_reader = csv.reader(csv_in_file)
    output_file = open("output/waypoints_details.txt", 'w')
    for row in csv_reader:
        # skip the cup header
        if row[0] == "name":
            continue
        # bullet proofing: if the field 14 does not exist skip the row
        if len(row) >= 15:
            output_file.write("[" + row[0] + "]\n")
            if ';' in row[14]:
                for item in row[14].split(';'):
                    if '.jpg' in item:
                        output_file.write("image=pics/" + item + "\n")
                    if '*.pdf' in item:
                        output_file.write("file=docs/" + item + "\n")
            else:
                if '.jpg' in row[14]:
                    output_file.write("image=pics/" + row[14] + "\n")
                if '.pdf' in row[14]:
                    output_file.write("file=docs/" + row[14] + "\n")
        else:
            continue
            # Add newline for better readability
            output_file.write("\n")
    output_file.close()
# delete temporary directory
shutil.rmtree(temp_dir)
