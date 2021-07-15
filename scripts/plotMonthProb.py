import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
from groupbySeason import groupbySeason, groupManybySeason
from getGWLdata import getGWLdata
plt.rcParams.update({'font.size': 20})

model = "CanESM5"
scenario = "585"
GWLs = [0, 1, 1.5, 2, 3, 4]

var_shortname = ['tas','ts','pr','abswind','mrso']
var_longname = ['temperature','skin temperature','precipitation','windspeed','soil moisture']
var_unit = ['$^{\circ}$C','$^{\circ}$C','mm d$^{-1}$','m s$^{-1}$','kg m$^{-2}$']
var_binsize = [2, 2, 0.5,0.4,10]

reg_shortname = ["alaska","canada","fscand","wsib","esib","us","ea","eu","arc","afr","sam","sane","china","india","land"]
reg_longname = ["Alaska", "Canada", "Fennoscandia", "West Siberia", "East Siberia","USA","East Asia","Europe","Arctic","Africa","South America","Scandinavia","China", "India","Global land areas"]
spring_regions = [0,1,2,3,4]
autumn_regions = [0,1,2,3,4] 

season_longname = ["spring", "summer", "autumn", "winter"]
season_shortname = ["MAM", "JJA", "SON", "DJF"]

colors = sns.color_palette("colorblind")[:6]
labels = ["Preindustrial",r"+1$^{\circ}$C",r"+1.5$^{\circ}$C",r"+2$^{\circ}$C",r"+3$^{\circ}$C","+4$^{\circ}$C"]


