import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
from groupbySeason import groupbySeason, groupManybySeason
plt.rcParams.update({'font.size': 20})

preInd = xr.open_dataset("../outputdata/pi_tas_regAll.nc")
plus1 = xr.open_dataset("../outputdata/plus1_tas_regAll.nc")
plus1_5 = xr.open_dataset("../outputdata/plus1-5_tas_regAll.nc")
plus2 = xr.open_dataset("../outputdata/plus2_tas_regAll.nc")
plus3 = xr.open_dataset("../outputdata/plus3_tas_regAll.nc")
plus4 = xr.open_dataset("../outputdata/plus4_tas_regAll.nc")

dayofyear = preInd.dayofyear
nreg = len(preInd.region)

preInd['tas'] -= 273.15
plus1['tas'] -= 273.15
plus1_5['tas'] -= 273.15
plus2['tas'] -= 273.15
plus3['tas'] -= 273.15
plus4['tas'] -= 273.15


reg_shortname = ["alaska","canada","fscand","wsib","esib","us","ea","eu","arc","afr","sam","sane","china","india","land"]
reg_longname = ["Alaska", "Canada", "Fennoscandia", "West Siberia", "East Siberia","the USA","East Asia","Europe","the Arctic","Africa","South America","Scandinavia","China", "India","global land areas"]

MAM, JJA, SON, DJF = groupManybySeason([preInd, plus1, plus1_5, plus2, plus3, plus4])
seasons = [MAM, JJA, SON, DJF]
season_longname = ["spring", "summer", "autumn", "winter"]
season_shortname = ["MAM", "JJA", "SON", "DJF"]


Tlevels = [1, 1.5, 2, 3, 4]
colors = sns.color_palette("colorblind")[:6]
labels = ["Preindustrial",r"+1$^{\circ}$C",r"+1.5$^{\circ}$C",r"+2$^{\circ}$C",r"+3$^{\circ}$C","+4$^{\circ}$C"]

var_shortname = ['tas']
var_longname = ['temperature']
var_unit = ['$^{\circ}$C']
var_xlim = [[-50,50]]

bins = np.arange(-50,52,2)

fig = plt.figure(figsize=(14,8))
figshape = 230

