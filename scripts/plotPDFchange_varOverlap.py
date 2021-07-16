import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams.update({'font.size':30})

#-Variable specifications----------------------------------------------------------------

model = "MPI-ESM1-2-LR"         # Which model are you using?
scenario = "585"                # Which shared socio-economic pathway are you using?
GWLs = [0, 1, 1.5, 2, 3, 4]     # Which global warming levels are you using?
var_list = [3]                  # Which indices are you using (indices of var_shortname)?

#----------------------------------------------------------------------------------------

var_shortname = ['tas','ts','pr','abswind','mrso']
var_longname = ['temperature','skin temperature','precipitation','windspeed','soil moisture']
var_unit = ['$^{\circ}$C','$^{\circ}$C','mm d$^{-1}$','m s$^{-1}$','kg m$^{-2}$']
var_binsize = [2, 2, 0.5,0.4,10]
var_combo = [[0,1],[0,2],[0,3],[0,4]]

reg_shortname = ["alaska","canada","fscand","wsib","esib","us","ea","eu","arc","afr","sam","sane","china","india","land"]
reg_longname = ["Alaska", "Canada", "Fennoscandia", "West Siberia", "East Siberia","USA","East Asia","Europe","Arctic","Africa","South America","Scandinavia","China", "India","Global land areas"]
region_lists = [[0,1,2,3,4],[7,11,5,8,14],[6,13,12,9,10]]
region_marker = ["o","v","x","s","D"]
regions_names = ["boreal","euusarc","afrea"]

season_longname = ["spring", "summer", "autumn", "winter"]
season_shortname = ["MAM", "JJA", "SON", "DJF"]

colors = sns.color_palette("colorblind")[:6]
labels = ["Preindustrial",r"+1$^{\circ}$C",r"+1.5$^{\circ}$C",r"+2$^{\circ}$C",r"+3$^{\circ}$C","+4$^{\circ}$C"]

#-----------------------------------------------------------------------------------------

fig = plt.figure(figsize=(23,18))
markersize = 200

for i in var_list:
    
    var1 = var_combo[i][0]
    var2 = var_combo[i][1]
    ds1 = xr.open_dataset("../outputdata/pdfchange_"+var_shortname[var1]+"_"+model+"_ssp"+scenario+".nc")
    ds2 = xr.open_dataset("../outputdata/pdfchange_"+var_shortname[var2]+"_"+model+"_ssp"+scenario+".nc")

    for k in range(3):

        region_list = region_lists[k]

        for season in range(len(season_longname)):

            fig.suptitle("Probability distribution displacement in "+season_longname[season]+" ("+season_shortname[season]+")")
            rm = 0

            pi_regs = []
            reg_one_gwls = []

            for region in region_list:

                pi_reg = plt.scatter(0,0, marker=region_marker[rm], s=markersize,color=colors[0])
                pi_regs.append(pi_reg)

                for l in range(1,len(GWLs)):

                    overlap1 = ds1.overlapArea.isel(GWL=l,season=season,region=region)
                    overlap2 = ds2.overlapArea.isel(GWL=l,season=season,region=region)

                    if region == region_list[0]:
                        reg_one_gwl = plt.scatter(100-overlap1*100,100-overlap2*100,marker=region_marker[rm],s=markersize,color=colors[l])
                        reg_one_gwls.append(reg_one_gwl)
                    else:
                        plt.scatter(100-overlap1*100,100-overlap2*100,marker=region_marker[rm],s=markersize,color=colors[l])

                rm += 1

            legend1=plt.legend([pi_regs[j] for j in range(5)], [reg_longname[j] for j in region_list], bbox_to_anchor=([1.03, 0,0,1]), loc='upper left',title="Regions")
            plt.legend(reg_one_gwls, labels[1:len(GWLs)], bbox_to_anchor=([1.03, 0,0,1]),loc='center left',title="Warming levels")
            plt.gca().add_artist(legend1)
            plt.grid()
            plt.hlines(y = 0, xmin = 0,xmax = 100,zorder=0,color='darkgrey',linewidth=5,linestyle="--")
            plt.vlines(x = 0, ymin = 0,ymax = 100,zorder=0,color='darkgrey',linewidth=5,linestyle="--")
            plt.xlabel("Displacement from "+var_longname[var1]+" distribution in preindustrial time [%]")
            plt.ylabel("Displacement from "+var_longname[var2]+" distribution in preindustrial time [%]")
            fig.tight_layout()

            if k == 0:
                fig.savefig("../figures/ACRoBEAR/PDFchange/dispment_"+var_shortname[var1]+"_"+var_shortname[var2]+"_"+model+"_ssp"+scenario+"_"+season_shortname[season]+".png")
            else:
                fig.savefig("../figures/OtherRegions/PDFchange/dispment_"+var_shortname[var1]+"_"+var_shortname[var2]+"_"+model+"_ssp"+scenario+"_"+regions_names[k]+"_"+season_shortname[season]+".png")

            plt.clf()


