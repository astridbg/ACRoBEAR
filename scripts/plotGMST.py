import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
import seaborn as sns
plt.rcParams.update({'font.size': 22})

def find_nearest_index(array, value):

    array = np.asarray(array)
    idx = np.nanargmin(np.abs(array - value))

    return idx

gmst = xr.open_dataset("../outputdata/gmst.nc")

Tlevels = [1, 1.5, 2, 3, 4]
colors = sns.color_palette("colorblind")[:6]
#colors = plt.style('tableau-colorblind10')[:5]
labels = [r"+1$^{\circ}$C",r"+1.5$^{\circ}$C",r"+2$^{\circ}$C",r"+3$^{\circ}$C","+4$^{\circ}$C"]

plt.figure(figsize=(20,10))
plt.title("Global annual mean surface temperature anomaly")

for i in range(len(gmst.ensmemb)):

    baseline = np.mean(gmst.tas.isel(ensmemb=i)[:20])
    
    deltaT = gmst.tas.isel(ensmemb=i)-baseline
    
    twentyyrmean = deltaT.rolling(time=20,center=True).mean()

    plt.scatter(gmst.time,deltaT,color="grey")

    idx_min = 0
    idx_max = 20
    
    if i == 0:

        plt.scatter(gmst.time[idx_min:idx_max], deltaT[idx_min:idx_max], color=colors[0],label="Preindustrial")
    else:
        plt.scatter(gmst.time[idx_min:idx_max], deltaT[idx_min:idx_max],color=colors[0])

    plt.hlines(y=twentyyrmean[find_nearest_index(twentyyrmean,0)], xmin=gmst.time[0], xmax=gmst.time[-1], color=colors[0],linewidth=2, linestyle='--')

    for l in range(len(Tlevels)):
        
        idx = find_nearest_index(twentyyrmean,Tlevels[l])

        idx_min = idx - 10
        idx_max = idx + 10
       
        if i == 0:
            plt.scatter(gmst.time[idx_min:idx_max], deltaT[idx_min:idx_max], label=labels[l],color=colors[l+1])
        else:
            plt.scatter(gmst.time[idx_min:idx_max], deltaT[idx_min:idx_max], color=colors[l+1])

        plt.hlines(y=twentyyrmean[idx], xmin=gmst.time[0], xmax=gmst.time[-1], color=colors[l+1], linewidth=2, linestyle='--')


#plt.xlabel("Year")
plt.ylabel("Surface temperature change")
plt.grid()
plt.legend(loc="upper left")
plt.savefig("../figures/gmst_hlines.png")

