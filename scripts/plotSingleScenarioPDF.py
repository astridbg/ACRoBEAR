import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
from groupbySeason import groupbySeason, groupManybySeason
from getGWLdata import getGWLdata
from extremeIndices import CDD,TX90p,WSDI
plt.rcParams.update({'font.size': 28})

model = "MPI-ESM1-2-LR"
scenario = "585"
GWLs = [0, 1, 1.5, 2, 3, 4]
var_list = [0]

var_shortname = ['tas','ts','pr','abswind','mrso','CDD','TX90p','WSDI']
d = "daily"; D = "Daily"
var_longname = [d+' temperature',d+' skin temperature',d+' precipitation',d+' windspeed',d+' soil moisture','consecutive dry days','warm days','warm spell duration']
var_Longname = [D+' temperature',D+' skin temperature',D+' precipitation',D+' windspeed',D+' soil moisture','Consecutive dry days','Warm days','Warm spell duration']
var_unit = ['$^{\circ}$C','$^{\circ}$C','mm d$^{-1}$','m s$^{-1}$','kg m$^{-2}$','d','%','d']
var_xlim = [[[-50,50],[-40,40],[-20,50]],[[-50,50],[-40,40],[-20,50]],[[0,10],[0,10],[0,10]],[[0,8],[0,8],[0,8]],[[200,1750],[450,1300],[250,1250]]]
var_binsize = [2, 2, 0.5,0.4,10,5,4,2]

reg_shortname = ["alaska","canada","fscand","wsib","esib","us","ea","eu","arc","afr","sam","sane","china","india","land"]
reg_longname = ["Alaska", "Canada", "Fennoscandia", "West Siberia", "East Siberia","USA","East Asia","Europe","Arctic","Africa","South America","Scandinavia","China", "India","Global land areas"]
#region_lists = [[0,1,2,3,4],[14,9,10,5,8],[6,13,12,7,11]]
#region_names = ["boreal", "aframarc", "eurasia"]
region_lists = [[0,1,2,3,4],[7,11,5,8,14],[6,13,12,9,10]]
regions_names = ["boreal","euusarc","afrea"]

season_longname = ["spring", "summer", "autumn", "winter"]
season_shortname = ["MAM", "JJA", "SON", "DJF"]

colors = sns.color_palette("colorblind")[:6]
labels = ["Preindustrial",r"+1$^{\circ}$C",r"+1.5$^{\circ}$C",r"+2$^{\circ}$C",r"+3$^{\circ}$C","+4$^{\circ}$C"]


for var in var_list:

    GWL_data = getGWLdata(var_shortname[var], model, scenario, GWLs)

    dayofyear = GWL_data[0].dayofyear
    nreg = len(GWL_data[0].region)


    MAM, JJA, SON, DJF = groupManybySeason(GWL_data)
    seasons = [MAM, JJA, SON, DJF]

    if var_shortname[var] == "CDD":
        seasons = CDD(seasons)
    elif var_shortname[var] == "TX90p":
        seasons = TX90p(seasons)
    elif var_shortname[var] == "WSDI":
        seasons = WSDI(seasons)

    binsize = var_binsize[var]

    fig = plt.figure(figsize=(30,20))
    figshape = 230

    for k in range(3):

        region_list = region_lists[k]
        
        #xlims = var_xlim[var][k]
        xmin = np.min(seasons[0].isel(region=region_list[0]))
        xmax = np.max(seasons[0].isel(region=region_list[0]))

        for region in region_list[1:]:
            for i in range(1,len(seasons)):
                tempmin = np.min(seasons[i].isel(region=region))
                tempmax = np.max(seasons[i].isel(region=region))
                if tempmin < xmin:
                    xmin = tempmin
                if tempmax > xmax:
                    xmax = tempmax
        xlims = [xmin,xmax]

        bins = np.arange(xlims[0],xlims[-1],binsize)
        print("Variable:", var_shortname[var],", Region:",regions_names[k],", xmin = ",np.array(xmin),", xmax = ", np.array(xmax))
            

        for i in range(len(seasons)):
                
            fig.suptitle("SSP"+scenario+" PDFs of "+var_longname[var]+" in "+season_longname[i]+" ("+season_shortname[i]+")", fontsize=32)
            f = 1

            for region in region_list:

                fig.add_subplot(figshape+f)
                plt.title(reg_longname[region])

                for l in range(len(MAM.GWL)):
                    
                    gwl_data = np.array(seasons[i].isel(GWL=l,region=region)).flatten()
                    
                    density,bins,_ = plt.hist(gwl_data,bins=bins,histtype=u"step",density=True,color="white")
                    bin_centers = 0.5*(bins[1:]+bins[:-1])

                    if region == region_list[-1]:
                        plt.plot(bin_centers,density,linewidth=4,color=colors[l],label=labels[l])
                    else:
                        plt.plot(bin_centers,density,linewidth=4,color=colors[l])
                
                    area = np.sum(np.diff(bins)*density)
                    print("Area under graph: ", area)

                plt.xlabel(var_longname[var]+r" ["+var_unit[var]+"]")
                plt.ylabel("Probability density")
                plt.xlim(xlims)

                f += 1


            fig.legend(bbox_to_anchor=(0.5, -0.05, 0.3, 0.5))
            fig.tight_layout()

            if k == 0:
                fig.savefig("../figures/ACRoBEAR/allRegionsPDFs/pdf_"+var_shortname[var]+"_"+model+"_ssp"+scenario+"_"+season_shortname[i]+".png")
            else:
                fig.savefig("../figures/OtherRegions/allRegionsPDFs/pdf_"+var_shortname[var]+"_"+model+"_ssp"+scenario+"_"+regions_names[k]+"_"+season_shortname[i]+".png")
            
            plt.clf()

