#!/usr/bin/python3
import sys
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
from matplotlib import cm
from input_tools import UserInput

'''
This script takes the calculated_output file containing the processed curve data in each well from the platereader, and an input table containing the points to plot a line over for each reaction. It plots a line over the points using numpy polyfit which is a least squares fit. It then outputs the m and c values obtained for each reaction alongside a picture showing the fit.
'''


if sys.version_info[0] == 2:
	from Tkinter import  *
elif sys.version_info[0] == 3:
	from tkinter import *


class File_Obj:
	number=1
	def __init__(self, filename, fit_input_data):
		self.name = filename
		self.number = File_Obj.number
		self.first_fit_point = int(fit_input_data[1])	# comes from input table and is the points over which to fit an initial rate
		self.last_fit_point = int(fit_input_data[2])
		File_Obj.number += 1
		print(self.name, self.first_fit_point, self.last_fit_point)
		
		
	def extract_data(self):
		fr = open(self.name, 'r')
		self.lines = fr.readlines()[1:]

		self.fields = {}
		linenumber = 1
		for line in self.lines:
			fields_tmp = line.split()	# removes carriage return
			self.fields[linenumber] = {}
			for i in range(0, len(fields_tmp)):
				self.fields[linenumber][i] = float(fields_tmp[i])
			linenumber += 1

	def initial_rate_plot(self):
		# fits a line to get an intial rate over the first and last points specified in the input table
		# outputs a picture
		xvals = self.x_data[self.first_fit_point:self.last_fit_point]
		yvals = self.y_data[self.first_fit_point:self.last_fit_point]

		# fits a straight line over the points specified using linear least squares regression		
		line_pars = scipy.stats.linregress(xvals, yvals)
		self.m_val = line_pars[0]
		self.c_val = line_pars[1]
		self.rval = line_pars[2]
		self.r_sq = self.rval**2
		self.y_line_data = [(self.m_val * xx) + self.c_val for xx in self.x_data]


		# plots the full curve, the point over which the fit occured, and the fitted line		
		plt.scatter(xvals, yvals, c='r')

		plt.scatter(self.x_data[self.last_fit_point:], self.y_data[self.last_fit_point:], c='k')
		if self.first_fit_point != 0:
			plt.scatter(self.x_data[0:self.first_fit_point], self.y_data[0:self.first_fit_point], c='k')
		plt.plot(self.x_data, self.y_line_data, c='r')

		plt.axis([0,self.x_data[-1]*1.1, 0, max(self.y_data)*1.1])
		text = "y = %6.5fx + %6.5f , $R^2$ = %6.5f" % (self.m_val, self.c_val, self.r_sq)
		plt.annotate(text, (max(self.x_data)/3, max(self.y_data)/4))

		plt.xlabel("Time (s)")
		plt.ylabel("[G6P] ($\mu$M)")

		fname = "./fit_images/%s_fitted_line.png" % self.name
		plt.savefig(fname)
		plt.clf()
		
	def dump_data(self):
		x_data, y_data = [], []
		for entry in self.fields.keys():
			x_data.append(self.fields[entry][0])
			y_data.append(self.fields[entry][1])
		return x_data, y_data

	def store_data(self, x, y):
		self.x_data = x
		self.y_data = y

		self.last_point = len(self.x_data)

	
class File_Holder:
	def __init__(self, file_list, input_table):
		self.contents = file_list
		self.points_table = input_table
	
	def create_objects(self):
		self.file_objects = {}
		fr = open(self.points_table, 'r')
		lines = fr.readlines()[1:]
		
		for i in range(0, len(self.contents)):
			filename = self.contents[i]
			fitting_input_data = lines[i].split()
			self.file_objects[filename] = File_Obj(filename, fitting_input_data)

	



input_table = sys.argv[-1] 	# the input table has the points to fit for each curve
print("'%s' found" % input_table)
file_holder = File_Holder(sys.argv[1:-1], input_table)
file_holder.create_objects()

fw = open("output_file.txt", 'w')
fw.write("well\tfirst\tlast\tmval\tcval\tR-squared\n")
for file in sorted(file_holder.file_objects.values(), key= lambda x : x.name):
	file.extract_data()
	x, y = file.dump_data()
	file.store_data(x, y)
	file.initial_rate_plot()
	fw.write("%s\t%i\t%i\t%6.5f\t%6.5f\t%6.5f\n" % (file.name[6:], file.first_fit_point, file.last_fit_point, file.m_val, file.c_val, file.r_sq))
fw.close()

	




