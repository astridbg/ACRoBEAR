# ACRoBEAR
This is an overview of preliminary investigations of future climate variability in Arctic regions, as a part of Arctic Community Resilience to Boreal Environmental change: Assessing Risks from fire and disease (ACRoBEAR).

Our goal has been to quantify the changes in daily variability in climate variables such as temperature, precipitation, wind, and soil moisture, as well as more composite variables or these such as consecutive drays, percentage of warm days and warm spell duration, through the changes in probability density funcitons. We have also investigated the yearly cycles of these properties and how they evolve with time. The resulting figures can be found in the folder /figures/. We have used climate model data which we have divided into different global warming levels based on the global annual mean surface temperature. The climate models we have used so far are MPI-ESM1-2-LR and CanESM5. Our methods can be found the programs in the folder /scripts/.

For this project, we have considered regions in Alaska, Canada, Fennoscandia, West Siberia and East Siberia. However, we have also applied our methods to other parts of the world. The latitude and longitude values of the regions we have used can be found in the program /scripts/calcAreagrid.py

We have also adapted a program from the Canadian Forest Service which calculates the daily Fire Weather Index, given daily temperature, relative humidity, windspeed and precipitation. This program can be found in the folder /fwiModel/, along with some test data.
