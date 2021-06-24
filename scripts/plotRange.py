import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from groupbySeason import groupbySeason, groupManybySeason
plt.rcParams.update({'font.size': 12})

preInd = xr.open_dataset("../outputdata/preInd.nc")
plus1 = xr.open_dataset("../outputdata/plus1.nc")
plus2 = xr.open_dataset("../outputdata/preInd.nc")
plus3 = xr.open_dataset("../outputdata/plus3.nc")
plus4 = xr.open_dataset("../outputdata/plus4.nc")

MAM, JJA, SON, DJF = groupManybySeason([preInd, plus1, plus2, plus3, plus4])

seasons = [MAM, JJA, SON, DJF]
season_means = []
season_longname = ["Spring", "Summer", "Autumn", "Winter"]
season_shortname = ["MAM", "JJA", "SON", "DJF"]

for i in range(len(seasons)):

    season_means.append( seasons[i].tas.mean("year").mean("dayofyear") )



colors = ["black","cyan","green","yellow","red"]
labels = ["Preindustrial",r"+1$^{\circ}$C",r"+2$^{\circ}$C",r"+3$^{\circ}$C","+4$^{\circ}$C"]

fname = ["alaska","canada","fscand","wsib","esib","us","ea","eu","arc","afr","sam","sane","china","india","land"]
name = ["Alaska", "Canada", "Fennoscandia", "West Siberia", "East Siberia","the USA","East Asia","Europe","the Arctic","Africa","South America","Sane","China", "India","global land areas"]

"""
for i in range(1):

    fig = plt.figure(figsize=(10,5))
    fig.suptitle("Mean and spread of annual cycle of "+name[i])

    fig.add_subplot(121)
    plt.hlines(y=0,  xmin=0, xmax=365, linestyle="--",color="grey")
    plt.scatter(dayofyear,pi_annavg.isel(region=i),s=5,color="black",label="Preindustrial")
    plt.scatter(dayofyear,pi_min.isel(region=i),s=1,color="black")


"""
