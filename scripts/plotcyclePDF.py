import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
from getGWLdata import getGWLdata
plt.rcParams.update({'font.size': 25})

# This program plots probability density for a given variable for each day of the year, 
# for different warming levels.

#-Variable specifications----------------------------------------------------------------

model = "MPI-ESM1-2-LR"         # Which model are you using?
scenario = "585"                # Which shared socio-economic pathway are you using?
GWLs = [0, 1, 1.5, 2, 3, 4]     # Which global warming levels are you using?
var_list = [3]                  # Which indices are you using (indices of var_shortname)?

#----------------------------------------------------------------------------------------
var_shortname = ['tas','ts','pr','tdiff']
var_longname = ['Surface temperature',"Skin temperature",'Precipitation',r'$\Delta$(T$_{skin}$ - T$_{surface \: air}$']
var_unit = ['$^{\circ}$C','$^{\circ}$C','mm d$^{-1}$','$^{\circ}$C']

reg_shortname = ["alaska","canada","fscand","wsib","esib","us","ea","eu","arc","afr","sam","sane","china","india","land"]
reg_longname = ["Alaska", "Canada", "Fennoscandia", "West Siberia", "East Siberia","USA","East Asia","Europe","The Arctic","Africa","South America","Sane","China", "India","Global land areas"]

colors = sns.color_palette("colorblind")[:6]
titles = ["Preindustrial",r"+1$^{\circ}$C warming",r"+1.5$^{\circ}$C warming",r"+2$^{\circ}$C warming",r"+3$^{\circ}$C warming","+4$^{\circ}$C warming"]
#-----------------------------------------------------------------------------------------

for var in var_list:

    GWL_data = getGWLdata(var_shortname[var], model,scenario, GWLs)

    dayofyear = GWL_data[0].dayofyear
    nyears = len(GWL_data[0].year)
    nreg = len(GWL_data[0].region)

    dayofyears = np.repeat(dayofyear,nyears)
    
    fig = plt.figure(figsize=(30,20))
    figshape = 230 

    for region in range(nreg):
       
        ymin = np.min(GWL_data[0].isel(region=region))
        ymax = np.max(GWL_data[0].isel(region=region))
        
        for l in range(1,len(GWL_data)):
            tempmin = np.min(GWL_data[l].isel(region=region))
            tempmax = np.max(GWL_data[l].isel(region=region))
            if tempmin < ymin:
                ymin = tempmin
            if tempmax > ymax:
                ymax = tempmax

        fig.suptitle(reg_longname[region])
        f = 1

        for l in range(len(GWL_data)):
            
            GWL_data_array = np.array(GWL_data[l].isel(region=region)).flatten()

            fig.add_subplot(figshape+f)
            plt.hist2d(dayofyears, GWL_data_array, bins=100, density=True)
            plt.title(titles[l])
            plt.xlabel("Day")
            plt.xticks([100, 200, 300], ['100','200','300'])
            plt.ylim([ymin,ymax])
            plt.ylabel(var_longname[var]+" ["+var_unit[var]+"]")
            
            f += 1
        
        fig.tight_layout()

        if region < 5:
            fig.savefig("../figures/ACRoBEAR/annualCycles/PDFCycles/pdf2d_"+var_shortname[var]+"_"+model+"_ssp"+scenario+"_"+reg_shortname[region]+".png")
        else:
            fig.savefig("../figures/OtherRegions/annualCycles/PDFCycles/pdf2d_"+var_shortname[var]+"_"+model+"_ssp"+scenario+"_"+reg_shortname[region]+".png")
        
        plt.clf()
        
