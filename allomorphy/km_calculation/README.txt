This script is for calculating kinetic parameters using intial rate data from experiments run at different concentrations of g1p and gbp.

The data has been obtained by running turnover reactions at different, fixed concentrations of gbp, and varying the g1p concentration. For this reason each input file represents a single gbp conc and contains rates at various g1p concs.

To run the script, simply open the program and adjust the g1p concentrations and gbp concentrations that were used.

If data points are missing this can be accomodated by uncommenting certain bits of code which are indicated in the program.


Usage: km_plotter.py <gbp_1uM_data> <gbp_2uM_data> <gbp_5uM_data> ...
