import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
import seaborn as sns
plt.rcParams.update({'font.size': 22})

model = "CanESM5"
hlines = True
scenario = "126"
GWLs = [0, 1, 1.5,2,3]
after2070 = False

gmst = xr.open_dataset("../outputdata/gmst_"+model+"_ssp"+scenario+".nc")

colors = sns.color_palette("colorblind")[:len(GWLs)]
labels = ["Preindustrial",r"+1$^{\circ}$C",r"+1.5$^{\circ}$C",r"+2$^{\circ}$C",r"+3$^{\circ}$C","+4$^{\circ}$C"]

plt.figure(figsize=(20,10))
plt.title("Global annual mean surface temperature anomaly for SSP"+scenario)

def find_nearest_index(array, value):

    array = np.asarray(array)
    idx = np.nanargmin(np.abs(array - value))

    return idx

for i in range(len(gmst.ensmemb)):

    baseline = np.mean(gmst.tas.isel(ensmemb=i)[:20])
    
    deltaT = gmst.tas.isel(ensmemb=i)-baseline
    
    twentyyrmean = deltaT.rolling(time=20,center=True).mean()

    plt.scatter(gmst.time,deltaT,color="grey")

    idx_min = 0
    idx_max = 20
    
    if i == 0:

        plt.scatter(gmst.time[idx_min:idx_max], deltaT[idx_min:idx_max], color=colors[0],label=labels[0])
    else:
        plt.scatter(gmst.time[idx_min:idx_max], deltaT[idx_min:idx_max],color=colors[0])

    if hlines == True:
        plt.hlines(y=twentyyrmean[find_nearest_index(twentyyrmean,0)], xmin=gmst.time[0], xmax=gmst.time[-1], color=colors[0],linewidth=2, linestyle='--')

    for l in range(1,len(GWLs)):
        
        if after2070 == True:

            if GWLs[l] == 1.5:

                idx_after2070 = find_nearest_index(twentyyrmean.sel(time=slice(2070,2101)),GWLs[l])
                idx = 2070-1850+idx_after2070
            else:

                idx = find_nearest_index(twentyyrmean,GWLs[l])
        else:

            idx = find_nearest_index(twentyyrmean,GWLs[l])

        idx_min = idx - 10
        idx_max = idx + 10
       
        if i == 0:
            plt.scatter(gmst.time[idx_min:idx_max], deltaT[idx_min:idx_max], label=labels[l],color=colors[l])
        else:
            plt.scatter(gmst.time[idx_min:idx_max], deltaT[idx_min:idx_max], color=colors[l])

        if hlines == True:
            plt.hlines(y=twentyyrmean[idx], xmin=gmst.time[0], xmax=gmst.time[-1], color=colors[l], linewidth=2, linestyle='--')
        

plt.ylabel("Surface temperature change")
plt.grid()
plt.legend(loc="upper left")
plt.ylim([-0.5,8.5])
if scenario == "126" and after2070 == True: 
    plt.savefig("../figures/GMST/gmst_hlines_"+model+"_ssp"+scenario+"_after2070.png")
else:
    plt.savefig("../figures/GMST/gmst_hlines_"+model+"_ssp"+scenario+".png")


