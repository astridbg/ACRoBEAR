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


var_shortname = ['tas']
var_longname = ['temperature']
var_unit = ['$^{\circ}$C']
var_xlim = [[-50,50]]

bins = np.arange(-50,52,2)

fig = plt.figure(figsize=(30,20))

for var in range (len(var_shortname)):

    for i in range(len(seasons)):

        for k in range(3):

            region_list = region_lists[k]
            fig.suptitle("PDFs of daily "+var_longname[var]+" in "+season_longname[i]+" ("+season_shortname[i]+")")
            f = 1

            for region in region_list:

                fig.add_subplot(320+f)
                plt.title(reg_longname[region])

                for l in range(len(MAM.GWL)):

                    gwl_data = np.array(seasons[i][var_shortname[var]].isel(GWL=l,region=region)).flatten()

                    n,x,_ = plt.hist(gwl_data,bins=bins,histtype=u"step",density=True,color="white")
                    bin_centers = 0.5*(x[1:]+x[:-1])

                    if region == region_list[-1]:
                        plt.plot(bin_centers,n,linewidth=2,color=colors[l],label=labels[l])
                    else:
                        plt.plot(bin_centers,n,linewidth=2,color=colors[l])
                
                    area = sum(2*n)
                    print("Area under graph: ", area)

                plt.xlabel(r"Daily "+var_longname[var]+" ["+var_unit[var]+"]")
               # plt.ylabel("PDF, "+season_longname[i]+" ("+season_shortname[i]+")")
                plt.xlim(var_xlim[var])

                f += 1


            fig.legend(loc='lower right')
            fig.tight_layout()
            fig.savefig("../figures/pdfByRegion/pdf_"+var_shortname[var]+"_"+regions_names[k]+"_"+season_shortname[i]+".png")
            plt.clf()


