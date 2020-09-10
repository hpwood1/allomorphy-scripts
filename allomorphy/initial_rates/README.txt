The scripts here are used to take platereader data that has been processed with other scripts into a calculated_output.csv file, and calculate initial rates over the range of conditions tested.

Starting with the calculated_output.csv file, the scripts are run in the following order:





1) make_points_table.py <calculated_output.csv>
2) csv_linefit <calculated_output.csv>
3) get_average_mvals.py <output_no_blanks.txt>
4) make_table_g1p_concs <average_mvals.txt> <g1p_concs.txt>

See below for a detailed description of what to do at each stage.





-------------------------------------------------------

1) make_points_table.py <calculated_output.csv>

This creates a table with each well name in the first column. Then the 'first' and 'last' columns must be populated with the points you want to fit over.
Selection of appropriate section of the curve can be done by eye, or simply by setting the first 10 or 20 points.

-------------------------------------------------------

2) csv_linefit <calculated_output.csv>

Once points_table.txt is full with first and last points for each well, run:

This fits a line over the points specified using linear least squares regression. The outputs are a plot for each fit (sepearate dir) and an output table which contains the mvalues calculated in the fit.

!!! Extra blank wells need to be removed from the table at this point. !!! 

In the example data, the blank wells B04 and B06 need to be removed.

-------------------------------------------------------

3) get_average_mvals.py <output_no_blanks.txt>

This returns a new table called 'average_mvals.txt' which contains the average mvalue for each condition i.e. each column in the platereader.

-------------------------------------------------------

4) make_table_g1p_concs <average_mvals.txt> <g1p_concs.txt> 		NOTE: The order of the arguments matters

This requires a g1p_concs.txt file containing the platereader well number (2 digits, e.g. 01) followed by the concentration of substrate in that well.

This scripts combines these two tables to produce a table containing g1p concentrations, and initial rates with errors.

You can further process this using which is easy to plot:
	
nawk 'NR>1 {print $1, $3, $5}' km_curve_table > km_plot_input

-------------------------------------------------------
