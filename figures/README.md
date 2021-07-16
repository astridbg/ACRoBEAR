## Figures

The folder is divided into /ACRoBEAR/ and /OtherRegions/: one folder for the ACRoBEAR regions (Alaska, Canada, Fennoscandia, West Siberia, East Siberia) and one for the other regions we have looked at (India, China, East Asia, Africa, South America, USA, the Arctic, Scandinavia, Europa and global land areas).

In addition, we have one folder /GMST/ containing plots of the global annual mean surface temperature of the Earth, which we have calculated for different models and shared socio-economic pathways.

In the /ACRoBEAR/ and /OtherRegions/ folders you find the following folders:

### /allregionspdf/ 
Containing probability density function (PDF) plots for each variable and each season for regions grouped together five and five (from which program?)

### /annualCycles/
containing the folders:
 - /MeanMinMaxCycles/: 
     - containing annual cycles for a variable averaged over ensemble members and with minimum and maximum values for two warming levels
 - /PDFCycles/
      - containing annual cycles of probability density for different values of a variable, with all warming levels grouped together
* /individualPDFs/: containing PDFs for individual regions and variables
* /montlyPDFs/: containing PDFs for individual seasons divided up into months
/PDFchange/: containing different measures for how the PDF has changed, boht through displacement in overlap area from preindustrial climate (dispment) and changes in mean and standard deviation of the PDF (pdfchange).
/summaryFigs/: tables of summary figures

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


