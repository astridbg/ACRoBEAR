# Functions and calculation programs

## Functions

#### gv3.py
- A script that averages over a given region, given longitude values, latitude values and a region mask, weighting each grid point with its respective area. Also checks if there are any missing (non-finite or very high) values in the dataset. Used in calcGMST.py, but replaced later due to slow speed.


 
## Calculation scripts

#### cleanField.py

#### calcAreagrid.py
- A script for which you can specify the regions you want to look at and which model you are using, and which will then give you a dataset containing region masks for all the regions, weighted with the area of the grid points. Partly replaces gv3.py. The output is given in the file regAreagrid_modelname_All.nc on the cic-qbo server under /regions/.

#### calcGMST.py
- A script that calculates the global annual mean surface temperature for a given scenario and model. Gives a time series of both historical and scenario years.

#### 


## Plotting functions




