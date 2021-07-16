import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
from getGWLdata import getGWLdata
plt.rcParams.update({'font.size': 20})


#-Variable specifications------------------------------------------------------------------

model = "CanESM5"               # Which model are you using+
scenario = "585"                # Which shared socio-economic pathway are you using?
GWLs = [0, 1, 1.5, 2, 3, 4]     # Which global warmning levels are you using?
var_list = [0]                  # Which variables are you using (indices of var_shortname)?

#------------------------------------------------------------------------------------------

var_shortname = ['tas','ts','pr','abswind','mrso']
var_longname = ['Surface temperature','Skin temperature','Precipitation','Windspeed','Soil moisture']
var_unit = ['$^{\circ}$C','$^{\circ}$C','mm d$^{-1}$','m s$^{-1}$','kg m$^{-2}$']

reg_shortname = ["alaska","canada","fscand","wsib","esib","us","ea","eu","arc","afr","sam","sane","china","india","land"]
reg_longname = ["Alaska", "Canada", "Fennoscandia", "West Siberia", "East Siberia","the USA","East Asia","Europe","the Arctic","Africa","South America","Sane","China", "India","global land areas"]

colors = sns.color_palette("colorblind")[:6]
labels = ["Preindustrial",r"+1$^{\circ}$C",r"+1.5$^{\circ}$C",r"+2$^{\circ}$C",r"+3$^{\circ}$C","+4$^{\circ}$C"]

#------------------------------------------------------------------------------------------

for var in var_list:
    
    GWL_data = getGWLdata(var_shortname[var], model,scenario, GWLs)
    
    dayofyear = GWL_data[0].dayofyear
    nreg = len(GWL_data[0].region)

    fig = plt.figure(figsize=(20,10))
    
    for i in range(nreg):

        fig.suptitle("Mean and spread of annual cycle of "+reg_longname[i])
        
        fig.add_subplot(121)
        plt.hlines(y=0,  xmin=0, xmax=365, linestyle="--",color="grey")
        for l in [0, 3]:
            plt.scatter(dayofyear,GWL_data[l].mean("year").isel(region=i),s=15,color=colors[l],label=labels[l])
            plt.scatter(dayofyear,GWL_data[l].min("year").isel(region=i),s=5,color=colors[l])
            plt.scatter(dayofyear,GWL_data[l].max("year").isel(region=i),s=5,color=colors[l])
        plt.xlabel("Day")
        plt.xticks([100, 200, 300], ['100','200','300'])
        plt.ylabel(var_longname[var]+" ["+var_unit[var]+"]")
        plt.grid()
    
        fig.add_subplot(122)
        baseline = GWL_data[0].mean("year").isel(region=i)
        for l in [0, 3]:
            plt.scatter(dayofyear,GWL_data[l].mean("year").isel(region=i)-baseline,s=15,color=colors[l],label=labels[l])
            plt.scatter(dayofyear,GWL_data[l].min("year").isel(region=i)-baseline,s=5,color=colors[l])
            plt.scatter(dayofyear,GWL_data[l].max("year").isel(region=i)-baseline,s=5,color=colors[l])
        plt.xlabel("Day")
        plt.xticks([100, 200, 300], ['100','200','300'])
        plt.ylabel(var_longname[var]+" change"+" ["+var_unit[var]+"]")
        plt.legend(loc="lower right")
        plt.grid()

        fig.tight_layout()
        if i < 5:
            fig.savefig("../figures/ACRoBEAR/annualCycles/MeanMinMaxCycles/cycle_"+var_shortname[var]+"_"+model+"_ssp"+scenario+"_"+reg_shortname[i]+".png")
        else:
            fig.savefig("../figures/OtherRegions/annualCycles/MeanMinMaxCycles/cycle_"+var_shortname[var]+"_"+model+"_ssp"+scenario+"_"+reg_shortname[i]+".png")

        plt.clf()
