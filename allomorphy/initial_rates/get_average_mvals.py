#!/usr/bin/python3

import sys
import numpy as np
import scipy.stats
import math

# This takes an output table from multi_csv_linefit.py and gets the average m value data for each condition.

if len(sys.argv)<2:
	print("\nUsage:\tget_average_mvals.py\toutput_file.txt\n")
	quit()


# read file and extract data
fr = open(sys.argv[1], 'r')
lines = fr.readlines()
print("\nWARNING: Make sure blank wells are removed from the output file.\n")


average_dict = {}
for line in lines[1:]:
	well, f, l, mval, cval, r_sq = line.split()
	condition_id = well[1:3]	# the number of the column on the plate. there should be three with each number, each having the same conditions
	average_dict.setdefault(condition_id, [])
	average_dict[condition_id].append(float(mval))

fw = open('average_mvals.txt', 'w')
fw.write("plate_column\tmval\tstd_dev\tstd_err\n")
for condition_id in sorted(average_dict.keys(), key=lambda x : int(x)):
	if len(average_dict[condition_id])>3:
		# there should only be three repeats per condition
		print("WARNING: Condition %s contains more than three repeats. This is unusual.\n" % condition_id)
	mvals = average_dict[condition_id]
	mean_mval = np.mean(mvals)		# mean of the three mvalues
	std_dev = np.std(mvals, ddof=1) 	# sample std dev of the three mvalues
	std_err = scipy.stats.sem(mvals)	# standard error of the mean of the three mvalues
	fw.write("%s\t%6.5f\t%6.5f\t%6.5f\n" % (condition_id, mean_mval, std_dev, std_err))
fw.close()
	


	
	





# checks for blank wells and removes them

