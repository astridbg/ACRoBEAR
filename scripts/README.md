## Functions and calculation programs

### Function programs

#### gv3.py
- A function that averages over a given region, given longitude values, latitude values and a region mask, weighting each grid cell with its respective area. Also checks if there are any missing (non-finite or very high) values in the dataset. Used in calcGMST.py, but replaced later due to slow speed.

#### makeRegion.py
- A function that creates a mask of 0 and 1 for a given region (given by longitude values, latitude values and min/max latitude/longitude) where all grid cells inside the region is 1.

#### makeAreagrid.py
- A function that takes latitude values, longitude values and a region mask and gives a mask where all grid cells inside the region is weighted by the area fraction. Partly replaces gv3.py.

#### getGWLdata.py 
 - A function that returns a list of data for different warming levels for a given variable, model and scenario. If the variable is a direct climate data variable, but a product of others (e.g. windspeed), this can be specified in the function and it will return the data product for each warming level. If the variable is not daily data (e.g. consecutive dry days) it will return the relevant variable (precipitation). You can specify that "after2070 = True", which means that it picks out only the 1.5 deg C warming after year 2070 (relevant for SSP126, to check reversability in climate).

#### groupbySeason.py
- Contains two functions: groupbySeason and groupManybySeason. Both takes datasets and group them into four different seasons, but groupManybySeason takes a list of datasets in different warming levels and groups them into four season datasets with GWL as a coordinate. Season start and end date can be specified.

#### extremeIndices.py
- Contains three functions CDD, TX90p and WSDI, which correspond to climate indices. Takes a list of seasons, with GWL as a coordinate, and calculate the climate indices for each season. The index definitions were found here: https://agupubs.onlinelibrary.wiley.com/doi/10.1002/jgrd.50203.

#### findOverlap.py
- A function that finds the overlapping area between two curves, given the x and y values of the two curves.

## Calculation scripts

#### cleanField.py
- A script that checks all ensemble members of a given model variable for both historical years and the years in a given scenario for missing values. Replaces missing values with NaN. Partly replaces gv3.py. Combines the historical and scenario years into one time series, and concatenates together all ensemble member into one big data file that is stored /outputdata/.

#### calcAreagrid.py
- A script for which you can specify the regions you want to look at and which model you are using, and which will then give you a dataset containing region masks for all the regions, weighted with the area of the grid cells using the makeAreagrid function. The output is given in the file regAreagrid_modelname_All.nc on the cic-qbo server under /regions/.

#### calcGMST.py
- A script that calculates the global annual mean surface temperature for a given scenario and model. Gives a time series of both historical and scenario years.

#### calcRegAvg.py
- A script that calculates the 


## Plotting functions




