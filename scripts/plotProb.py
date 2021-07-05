import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
from groupbySeason import groupbySeason, groupManybySeason
plt.rcParams.update({'font.size': 25})

var_shortname = ['tas','ts','pr']
var_longname = ['temperature','skin temperature','precipitation']
var_unit = ['$^{\circ}$C','$^{\circ}$C','mm d$^{-1}$']
var_xlim = [[-50,50],[-50,50],[0,10]]
var_bins = [np.arange(-50,52,2),np.arange(-50,52,2),np.arange(0,21,0.5)]

for var in range(3):
    preInd = xr.open_dataset("../outputdata/pi_"+var_shortname[var]+"_regAll.nc")
    plus1 = xr.open_dataset("../outputdata/plus1_"+var_shortname[var]+"_regAll.nc")
    plus1_5 = xr.open_dataset("../outputdata/plus1-5_"+var_shortname[var]+"_regAll.nc")
    plus2 = xr.open_dataset("../outputdata/plus2_"+var_shortname[var]+"_regAll.nc")
    plus3 = xr.open_dataset("../outputdata/plus3_"+var_shortname[var]+"_regAll.nc")
    plus4 = xr.open_dataset("../outputdata/plus4_"+var_shortname[var]+"_regAll.nc")

    dayofyear = preInd.dayofyear
    nreg = len(preInd.region)

    if var == 0 or var == 1:
        preInd[var_shortname[var]] -= 273.15
        plus1[var_shortname[var]] -= 273.15
        plus1_5[var_shortname[var]] -= 273.15
        plus2[var_shortname[var]] -= 273.15
        plus3[var_shortname[var]] -= 273.15
        plus4[var_shortname[var]] -= 273.15

    elif var == 2:
        preInd[var_shortname[var]] *= 86400
        plus1[var_shortname[var]] *= 86400
        plus1_5[var_shortname[var]] *= 86400
        plus2[var_shortname[var]] *= 86400
        plus3[var_shortname[var]] *= 86400
        plus4[var_shortname[var]] *= 86400


    reg_shortname = ["alaska","canada","fscand","wsib","esib","us","ea","eu","arc","afr","sam","sane","china","india","land"]
    reg_longname = ["Alaska", "Canada", "Fennoscandia", "West Siberia", "East Siberia","USA","East Asia","Europe","Arctic","Africa","South America","Scandinavia","China", "India","Global land areas"]

    region_lists = [[0,1,2,3,4],[14,9,10,5,8],[6,13,12,7,11]]
    regions_names = ["boreal","aframarc","eurasia"]

    MAM, JJA, SON, DJF = groupManybySeason([preInd, plus1, plus1_5, plus2, plus3, plus4])
    seasons = [MAM, JJA, SON, DJF]
    season_longname = ["spring", "summer", "autumn", "winter"]
    season_shortname = ["MAM", "JJA", "SON", "DJF"]

    Tlevels = [1, 1.5, 2, 3, 4]
    colors = sns.color_palette("colorblind")[:6]
    labels = ["Preindustrial",r"+1$^{\circ}$C",r"+1.5$^{\circ}$C",r"+2$^{\circ}$C",r"+3$^{\circ}$C","+4$^{\circ}$C"]

    bins = var_bins[var]

    fig = plt.figure(figsize=(30,20))
    figshape = 230

    for i in range(len(seasons)):

        for k in range(3):

            region_list = region_lists[k]
            fig.suptitle("PDFs of daily "+var_longname[var]+" in "+season_longname[i]+" ("+season_shortname[i]+")")
            f = 1

            for region in region_list:

                fig.add_subplot(figshape+f)
                plt.title(reg_longname[region])

                for l in range(len(MAM.GWL)):
                    
                    gwl_data = np.array(seasons[i][var_shortname[var]].isel(GWL=l,region=region)).flatten()
                    
                    n,x,_ = plt.hist(gwl_data,bins=bins,histtype=u"step",density=True,color="white")
                    bin_centers = 0.5*(x[1:]+x[:-1])

                    if region == region_list[-1]:
                        plt.plot(bin_centers,n,linewidth=2,color=colors[l],label=labels[l])
                    else:
                        plt.plot(bin_centers,n,linewidth=2,color=colors[l])
                
                    area = sum((bins[1]-bins[0])*n)
                    print("Area under graph: ", area)

                plt.xlabel(r"Daily "+var_longname[var]+" ["+var_unit[var]+"]")
               # plt.ylabel("PDF, "+season_longname[i]+" ("+season_shortname[i]+")")
                plt.xlim(var_xlim[var])

                f += 1


            fig.legend(bbox_to_anchor=(0.5, 0, 0.4, 0.5))
            fig.tight_layout()

            if k == 0:
                fig.savefig("../figures/ACRoBEAR/allRegionsPDFs/pdf_"+var_shortname[var]+"_"+season_shortname[i]+".png")
            else:
                fig.savefig("../figures/OtherRegions/allRegionsPDFs/pdf_"+var_shortname[var]+"_"+regions_names[k]+"_"+season_shortname[i]+".png")
            
            plt.clf()

