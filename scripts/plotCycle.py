import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from groupbySeason import groupbySeason, groupManybySeason
plt.rcParams.update({'font.size': 12})

preInd = xr.open_dataset("../outputdata/preInd.nc")
plus1 = xr.open_dataset("../outputdata/plus1.nc")
plus2 = xr.open_dataset("../outputdata/plus2.nc")
plus3 = xr.open_dataset("../outputdata/plus3.nc")
plus4 = xr.open_dataset("../outputdata/plus4.nc")

dayofyear = preInd.dayofyear

pi_annavg = preInd.tas.mean("year")-273.15
pi_annspread = preInd.tas.std("year")
p2_annavg = plus2.tas.mean("year")-273.15
p2_annspread = plus2.tas.std("year")
p1_annavg = plus1.tas.mean("year")-273.15
p3_annavg = plus3.tas.mean("year")-273.15
p4_annavg = plus4.tas.mean("year")-273.15


fname = ['alaska','canada','fscand','wsib','esib']
name = ["Alaska", "Canada", "Fennoscandia", "West Siberia", "East Siberia"]
"""
for i in range(5):

    fig = plt.figure(figsize=(10,5))
    fig.suptitle("Mean and spread of annual cycle of "+name[i])
    
    fig.add_subplot(121)
    plt.hlines(y=0,  xmin=0, xmax=365, linestyle="--",color="grey")
    plt.scatter(dayofyear,pi_annavg.isel(region=i),s=5,color="black",label="Preindustrial")
    plt.scatter(dayofyear,pi_annavg.isel(region=i)+pi_annspread.isel(region=i),s=1, color="black")
    plt.scatter(dayofyear,pi_annavg.isel(region=i)-pi_annspread.isel(region=i),s=1,color="black")
    plt.scatter(dayofyear,p2_annavg.isel(region=i),s=5,color="green",label=r"+2$^{\circ}$C")
    plt.scatter(dayofyear,p2_annavg.isel(region=i)+p2_annspread.isel(region=i),s=1, color="green")
    plt.scatter(dayofyear,p2_annavg.isel(region=i)-p2_annspread.isel(region=i),s=1,color="green")
    plt.xlabel("Day")
    plt.xticks([100, 200, 300], ['100','200','300'])
    plt.ylabel("Surface temperature")
    #plt.legend(loc="lower right")
    plt.grid()
    
    fig.add_subplot(122)
    plt.hlines(y=0,  xmin=0, xmax=365, linestyle="--",color="grey")
    plt.scatter(dayofyear,pi_annavg.isel(region=i)-pi_annavg.isel(region=i),s=5,color="black",label="Preindustrial")
    plt.scatter(dayofyear,pi_annspread.isel(region=i),s=1, color="black")
    plt.scatter(dayofyear,-pi_annspread.isel(region=i),s=1,color="black")
    plt.scatter(dayofyear,p2_annavg.isel(region=i)-pi_annavg.isel(region=i),s=5,color="green",label=r"+2$^{\circ}$C")
    plt.scatter(dayofyear,p2_annavg.isel(region=i)-pi_annavg.isel(region=i)+p2_annspread.isel(region=i),s=1, color="green")
    plt.scatter(dayofyear,p2_annavg.isel(region=i)-pi_annavg.isel(region=i)-p2_annspread.isel(region=i),s=1,color="green")
    plt.xlabel("Day")
    plt.xticks([100, 200, 300], ['100','200','300'])
    plt.ylabel("Surface temperature change")
    plt.yticks(np.arange(-15,16,5), ['-15','-10','-5','0','5','10','15'])
    plt.legend(loc="lower right")
    plt.grid()

    fig.tight_layout()
    fig.savefig("../figures/cycle_"+fname[i]+".png")

for i in range(1):

    fig = plt.figure(figsize=(6,5))
    fig.suptitle("Mean of annual cycle of "+name[i])

    fig.add_subplot(111)
    plt.hlines(y=0,  xmin=0, xmax=365, linestyle="--",color="grey")
    plt.scatter(dayofyear,p4_annavg.isel(region=i),s=5,color="red",label=r"+4$^{\circ}$C")
    plt.scatter(dayofyear,p3_annavg.isel(region=i),s=5,color="yellow",label=r"+3$^{\circ}$C")
    plt.scatter(dayofyear,p2_annavg.isel(region=i),s=5,color="green",label=r"+2$^{\circ}$C")
    plt.scatter(dayofyear,p1_annavg.isel(region=i),s=5,color="cyan",label=r"+1$^{\circ}$C")
    plt.scatter(dayofyear,pi_annavg.isel(region=i),s=5,color="black",label="Preindustrial")
    plt.xlabel("Day")
    plt.xticks([100, 200, 300], ['100','200','300'])
    plt.ylabel("Surface temperature")
    plt.legend(loc="lower right")
    plt.grid()

    fig.tight_layout()
    fig.savefig("../figures/cycle_"+fname[i]+"_evolve.png")

"""


MAM, JJA, SON, DJF = groupManybySeason([preInd, plus1, plus2])
print(DJF)
print(DJF.GWL)
print(DJF.isel(GWL=0))

