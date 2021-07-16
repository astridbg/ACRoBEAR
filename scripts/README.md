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
- A script that calculates the regional average for a daily variable in a given region using the cleaned data from cleanField.py and the weighted region masks from calcAreagrid.py. Produces files in /outputdata/ for each variable, each scenario, each model and each warming level. The warming levels are found using the global mean surface temperature data from calcGMST.py. Can specify whether "after2070=True", which is relevant for SSP126 on GWL 1.5 degC in MPI-ESM1-2-LR to check reversibility. 

#### calcPDFchange.py
- A script that find the probability density function (PDF) values of the different variables and calculate changes in the PDF, including overlap area change, mean change, and standard deviation change (in respect to preindustrial climate). Stores the data in /outputdata/.


## Plotting programs

#### plotGMST.py
- Plots the global mean surface temperature for different scenarios and models. Plots found in /figures/GMST/

#### plotCycle.py
- Plots the annual cycle, averaged over ensemble members and years in GWLs, for preindustrial climate and +2 degC climate. Also plots minimum and maximum values in each warming level. Plots found in /figures/*insert region*/annualCycles/MeanMinMaxCycles/
  
#### plotcyclePDF.py
- Plots the probability density of different variable values for each days, for all warming levels group together in one plot. Plots found in /figures/*insert region*/annualCycles/PDFCycles/

#### plotSingleScenarioPDF.py
- Plots the PDF for variable in a single scenario, with the different warming levels together. Regions grouped together five and five. Plots found in /figures/*insert region*/allregionsPDF/singleScenario/

#### plotDoubleScenarioPDF.py
- Plots the PDF for variable in with different scenario and/or different models, with the different warming levels together. Regions grouped together five and five. Plots found in /figures/*insert region*/allregionsPDF/compareScenario/

#### plotMonthProb.py
- Plots the PDF for variable for a regio in spring or autumn season, with season divided up into months. Plots found in /figures/*insert region*/monthlyPDF/

#### plotPDFchange_meanStd.py
- Plots scatter plot for change in PDF of variable, for mean and standard deviation change. Plots found in /figures/*insert region*/PDFchange/

#### plotPDFchange_varOverlap.py
- Plots scatter plot of the change in overlap area for one variable compared to another variable. Plots found in /figures/*insert region*/PDFchange/

#### plotSummary.py
- Plots a table of all variables for all area and three different GWL, with colors strengt marking how much displaced the PDF has become for the warming and color (red/blue) marking the spread change of the variable (positive/negative). Plots found in /figures/*insert region*/summaryFigs/



