#!/usr/bin/python3

import csv
import sys
import argparse
import os

# Takes a POINTS.CUP file in cupx format and converts it to a waypoints_details
# file.

input_file = open("POINTS.CUP", 'r')

# convert to unix line format
input_file_content = input_file.read()
input_file_content = input_file_content.replace('\r\n', '\n')
input_file_content = input_file_content.replace('\r', '\n')

temp_file = open("POINTS-UNIX.cup", 'w')
temp_file.write(input_file_content)
temp_file.close()

cup_unix_file = "POINTS-UNIX.cup"

# Create a corresponding waypoints_details file
with open(cup_unix_file, 'r') as csv_in_file:
    csv_reader = csv.reader(csv_in_file)
    output_file = open("waypoints_details.txt", 'w')
    for row in csv_reader:
        if row[0] == "name":
            continue
        output_file.write("[" + row[0] + "]\n")
        if ';' in row[13]:
            for item in row[13].split(';'):
                if '.jpg' in item:
                    output_file.write("image=pics/" + item + "\n")
                if '*.pdf' in item:
                    output_file.write("file=pics/" + item + "\n")
        else:
            if '.jpg' in row[13]:
                output_file.write("image=pics/" + row[13] + "\n")
            if '.pdf' in row[13]:
                output_file.write("file=pics/" + row[13] + "\n")
        # Add newline for better readability
        output_file.write("\n")
    output_file.close()
    # remove cupx file
    os.remove(cup_unix_file)