for var in range (len(var_shortname)):

    for region in [0,2,11]:
        
        for i in range(1):
            
            fig.suptitle("PDF of daily "+var_longname[var]+" in "+season_longname[i]+", "+reg_longname[region])

            fig.add_subplot(figshape+1)

            plt.title(season_shortname[i])

            for l in range(len(MAM.GWL)):

                gwl_data = np.array(seasons[i][var_shortname[var]].isel(GWL=l,region=region)).flatten()

                n,x,_ = plt.hist(gwl_data,bins=bins,histtype=u"step",density=True,color="white")
                bin_centers = 0.5*(x[1:]+x[:-1])
                plt.plot(bin_centers,n,linewidth=2,color=colors[l])

            plt.xlabel(r"Daily "+var_longname[var]+" ["+var_unit[var]+"]")
            plt.ylabel("PDF")
            plt.xlim(var_xlim[var])

            fig.add_subplot(figshape+2)
            plt.title("March")

            for l in range(len(MAM.GWL)):

                gwl_data = np.array(seasons[i][var_shortname[var]].isel(dayofyear=slice(0,30),GWL=l,region=region)).flatten()

                n,x,_ = plt.hist(gwl_data,bins=bins,histtype=u"step",density=True,color="white")
                bin_centers = 0.5*(x[1:]+x[:-1])
                plt.plot(bin_centers,n,linewidth=2,color=colors[l])

            plt.xlabel(r"Daily "+var_longname[var]+" ["+var_unit[var]+"]")
            plt.xlim(var_xlim[var])

            fig.add_subplot(figshape+4)
            plt.title("April")

            for l in range(len(MAM.GWL)):

                gwl_data = np.array(seasons[i][var_shortname[var]].isel(dayofyear=slice(31,61),GWL=l,region=region)).flatten()

                n,x,_ = plt.hist(gwl_data,bins=bins,histtype=u"step",density=True,color="white")
                bin_centers = 0.5*(x[1:]+x[:-1])
                plt.plot(bin_centers,n,linewidth=2,color=colors[l])

            plt.xlabel(r"Daily "+var_longname[var]+" ["+var_unit[var]+"]")
            plt.xlim(var_xlim[var])

            fig.add_subplot(figshape+5)
            plt.title("May")

            for l in range(len(MAM.GWL)):

                gwl_data = np.array(seasons[i][var_shortname[var]].isel(dayofyear=slice(62,93),GWL=l,region=region)).flatten()

                n,x,_ = plt.hist(gwl_data,bins=bins,histtype=u"step",density=True,color="white")
                bin_centers = 0.5*(x[1:]+x[:-1])
                plt.plot(bin_centers,n,linewidth=2,color=colors[l],label=labels[l])

            plt.xlabel(r"Daily "+var_longname[var]+" ["+var_unit[var]+"]")
            plt.xlim(var_xlim[var])
    
            fig.tight_layout()
            fig.legend(loc="center right")

            if region < 5:
                fig.savefig("../figures/ACRoBEAR/monthlyPDFs/pdf_"+var_shortname[var]+"_"+reg_shortname[region]+"_MAMmonths.png")
            else:
                fig.savefig("../figures/OtherRegions/monthlyPDFs/pdf_"+var_shortname[var]+"_"+reg_shortname[region]+"_MAMmonths.png")

            plt.clf()


    for region in [4,8]:

        for i in range(2,3):

            fig.suptitle("PDF of daily "+var_longname[var]+" in "+reg_longname[region]+" in "+season_longname[i])

            fig.add_subplot(figshape+1)

            plt.title(season_shortname[i])

            for l in range(len(MAM.GWL)):

                gwl_data = np.array(seasons[i][var_shortname[var]].isel(GWL=l,region=region)).flatten()

                n,x,_ = plt.hist(gwl_data,bins=bins,histtype=u"step",density=True,color="white")
                bin_centers = 0.5*(x[1:]+x[:-1])
                plt.plot(bin_centers,n,linewidth=2,color=colors[l])

            plt.xlabel(r"Daily "+var_longname[var]+" ["+var_unit[var]+"]")
            plt.xlim(var_xlim[var])

            fig.add_subplot(figshape+2)
            plt.title("September")

            for l in range(len(MAM.GWL)):

                gwl_data = np.array(seasons[i][var_shortname[var]].isel(dayofyear=slice(0,29),GWL=l,region=region)).flatten()

                n,x,_ = plt.hist(gwl_data,bins=bins,histtype=u"step",density=True,color="white")
                bin_centers = 0.5*(x[1:]+x[:-1])
                plt.plot(bin_centers,n,linewidth=2,color=colors[l])

            plt.xlabel(r"Daily "+var_longname[var]+" ["+var_unit[var]+"]")
            plt.xlim(var_xlim[var])

            fig.add_subplot(figshape+4)
            plt.title("October")

            for l in range(len(MAM.GWL)):

                gwl_data = np.array(seasons[i][var_shortname[var]].isel(dayofyear=slice(30,61),GWL=l,region=region)).flatten()

                n,x,_ = plt.hist(gwl_data,bins=bins,histtype=u"step",density=True,color="white")
                bin_centers = 0.5*(x[1:]+x[:-1])
                plt.plot(bin_centers,n,linewidth=2,color=colors[l])

            plt.xlabel(r"Daily "+var_longname[var]+" ["+var_unit[var]+"]")
            plt.xlim(var_xlim[var])

            fig.add_subplot(figshape+5)
            plt.title("November")

            for l in range(len(MAM.GWL)):

                gwl_data = np.array(seasons[i][var_shortname[var]].isel(dayofyear=slice(62,92),GWL=l,region=region)).flatten()

                n,x,_ = plt.hist(gwl_data,bins=bins,histtype=u"step",density=True,color="white")
                bin_centers = 0.5*(x[1:]+x[:-1])
                plt.plot(bin_centers,n,linewidth=2,color=colors[l],label=labels[l])

            plt.xlabel(r"Daily "+var_longname[var]+" ["+var_unit[var]+"]")
            plt.xlim(var_xlim[var])

            fig.tight_layout()
            fig.legend(loc="center right")

            if region < 5:
                fig.savefig("../figures/ACRoBEAR/monthlyPDFs/pdf_"+var_shortname[var]+"_"+reg_shortname[region]+"_SONmonths.png")
            else:
                fig.savefig("../figures/OtherRegions/monthlyPDFs/pdf_"+var_shortname[var]+"_"+reg_shortname[region]+"_SONmonths.png")




            
