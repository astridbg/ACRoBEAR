import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from groupbySeason import groupbySeason, groupManybySeason
plt.rcParams.update({'font.size': 20})

preInd = xr.open_dataset("../outputdata/preInd.nc")
plus1 = xr.open_dataset("../outputdata/plus1.nc")
plus2 = xr.open_dataset("../outputdata/plus2.nc")
plus3 = xr.open_dataset("../outputdata/plus3.nc")
plus4 = xr.open_dataset("../outputdata/plus4.nc")

dayofyear = preInd.dayofyear


fname = ['alaska','canada','fscand','wsib','esib']
name = ["Alaska", "Canada", "Fennoscandia", "West Siberia", "East Siberia"]


MAM, JJA, SON, DJF = groupManybySeason([preInd, plus1, plus2, plus3, plus4])
seasons = [MAM, JJA, SON, DJF]
season_longname = ["Spring", "Summer", "Autumn", "Winter"]
season_shortname = ["MAM", "JJA", "SON", "DJF"]

colors = ["black","cyan","green","yellow","red"]
labels = ["Preindustrial",r"+1$^{\circ}$C",r"+2$^{\circ}$C",r"+3$^{\circ}$C","+4$^{\circ}$C"]

bins = np.arange(-50,32,2)

for i in range(4):

    for region in range(5):

        fig = plt.figure(figsize=(10,9))
        plt.title("PDF of daily temperature in "+name[region])

        for l in range(len(MAM.GWL)):
   
            gwl_tas = np.array(seasons[i].tas.isel(GWL=l,region=region)).flatten() - 273.15
                
            n,x,_ = plt.hist(gwl_tas,bins=bins,histtype=u"step",density=True,color="white")
            bin_centers = 0.5*(x[1:]+x[:-1])
            plt.plot(bin_centers,n,linewidth=2,color=colors[l],label=labels[l])
            
            plt.xlabel(r"Daily temperature [$^{\circ}$C]")
            plt.ylabel("PDF, "+season_longname[i]+" ("+season_shortname[i]+")")
            plt.grid()
            plt.legend(loc="upper left")
            plt.xlim([-50,30])

            fig.tight_layout()
            fig.savefig("../figures/pdf_tas_"+fname[region]+"_"+season_shortname[i]+".png")