for var in range(len(var_shortname)):

    GWL_data = getGWLdata(var_shortname[var], model, scenario, GWLs)

    dayofyear = GWL_data[0].dayofyear
    nreg = len(GWL_data[0].region)


    MAM, JJA, SON, DJF = groupManybySeason(GWL_data)
    seasons = [MAM, JJA, SON, DJF]

    binsize = var_binsize[var]

    fig = plt.figure(figsize=(14,8))
    figshape = 230


    for region in spring_regions:
        
        xmin = np.min(seasons[0].isel(region=region))
        xmax = np.max(seasons[0].isel(region=region))
 
        xlims = [xmin,xmax]

        bins = np.arange(xlims[0],xlims[-1],binsize)
        print("Variable:", var_shortname[var],", Region:",reg_longname[region],", xmin = ",np.array(xmin),", xmax = ", np.array(xmax))
            
        fig.suptitle("PDF of daily "+var_longname[var]+" in "+reg_longname[region]+" in "+season_longname[0])

        fig.add_subplot(figshape+1)

        plt.title(season_shortname[0])

        for l in range(len(GWLs)):

            gwl_data = np.array(seasons[0].isel(GWL=l,region=region)).flatten()

            n,x,_ = plt.hist(gwl_data,bins=bins,histtype=u"step",density=True,color="white")
            bin_centers = 0.5*(x[1:]+x[:-1])
            plt.plot(bin_centers,n,linewidth=2,color=colors[l])

        plt.xlabel(r"Daily "+var_longname[var]+" ["+var_unit[var]+"]")
        plt.xlim(xlims)

        fig.add_subplot(figshape+2)
        plt.title("March")

        for l in range(len(GWLs)):

            gwl_data = np.array(seasons[0].isel(dayofyear=slice(0,30),GWL=l,region=region)).flatten()

            n,x,_ = plt.hist(gwl_data,bins=bins,histtype=u"step",density=True,color="white")
            bin_centers = 0.5*(x[1:]+x[:-1])
            plt.plot(bin_centers,n,linewidth=2,color=colors[l])

        plt.xlabel(r"Daily "+var_longname[var]+" ["+var_unit[var]+"]")
        plt.xlim(xlims)

        fig.add_subplot(figshape+4)
        plt.title("April")

        for l in range(len(GWLs)):

            gwl_data = np.array(seasons[0].isel(dayofyear=slice(31,61),GWL=l,region=region)).flatten()

            n,x,_ = plt.hist(gwl_data,bins=bins,histtype=u"step",density=True,color="white")
            bin_centers = 0.5*(x[1:]+x[:-1])
            plt.plot(bin_centers,n,linewidth=2,color=colors[l])

        plt.xlabel(r"Daily "+var_longname[var]+" ["+var_unit[var]+"]")
        plt.xlim(xlims)

        fig.add_subplot(figshape+5)
        plt.title("May")

        for l in range(len(GWLs)):

            gwl_data = np.array(seasons[0].isel(dayofyear=slice(62,93),GWL=l,region=region)).flatten()

            n,x,_ = plt.hist(gwl_data,bins=bins,histtype=u"step",density=True,color="white")
            bin_centers = 0.5*(x[1:]+x[:-1])
            plt.plot(bin_centers,n,linewidth=2,color=colors[l],label=labels[l])

        plt.xlabel(r"Daily "+var_longname[var]+" ["+var_unit[var]+"]")
        plt.xlim(xlims)
    
        fig.tight_layout()
        fig.legend(bbox_to_anchor=(0.5, 0.1, 0.4, 0.5))

        if region < 5:
            fig.savefig("../figures/ACRoBEAR/monthlyPDFs/pdf_"+var_shortname[var]+"_"+model+"_ssp"+scenario+"_"reg_shortname[region]+"_MAMmonths.png")
        else:
            fig.savefig("../figures/OtherRegions/monthlyPDFs/pdf_"+var_shortname[var]+"_"+model+"_ssp"+scenario+"_"+reg_shortname[region]+"_MAMmonths.png")

        plt.clf()


    for region in autumn_regions:
        
        xmin = np.min(seasons[2].isel(region=region))
        xmax = np.max(seasons[2].isel(region=region))

        xlims = [xmin,xmax]

        bins = np.arange(xlims[0],xlims[-1],binsize)
        print("Variable:", var_shortname[var],", Region:",reg_longname[region],", xmin = ",np.array(xmin),", xmax = ", np.array(xmax))

        fig.suptitle("PDF of daily "+var_longname[var]+" in "+reg_longname[region]+" in "+season_longname[2])

        fig.add_subplot(figshape+1)

        plt.title(season_shortname[2])

        for l in range(len(GWLs)):

            gwl_data = np.array(seasons[2].isel(GWL=l,region=region)).flatten()
            n,x,_ = plt.hist(gwl_data,bins=bins,histtype=u"step",density=True,color="white")
            bin_centers = 0.5*(x[1:]+x[:-1])
            plt.plot(bin_centers,n,linewidth=2,color=colors[l])

        plt.xlabel(r"Daily "+var_longname[var]+" ["+var_unit[var]+"]")
        plt.xlim(xlims)

        fig.add_subplot(figshape+2)
        plt.title("September")

        for l in range(len(GWLs)):
            gwl_data = np.array(seasons[2].isel(dayofyear=slice(0,29),GWL=l,region=region)).flatten()

            n,x,_ = plt.hist(gwl_data,bins=bins,histtype=u"step",density=True,color="white")
            bin_centers = 0.5*(x[1:]+x[:-1])
            plt.plot(bin_centers,n,linewidth=2,color=colors[l])

        plt.xlabel(r"Daily "+var_longname[var]+" ["+var_unit[var]+"]")
        plt.xlim(xlims)

        fig.add_subplot(figshape+4)
        plt.title("October")

        for l in range(len(GWLs)):

            gwl_data = np.array(seasons[2].isel(dayofyear=slice(30,61),GWL=l,region=region)).flatten()

            n,x,_ = plt.hist(gwl_data,bins=bins,histtype=u"step",density=True,color="white")
            bin_centers = 0.5*(x[1:]+x[:-1])
            plt.plot(bin_centers,n,linewidth=2,color=colors[l])

        plt.xlabel(r"Daily "+var_longname[var]+" ["+var_unit[var]+"]")
        plt.xlim(xlims)

        fig.add_subplot(figshape+5)
        plt.title("November")

        for l in range(len(GWLs)):

            gwl_data = np.array(seasons[2].isel(dayofyear=slice(62,92),GWL=l,region=region)).flatten()

            n,x,_ = plt.hist(gwl_data,bins=bins,histtype=u"step",density=True,color="white")
            bin_centers = 0.5*(x[1:]+x[:-1])
            plt.plot(bin_centers,n,linewidth=2,color=colors[l],label=labels[l])

        plt.xlabel(r"Daily "+var_longname[var]+" ["+var_unit[var]+"]")
        plt.xlim(xlims)

        fig.tight_layout()
        fig.legend(bbox_to_anchor=(0.5, 0.1, 0.4, 0.5))

        if region < 5:
            fig.savefig("../figures/ACRoBEAR/monthlyPDFs/pdf:"+var_shortname[var]+"_"+model+"_ssp"+scenario+"_"+reg_shortname[region]+"_SONmonths.png")
        else:
            fig.savefig("../figures/OtherRegions/monthlyPDFs/pdf_"+var_shortname[var]+"_"+model+"_ssp"+scenario+"_"+reg_shortname[region]+"_SONmonths.png")




            
