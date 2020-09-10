#!/usr/bin/python3

import sys

# Creates a table with all the well names as rows.
# This can then be populated with the first and last points to fit a straight line over.

if len(sys.argv) < 2:
	print("\nUsage: make_points_table.py calculated_output.csv\n")
	quit()

fr = open(sys.argv[1], 'r')	# input should be the calculated_output.csv file
lines = fr.readlines()
wells = lines[0].split()[1:]	# the well names are taken from the first line of the csv file
fr.close()

print("Wells extracted:")
for well in wells:
	print(well)

# Outputs a table with headers: well	first	last
# This can then be populated and used in the line fitting
fw = open('points_table.txt', 'w')
fw.write("well\tfirst\tlast\n")
for well in wells:
	fw.write(well)
	fw.write("\n")
fw.close()
