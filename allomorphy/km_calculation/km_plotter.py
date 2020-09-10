#!/usr/bin/python3

from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt
import sys


# This script takes initial rate data for a number of gbp and g1p concentrations and fits the
# data to a rate equation, enabling the extraction of certain kinetic parameters (Vmax, Km_g1p, Km_gbp, Ki_g1p)

# The input should be a series of files. Each file corresponds to a the initial rates of reaction
# for a series of g1p concentrations at a fixed gbp concentration
# A single file coresponds to a platereader experiment in which the gbp conc was constant and the
# g1p conc was varied in the normal km kind of way


# Usage:
# km_plotter.py <gbp_1uM_data> <gbp_2uM_data> <gbp_5uM_data> ...

# In each gbp input file, there will be initial rates at different g1p concentrations


#############################################################

if len(sys.argv) < 2:
	print("\n\nThis script globally fits rate data obtained at different g1p and gbp concentrations\n\nUsage: km_plotter.py <gbp_1uM_data> <gbp_2uM_data> <gbp_5uM_data> ...\n\nIn each gbp input file, there will be initial rates at different g1p concentrations\n\n")
	quit()


########################  Functions  ########################

def Km_eqn(substrate, Vmax, Km_g1p, Km_gbp, Ki):
	gbp = np.array([val[0] for val in substrate])
	g1p = np.array([val[1] for val in substrate])

	return  ( Vmax * g1p * gbp ) / (( g1p * gbp ) + ( Km_g1p * gbp ) + (( Km_gbp * g1p ) * (( Ki + g1p) / Ki )))


# Change these values to the G1P and GBP values used in the experiments.
gbp = [0.4, 1, 2, 5, 10]
g1p = [10,20,30,50,70,100,150,200,300,500,700]

substrate = []



for conc_gbp in gbp:
	for conc_g1p in g1p:
		substrate.append((conc_gbp, conc_g1p))

		# If any points in the input data are missing, use the below framework to ignore
		# e.g. in the below, the dataset for [gbp]=50uM is missing [g1p]=5uM & 10uM

		# Similar requirement further down in plotting section
		'''		
		if conc_gbp == 50 and conc_g1p == 5:	
			pass
		elif conc_gbp == 50 and conc_g1p == 10:
			pass
		else:
			substrate.append((conc_gbp, conc_g1p))
		'''

rates = []
errors = []
all_dict = {}


def readfile(infile, i):
	# Reads input files with the format:
	# g1p_conc  initial_rate  stdev_from_replicates

	fr = open(infile, 'r')
	lines = fr.readlines()
	single_rates, single_errs = [], []
	for line in lines:
		fields = line.split()
		rates.append(float(fields[1]))
		errors.append(float(fields[2]))
		single_rates.append(float(fields[1]))
		single_errs.append(float(fields[2]))
	all_dict[i] = (single_rates, single_errs)



########################  Reading Data  ########################

i=0
for file in sys.argv[1:]:
	# Each set of initial rates for a paritular gbp conc is contained in a file and 
	# read in at this point
	readfile(file, i)
	i+=1


# converts the input data into array form
rates_array = np.array(rates)
errors_array = np.array(errors)
subs_array = np.array(substrate)








########################  Fitting  ########################

# Initial guesses for the parameters: Vmax, Km_g1p, Km_gbp, Ki_g1p
pstart = [0.25, 50.0, 5.0, 500.0]

# Global fitting routine using scipy curve_fit
pfit, pcov = optimize.curve_fit(Km_eqn, substrate, rates_array, p0=pstart, sigma=errors_array)
perr = np.sqrt(np.diag(pcov))


print("Vmax = %6.4f +- %6.4f\nKm (g1p) = %6.4f +- %6.4f\nKm (gbp) = %6.4f +- %6.4f\nKi (g1p) = %6.4f +- %6.4f\n" % (pfit[0], perr[0], pfit[1], perr[1], pfit[2], perr[2], pfit[3], perr[3]))




########################  Plotting  ########################


# Produce a plot using the fitted parameters to produce smooth curves with oringal points

# Adjust the concentrations as required
num_points = 201
gbp1 = gbp
g1p1 = list(np.linspace(0,700,num_points))
substrate1 = []

for conc_gbp in gbp1:
	for conc_g1p in g1p1:
		substrate1.append((conc_gbp, conc_g1p))


x = g1p1*len(gbp)	# Creates a list of g1p concs for each gbp concentration
y = Km_eqn(substrate1, pfit[0], pfit[1], pfit[2], pfit[3])	# Fitted y data


# Colour list
cols=['b', 'k', 'r', 'g', 'c', 'm', 'y']*10



plt.clf()

i=0
k=0
j=0
for key, rates in all_dict.items():
	plt.scatter(g1p, rates[0], c=cols[i], label=str(gbp[i]))
	plt.errorbar(g1p, rates[0], yerr=rates[1], linestyle="None", c='k')
	i+=1

	# Use the below code if there are any missing data points, similar to above
	'''
	if key==4:
		plt.scatter(g1p[4:], rates[0], c=cols[i], label=str(gbp1[i]))
		plt.errorbar(g1p[4:], rates[0], yerr=rates[1], linestyle="None", c='k')
		i+=1
	elif key==0:
		plt.scatter(g1p[2:], rates[0], c=cols[i], label=str(gbp1[i]))
		plt.errorbar(g1p[2:], rates[0], yerr=rates[1], linestyle="None", c='k')
		i+=1
	else:
		plt.scatter(g1p, rates[0], c=cols[i], label=str(gbp[i]))
		plt.errorbar(g1p, rates[0], yerr=rates[1], linestyle="None", c='k')
		i+=1
	'''


i=0
j=0
for line in gbp1:
	plt.plot(x[i:i+num_points],y[i:i+num_points], c=cols[j])
	i+=num_points
	j+=1


plt.xlabel("[G1P] ($\mu$M)")
plt.ylabel("Initial rate ($\mu$M $s^{-1}$)")
plt.title(r"Initial reaction rates vs [$\beta$G1P] at different concentrations of $\beta$G16BP")
plt.legend(title=r"[$\beta$G16BP] ($\mu$M)")

plt.show()




