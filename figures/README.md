## Figures

The folder is divided into /ACRoBEAR/ and /OtherRegions/: one folder for the ACRoBEAR regions (Alaska, Canada, Fennoscandia, West Siberia, East Siberia) and one for the other regions we have looked at (India, China, East Asia, Africa, South America, USA, the Arctic, Scandinavia, Europa and global land areas).

In addition, we have one folder /GMST/ containing plots of the global annual mean surface temperature of the Earth, which we have calculated for different models and shared socio-economic pathways.

In the /ACRoBEAR/ and /OtherRegions/ folders you find the following folders:

#### /allregionspdf/ 
- Containing probability density function (PDF) plots for each variable and each season for regions grouped together five and five. Some are from a single scenario, other compare different scenarios. From plotSingleScenario.py and plotDoubleScenario.py

#### /annualCycles/
- Containing the folders:
* /MeanMinMaxCycles/ 
   * Containing annual cycles for a variable averaged over ensemble members and with minimum and maximum values for two warming levels. From plotCycle.py.
* /PDFCycles/
   * Containing annual cycles of probability density for different values of a variable, with all warming levels grouped together. From plotcyclePDF.py.
      
#### /individualPDFs/ 
- Containing PDFs for individual regions and variables. Mother plot no longer exists.

#### /monthlyPDFs/
- Containing PDFs for individual seasons (for a variable and region) divided up into months. From plotMonthProb.py

#### /PDFchange/
- Containing different measures for how the PDF has changed, boht through displacement in overlap area from preindustrial climate (dispment) and changes in mean and standard deviation of the PDF (pdfchange). From plotPDFchange_meanStd.py and plotPDFchange_varOverlap.py
 
#### /summaryFigs/
- Containing tables of all variables for all area and three different GWL, with colors strengt marking how much displaced the PDF has become for the warming and color (red/blue) marking the spread change of the variable (positive/negative). From plotSummary.py


