import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams.update({'font.size':20})

model = "MPI-ESM1-2-LR"
scenario = "585"
GWLs = [0, 1, 1.5, 2, 3, 4]

var_shortname = ['tas','ts','pr','abswind','mrso']
var_longname = ['Temperature (surface air)','Temperature (skin)','Precipitation','Windspeed','Soil moisture']
var_unit = ['$^{\circ}$C','$^{\circ}$C','mm d$^{-1}$','m s$^{-1}$','kg m$^{-2}$']

reg_shortname = ["alaska","canada","fscand","wsib","esib","us","ea","eu","arc","afr","sam","sane","china","india","land"]
reg_longname = ["Alaska", "Canada", "Fennoscandia", "West Siberia", "East Siberia","USA","East Asia","Europe","Arctic","Africa","South America","Scandinavia","China", "India","Global land areas"]
region_lists = [[0,1,2,3,4],[7,11,5,8,14],[6,13,12,9,10]]
regions_names = ["boreal","euusarc","afrea"]

season_longname = ["spring", "summer", "autumn", "winter"]
season_shortname = ["MAM", "JJA", "SON", "DJF"]

labels = ["Preindustrial",r"+1$^{\circ}$C",r"+1.5$^{\circ}$C",r"+2$^{\circ}$C",r"+3$^{\circ}$C","+4$^{\circ}$C"]

columns = ([labels[2], labels[3], labels[4]]*5)
legend_columns = ['70-100', '45-70','30-45','20-30','10-20','1-10','< 1','1-10','10-20','20-30','30-45','45-70','70-100']
rows = var_longname[:5]
colors = ['navy','mediumblue','royalblue','cornflowerblue','lightsteelblue','lavender','w','mistyrose','lightsalmon','salmon','tomato','red','darkred']

plt.figure(figsize=(20,10))

for season in range(4):
    
    for k in range(3):

        region_list = region_lists[k]
        color_list = []
        
        for variable in var_shortname:
        
            pdfchange = xr.open_dataset("../outputdata/pdfchange_"+variable+"_"+model+"_ssp"+scenario+".nc")
            var_list = []

            for region in region_list:

                for gwl in [2, 3, 4]:
                    
                    overlap = np.array(pdfchange.overlapArea.isel(GWL=gwl,season=season,region=region))
                    baseline_std = np.array(pdfchange.stdValue.isel(GWL=0,season=season,region=region))
                    std_ = np.array(pdfchange.stdValue.isel(GWL=gwl,season=season,region=region))
                    std_anom = std_-baseline_std

                    if overlap > 0.99:
                        idx = 0
                    elif 0.90 < overlap <= 0.99:
                        idx = 1*np.sign(std_anom)
                    elif 0.80 < overlap <= 0.90:
                        idx = 2*np.sign(std_anom)
                    elif 0.70 < overlap <= 0.80:
                        idx = 3*np.sign(std_anom)
                    elif 0.55 < overlap <= 0.70:
                        idx = 4*np.sign(std_anom)
                    elif 0.30 < overlap <= 0.55:
                        idx = 5*np.sign(std_anom)
                    elif overlap <= 0.30:
                        idx = 6*np.sign(std_anom)
                    
                    var_list.append(colors[int(idx+6)])

            
            color_list.append(var_list)


        header = plt.table(cellText=[['']*5],
                            colLabels=[reg_longname[i] for i in region_list],
                            loc='upper right',
                            bbox=[0, 0.75,1.0, 0.1]
                            )

        table = plt.table(cellColours=color_list,
                            rowLabels=rows,
                            colLabels=columns,
                            loc='upper right',
                            bbox=[0, 0.5, 1.0, 0.3]
                            )
        legend_header_1 = plt.table(cellText=[['']],
                            colLabels=['Displacement [%]'],
                            loc = 'upper right',
                            bbox=[0,0.3,1.0,0.1]
                            )
        legend_header_2 = plt.table(cellText=[['']*3],
                            colLabels=['Decreasing spread','','Increasing spread'],
                            colWidths=[0.5-0.5/len(colors),1/len(colors),0.5-0.5/len(colors)],
                            loc = 'upper right',
                            bbox=[0,0.25,1.0,0.1]
                            )

        legend_table = plt.table(cellColours=[colors],
                            rowLabels=["Colours"],
                            colLabels=legend_columns,
                            bbox=[0, 0.2, 1.0, 0.1]
                            )

        plt.axis('tight')
        plt.axis('off')
        plt.tight_layout()
        title = "Predicted PDF displacement in "+season_longname[season]+" ("+season_shortname[season]+") in SSP"+scenario+" ("+model+")"
        plt.text(-0.055,0.05,title,fontsize=24)
        if k == 0:
            plt.savefig("../figures/ACRoBEAR/summaryFigs/table_"+model+"_ssp"+scenario+"_"+season_shortname[season]+".png")
        else:
            plt.savefig("../figures/OtherRegions/summaryFigs/table_"+model+"_ssp"+scenario+"_"+regions_names[k]+"_"+season_shortname[season]+".png")
        plt.clf()
"""
for i in range(4):

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
"""
