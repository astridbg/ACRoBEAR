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

### Calculation scripts

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


### Plotting programs

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

## Workflow
This is a short description of how we end up with the probability density functions. 
#### Postprocessing of the CMIP6 data
The CMIP6 data can be postprocessed (checked for missing data, which is then standardised) in two ways - using *gv3.py* or *cleanField.py*. The gv3.py function postprocesses a single timestep of data while also averaging that timestep over a given region. The cleanField.py program, however, takes a model and a scenario as input, checks the historical run of the model as well as the scenario run, and concatenates the historical and scenario data into one big dataset. If you are making regional averages over many datasets, the cleanField.py program is considerably faster to use beforehand. The program requires that the name of the CMIP6 file is on the form variablename_day_modelname_simulationname_r*i1p1f1_years.nc. In the cic-qbo server under /CMIP6/ you can find the soft links to the CMIP6 datasets with names on this form. 

#### Finding the global warming levels 
The global warming levels are defined as the ten years before and the ten years after the twenty year rolling mean of the global mean annual surface temperature is closest to a certain degree of warming in each ensemble member. The global mean annual surface temperature is calcuated in the *calcGMST.py*program using the gv3.py function, and puts out a dataset of global mean annual surface temperatures for each ensemble member and each year in the length of the historical and scenario run combined. The program requires also that the name of the CMIP6 file is on the form {variable name}_day_{model name}_{simulation name}_r{ensemble member number}i1p1f1_{years}.nc. This dataset is then used when calculating daily regional averages for certain warming levels in the script *calcRegAvg.py*. In this script you can specify the warming levels you want to look at, and it begins with finding the start and end indices of each warming level and each ensemble member in a scenario from the output dataset of calcGMST.py. 

#### Calculating day-to-day regional averages
The day-to-day regional averages are calculated using the program calcRegAvg.py, which gives an output dataset with regionally averaged variables for each region, each day of year, and each year (20 in each warming level x 10 ensemble members = 200 sample years). The program uses datasets that have been post-processed by the cleanField.py scripts, and uses a regional mask that have been specified in the program *calcAreagrid.py*, where each grid is weighted with the area represented by the grid point.  

#### Creating seasonal and regional probability density functions
The probability density functions (PDFs) are created with the output data from calcRegAvg.py, and which is put into histograms based on region and season. The different plotting program display the probability density funcitons visually, while the calcPDFchange.py program quantifies different measures of change in the PDFs, such as mean, spread, overlapping area, etc. 
