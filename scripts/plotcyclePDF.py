import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
from getGWLdata import getGWLdata
plt.rcParams.update({'font.size': 25})

model = "CanESM5"
scenario = "585"
GWLs = [0, 1, 1.5, 2, 3, 4]

var_shortname = ['tas','ts','pr','tdiff']
var_longname = ['Surface temperature',"Skin temperature",'Precipitation',r'$\Delta$(T$_{skin}$ - T$_{surface \: air}$']
var_unit = ['$^{\circ}$C','$^{\circ}$C','mm d$^{-1}$','$^{\circ}$C']

reg_shortname = ["alaska","canada","fscand","wsib","esib","us","ea","eu","arc","afr","sam","sane","china","india","land"]
reg_longname = ["Alaska", "Canada", "Fennoscandia", "West Siberia", "East Siberia","USA","East Asia","Europe","The Arctic","Africa","South America","Sane","China", "India","Global land areas"]

colors = sns.color_palette("colorblind")[:6]
titles = ["Preindustrial",r"+1$^{\circ}$C warming",r"+1.5$^{\circ}$C warming",r"+2$^{\circ}$C warming",r"+3$^{\circ}$C warming","+4$^{\circ}$C warming"]


for var in range(3):

    GWL_data = getGWLdata(var_shortname[var], model,scenario, GWLs)
    print("Data collected")

    dayofyear = GWL_data[0].dayofyear
    nyears = len(GWL_data[0].year)
    nreg = len(GWL_data[0].region)

    dayofyears = np.repeat(dayofyear,nyears)
    
    fig = plt.figure(figsize=(30,20))
    figshape = 230 

    for region in range(nreg):
       
        if var_shortname[var] == 'tbiff':
            ymin = -1
            ymax = 2
        
        else:
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
        
        print("Data plotted")
