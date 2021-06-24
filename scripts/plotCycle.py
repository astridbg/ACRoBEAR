import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from groupbySeason import groupbySeason, groupManybySeason
plt.rcParams.update({'font.size': 12})

preInd = xr.open_dataset("../outputdata/preInd_allreg.nc")
#plus1 = xr.open_dataset("../outputdata/plus1_allreg.nc")
plus2 = xr.open_dataset("../outputdata/plus2_allreg.nc")
#plus3 = xr.open_dataset("../outputdata/plus3_allreg.nc")
#plus4 = xr.open_dataset("../outputdata/plus4_allreg.nc")

dayofyear = preInd.dayofyear
nreg = len(preInd.region)

pi_annavg = preInd.tas.mean("year")-273.15
pi_min = preInd.tas.min("year")-273.15
pi_max = preInd.tas.max("year")-273.15

p2_annavg = plus2.tas.mean("year")-273.15
p2_min = plus2.tas.min("year")-273.15
p2_max = plus2.tas.max("year")-273.15

#pi_annspread = preInd.tas.std("year")
#p2_annspread = plus2.tas.std("year")
#p1_annavg = plus1.tas.mean("year")-273.15
#p3_annavg = plus3.tas.mean("year")-273.15
#p4_annavg = plus4.tas.mean("year")-273.15

fname = ["alaska","canada","fscand","wsib","esib","us","ea","eu","arc","afr","sam","sane","china","india","land"]
name = ["Alaska", "Canada", "Fennoscandia", "West Siberia", "East Siberia","the USA","East Asia","Europe","the Arctic","Africa","South America","Sane","China", "India","global land areas"]


for i in range(nreg):

    fig = plt.figure(figsize=(10,5))
    fig.suptitle("Mean and spread of annual cycle of "+name[i])
    
    fig.add_subplot(121)
    plt.hlines(y=0,  xmin=0, xmax=365, linestyle="--",color="grey")
    plt.scatter(dayofyear,pi_annavg.isel(region=i),s=5,color="black",label="Preindustrial")
    plt.scatter(dayofyear,pi_min.isel(region=i),s=1,color="black")
    plt.scatter(dayofyear,pi_max.isel(region=i),s=1,color="black")
    #plt.scatter(dayofyear,pi_annavg.isel(region=i)+pi_annspread.isel(region=i),s=1, color="black")
    #plt.scatter(dayofyear,pi_annavg.isel(region=i)-pi_annspread.isel(region=i),s=1,color="black")
    plt.scatter(dayofyear,p2_annavg.isel(region=i),s=5,color="green",label=r"+2$^{\circ}$C")
    plt.scatter(dayofyear,p2_min.isel(region=i),s=1,color="green")
    plt.scatter(dayofyear,p2_max.isel(region=i),s=1,color="green")
    #plt.scatter(dayofyear,p2_annavg.isel(region=i)+p2_annspread.isel(region=i),s=1, color="green")
    #plt.scatter(dayofyear,p2_annavg.isel(region=i)-p2_annspread.isel(region=i),s=1,color="green")
    plt.xlabel("Day")
    plt.xticks([100, 200, 300], ['100','200','300'])
    plt.ylabel("Surface temperature")
    #plt.legend(loc="lower right")
    plt.grid()
    
    fig.add_subplot(122)
    plt.scatter(dayofyear,pi_annavg.isel(region=i)-pi_annavg.isel(region=i),s=5,color="black",label="Preindustrial")
    plt.scatter(dayofyear,pi_min.isel(region=i)-pi_annavg.isel(region=i),s=1,color="black")
    plt.scatter(dayofyear,pi_max.isel(region=i)-pi_annavg.isel(region=i),s=1,color="black")
    #plt.scatter(dayofyear,pi_annspread.isel(region=i),s=1, color="black")
    #plt.scatter(dayofyear,-pi_annspread.isel(region=i),s=1,color="black")
    plt.scatter(dayofyear,p2_annavg.isel(region=i)-pi_annavg.isel(region=i),s=5,color="green",label=r"+2$^{\circ}$C")
    plt.scatter(dayofyear,p2_min.isel(region=i)-pi_annavg.isel(region=i),s=1,color="green")
    plt.scatter(dayofyear,p2_max.isel(region=i)-pi_annavg.isel(region=i),s=1,color="green")
    #plt.scatter(dayofyear,p2_annavg.isel(region=i)-pi_annavg.isel(region=i)+p2_annspread.isel(region=i),s=1, color="green")
    #plt.scatter(dayofyear,p2_annavg.isel(region=i)-pi_annavg.isel(region=i)-p2_annspread.isel(region=i),s=1,color="green")
    plt.xlabel("Day")
    plt.xticks([100, 200, 300], ['100','200','300'])
    plt.ylabel("Surface temperature change")
    plt.yticks(np.arange(-20,21,5), ['-20','-15','-10','-5','0','5','10','15','20'])
    plt.legend(loc="lower right")
    plt.grid()

    fig.tight_layout()
    fig.savefig("../figures/cycle_"+fname[i]+".png")

"""
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
