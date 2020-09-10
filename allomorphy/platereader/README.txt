The process_raw_platereader.py script takes the raw data from the BMG labtech platereader and processes it to generate a file containing G6P concentration data over time for each well.

Run the script with the raw data csv file as the argument. You will be prompted to choose the well containing the blank, then the calculation will be performed resulting in a new filed called calculated_output.csv which contains the G6P concentration in each well at each time point in uM. This can then be further worked on using the km scripts in a separate directory.


NOTE: The formula used for this makes a pathlength correcting calculation using absorbance data at 977 nm and 900 nm. The ratio of these absorbances for a certain pathlength in the well can be calculated. If these readings were not taken, there is an alternative formula in the script that is commented out.


