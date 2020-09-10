#!/usr/bin/python3

"""
Created on 13 Jun 18 by AJR

This script will read a CSV with coupled assay output from BMG labtech platereader and process the raw data to enable kinetic analysis.

The script should take your raw (must be raw) plate reader data at 340nm with water correction readings at 977 and 900nm, and blank measurements, and calculate the proper reading.
It will then put this proper reading in a new column in the dataframe called GusCalc. From here you have your time vs [g6p] and can plot data etc.

There are a variety of functions in the program, some of which are just where I have encapsulated Gus's old code to preserve it should anyone need it.
Just chip and change the 'main' function to decide what the program does.

By default set to:
- output a new csv called 'calculated_output.csv', which has times and all the calculated [g6p] values in uM.

Usage: process_raw_platereader.py <BMG_output_file.csv>

@author: Chris Sharratt 
@author Angus Robertson
@author: Henry Wood

"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import cm
import interface_tools_home as interface
import sys, os, time

version_number = 2.0

if len(sys.argv) < 2:
	print("\n\nProgram for processing raw platereader data\n\nUsage: process_raw_platereader.py <BMG_output_file.csv>\n\n")
	quit()



CSV_file=sys.argv[1]

def find_columns(plate_reader_csv):
    # opens the csv file and where header=6, the columns will equal the well numbers
    well_finder = pd.read_csv(plate_reader_csv, header=6)
    columnnames = ['well', 'times'] + list(well_finder.columns)[2:]
    print(columnnames)
    return columnnames

def select_blank(columnnames):
    # set up a menu which prompts the user to identify the well containing the blank
    blank_ref = interface.Menu('Choose the well containing the blank', columnnames[2:], option_function_pairs=False).display()
    return blank_ref


columnnames = find_columns(CSV_file)
blank_ref = select_blank(columnnames)
print(blank_ref)

concentrations = [0, 0, 1, 3 , 5, 7, 10, 15, 20, 30]
csv_out = "no"      # Change to "yes" if you want full CSV output. 


#==============================================================================
# Here we make the dataframe and do multiplicaitons
#==============================================================================
#This time we try reading it, but NOT using the well in the index.  Should now be able to match on the index field.

# The header keyword is set to accomodate the standard output from BMG labtech OMEGA software.

df1 = pd.read_csv(CSV_file, header=7, index_col = 'times', names = columnnames )


#Note the Syntax, [RowFrom:RowTo, ColumnFrom, ColumnTo], so specifying a specific unrecognised column in the range means make me a new column.

print('Columns to calc are: ')
print(columnnames[2:])

for colname in columnnames[2:]:

    # Result in uM

    df1.loc[df1['well'] == 'Raw Data (340 1)', (colname + 'Corr')] = df1.loc[df1['well'] 
    == 'Raw Data (340 1)'][colname] - df1.loc[df1['well'] == 'Raw Data (340 1)'][blank_ref]

    df1.loc[df1['well'] == 'Raw Data (340 1)', (colname + 'GusCalc')] = df1.loc[df1['well'] 
    == 'Raw Data (340 1)', (colname + 'Corr')] / (((df1.loc[df1['well'] == 'Raw Data (977 3)'][colname] - 
    df1.loc[df1['well'] == 'Raw Data (900 2)'][colname])/0.183)*6220*(1/1000000.0))


    # Alternative calculation without pathlength correction.
    '''
    df1.loc[df1['well'] == 'Raw Data (340 1)', (colname + 'Corr')] = df1.loc[df1['well'] 
    == 'Raw Data (340 1)'][colname] - df1.loc[df1['well'] == 'Raw Data (340 1)'][blank_ref]

    df1.loc[df1['well'] == 'Raw Data (340 1)', (colname + 'GusCalc')] = df1.loc[df1['well'] 
    == 'Raw Data (340 1)', (colname + 'Corr')] / 0.183)*6220*(1/1000000.0))
    '''



    #********  Added to write all of the files independently.  **********

    df2 =   df1[['well', colname, colname + 'Corr', colname + 'GusCalc']]

    
    if csv_out=="yes":
        df2.loc[df2['well'] == 'Raw Data (340 1)'].to_csv(colname+'_verbose.csv')


def output_data():
    output_cols = []
    for columnname in df1.columns:
        if 'GusCalc' in columnname and blank_ref not in columnname:
            output_cols.append(columnname)
    df3 = df1.loc[df1['well'] == 'Raw Data (340 1)', output_cols]
    print(df3.head())
    df3.to_csv('calculated_output.csv', sep=' ')
    


#%%
#==============================================================================
# This outputs just the corrected value vs. time for each column
#==============================================================================
def individual_outputs():
    if csv_out=="yes":
        for colname in columnnames[2:]: 
            df2 = df1[[colname + 'GusCalc']]
            df2 = df2.dropna()
            df2.to_csv(colname+'.csv')
        
    for colname in columnnames[2:]: 
        df2 = df1[[colname + 'GusCalc']]
        df2 = df2.dropna()
        df2.to_csv(colname+'.txt', sep=' ')
    
    
#%%

#==============================================================================
# This plots each of the reactions with color order 
#==============================================================================
def plot_all_data():
    color=iter(cm.rainbow(np.linspace(0,1,len(columnnames)-3)))
    fig=plt.figure(figsize=(16,16))
    plt.title("Turnover series:%s \nPath to file:%s" % (CSV_file, os.getcwd()))

    for i in nc_sorted[1:]:
        c=next(color)
        a = df1[[i[1]+'GusCalc']]
        plt.plot(a[i[1]+'GusCalc'][0:50], label=str(i[0])+" - "+i[1], marker='o', c=c)
        plt.xlabel("Time /s")
        plt.ylabel("Concentration of G6P / uM")
    plt.legend(bbox_to_anchor=(1,1), loc="upper left") 
    fig.subplots_adjust(right=0.85)   
    plt.savefig("All_data_plotted.png", dpi=300)




def multiplot():
    fig1, axes = plt.subplots(4, 3)

    fig1.add_subplot(111, frameon=False)
    plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
    plt.grid(False)
    plt.xlabel("\nTime (s)")
    plt.ylabel("[G6P] (uM)\n")
    
    colours = {'B': '#1565C0', 'D': '#1565C0', 'E': '#E91E63'}
    col_dict = {'B03':(0, 0),
                'B04':(0, 1),
                'B05':(0, 2),
                'B06':(1, 0),
                'B07':(1, 1),
                'B08':(1, 2),
                'B09':(2, 0),
                'B10':(2, 1),
                'B11':(2, 2)
                }
 
    for i in nc_sorted:
        a = df1[[i[1]+'GusCalc']]
        if i[1][2] != "2":
            well_number = col_dict[i[1][0:3]]
            axes[well_number].plot(a.index, a[i[1]+'GusCalc'], color=colours[i[1][0]], marker='o', markersize=2, linewidth=0)
            old_ylabels = axes[well_number].get_yticklabels()
            plt.sca(axes[well_number])
            oldticks = plt.yticks()[0]
            newticks = [x for x in plt.yticks()[0]]
            plt.yticks(oldticks, newticks)
            plt.xticks(rotation='vertical')
            plt.tick_params(labelsize=8)
    plt.subplots_adjust(wspace=0.5, hspace=0.5)
    axes[3,2].axis('off')
    plt.savefig('multiplot.png', dpi=400)
    plt.clf()



#%% This section plots all turnovers separately on the same figure. 
 
#==============================================================================
# tot = len(columnnames[2:])
# matsizex=4
# matsizey = math.ceil(tot/4.0)
# counter=1
# 
# fig=plt.figure(figsize=(32,32))
# plt.title("Turnover series:%s \nPath to file:%s" % (CSV_file, current_dir))
# for colname in columnnames[2:]:
#     ax = fig.add_subplot(matsizey,matsizex,counter)
#     a = df1[[colname+'GusCalc']]
#     ax.plot(a[colname+'GusCalc'], label=colname)
#     plt.legend(loc='upper left')
#     plt.xlabel("Time /s")
#     plt.ylabel("Absorbance")
#     counter+=1
# plt.savefig("plotted_separately.png", dpi=300)
#==============================================================================

#%%
def plot_data_by_well():
    color=iter(cm.rainbow(np.linspace(0,1,len(columnnames)-2)))

    fig=plt.figure(figsize=(16,16))
    plt.title("Turnover series:%s \nPath to file:%s" % (CSV_file, os.getcwd()))
    for colname in columnnames[2:]:
        c=next(color)
        ax = fig.add_subplot(111)
        a = df1[[colname+'GusCalc']]
        ax.plot(a[colname+'GusCalc'], label=colname, c=c)
        plt.xlabel("Time /s")
        plt.ylabel("Concentration of G6P / uM")
    plt.legend(bbox_to_anchor=(1,1), loc="upper left") 
    fig.subplots_adjust(right=0.85) 
    plt.savefig("All_data_plotted_bywell.png", dpi=300)

#%%

#==============================================================================
# Output dynafit text for script correlating concentration and filename. 
#==============================================================================
def output_dynafit_text():
    DF_text=open("DynaFit_text.txt", 'w')
    DF_text.write("[data]\n")
    DF_text.write("directory %s \n" % (os.getcwd()))
    DF_text.write("extension txt\n\n")

    for i in nc_sorted:
        DF_text.write("file %s | concentration G1P = %s \n" % (i[1], i[0]))

def output_info_file():
    date = time.asctime()
    fw = open("what_was_done.txt", "w")
    fw.write("Version of %s used was version: %s\n" % (sys.argv[0], version_number))
    fw.write("Input file was %s\n" % sys.argv[1])
    fw.write("Working directory: %s\n" % os.getcwd())
    fw.write("Date: %s\n" % date)
    fw.write("Columns calculated: %s" % str(columnnames[2:]))
    fw.close()




def main():
    #multiplot()
    output_info_file()
    #plot_all_data()
    output_data()
    
main()











