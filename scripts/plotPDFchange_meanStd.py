import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams.update({'font.size':30})

model = "CanESM5"
scenario = "585"
GWLs = [0, 1, 1.5, 2, 3, 4]

var_shortname = ['tas','ts','pr','abswind','mrso']
var_longname = ['temperature','skin temperature','precipitation','windspeed','soil moisture']
var_unit = ['$^{\circ}$C','$^{\circ}$C','mm d$^{-1}$','m s$^{-1}$','kg m$^{-2}$']

reg_shortname = ["alaska","canada","fscand","wsib","esib","us","ea","eu","arc","afr","sam","sane","china","india","land"]
reg_longname = ["Alaska", "Canada", "Fennoscandia", "West Siberia", "East Siberia","USA","East Asia","Europe","Arctic","Africa","South America","Scandinavia","China", "India","Global land areas"]
#region_lists = [[0,1,2,3,4],[14,9,10,5,8],[6,13,12,7,11]]
#region_names = ["boreal", "aframarc", "eurasia"]
region_lists = [[0,1,2,3,4],[7,11,5,8,14],[6,13,12,9,10]]
region_marker = ["o","v","x","s","D"]
regions_names = ["boreal","euusarc","afrea"]

season_longname = ["spring", "summer", "autumn", "winter"]
season_shortname = ["MAM", "JJA", "SON", "DJF"]

colors = sns.color_palette("colorblind")[:6]
labels = ["Preindustrial",r"+1$^{\circ}$C",r"+1.5$^{\circ}$C",r"+2$^{\circ}$C",r"+3$^{\circ}$C","+4$^{\circ}$C"]


fig = plt.figure(figsize=(23,18))
markersize = 300

for i in range(5):

    ds = xr.open_dataset("../outputdata/pdfchange_"+var_shortname[i]+"_"+model+"_ssp"+scenario+".nc")

    for k in range(3):

        region_list = region_lists[k]

        for season in range(len(season_longname)):
            
            fig.suptitle("Probability distribution change in "+season_longname[season]+" ("+season_shortname[season]+")")
            rm = 0
            
            pi_regs = []
            reg_one_gwls = []

            for region in region_list:
                
                baseline_mean = ds.meanValue.isel(GWL=0,season=season,region=region)
                baseline_std = ds.stdValue.isel(GWL=0,season=season,region=region)
                
                pi_reg = plt.scatter(0,0, marker=region_marker[rm], s=markersize,color=colors[0])
                pi_regs.append(pi_reg)

                for l in range(1,len(GWLs)):
                    
                    _mean = ds.meanValue.isel(GWL=l,season=season,region=region)
                    _std = ds.stdValue.isel(GWL=l,season=season,region=region)
                    
                    if region == region_list[0]:
                        reg_one_gwl = plt.scatter(_mean-baseline_mean, _std - baseline_std,marker=region_marker[rm],s=markersize,color=colors[l])
                        reg_one_gwls.append(reg_one_gwl)
                    else:
                        plt.scatter(_mean-baseline_mean, _std - baseline_std,marker=region_marker[rm],s=markersize,color=colors[l])
                
                rm += 1
                
            legend1=plt.legend([pi_regs[j] for j in range(5)], [reg_longname[j] for j in region_list], bbox_to_anchor=([1.03, 0,0,1]), loc='upper left',title="Regions")
            plt.legend(reg_one_gwls, labels[1:len(GWLs)], bbox_to_anchor=([1.03, 0,0,1]),loc='center left',title="Warming levels")
            plt.gca().add_artist(legend1)
            plt.grid()
            plt.hlines(y = 0, xmin = plt.gca().get_xlim()[0],xmax = plt.gca().get_xlim()[1],zorder=0,color='darkgrey',linewidth=5,linestyle="--")
            plt.vlines(x = 0, ymin = plt.gca().get_ylim()[0],ymax = plt.gca().get_ylim()[1],zorder=0,color='darkgrey',linewidth=5,linestyle="--")
            plt.xlabel("Change in mean "+var_longname[i]+" from preindustrial time ["+var_unit[i]+"]")
            plt.ylabel("Change in "+var_longname[i]+" spread (std) from preindustrial time ["+var_unit[i]+"]")
            fig.tight_layout()

            if k == 0:
                fig.savefig("../figures/ACRoBEAR/PDFchange/pdfchange_"+var_shortname[i]+"_"+model+"_ssp"+scenario+"_"+season_shortname[season]+".png")
            else:
                fig.savefig("../figures/OtherRegions/PDFchange/pdfchange_"var_shortname[i]+"_"+model+"_ssp"+scenario+"_"+regions_names[k]+"_"+season_shortname[season]+".png")

            plt.clf()

