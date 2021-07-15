import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
from groupbySeason import groupbySeason, groupManybySeason
from getGWLdata import getGWLdata
plt.rcParams.update({'font.size': 28})

model1 = "CanESM5"
model2 = "CanESM5"
scenario1 = "126"
scenario2 = "126"
GWLs = [0, 1, 1.5]
after2070_1 = True
after2070_2 = False

var_shortname = ['tas','ts','pr','abswind','mrso']
var_longname = ['temperature','skin temperature','precipitation','windspeed','soil moisture']
var_unit = ['$^{\circ}$C','$^{\circ}$C','mm d$^{-1}$','m s$^{-1}$','kg m$^{-2}$']
var_xlim = [[[-50,50],[-40,40],[-20,50]],[[-50,50],[-40,40],[-20,50]],[[0,10],[0,10],[0,10]],[[0,8],[0,8],[0,8]],[[200,1750],[450,1300],[250,1250]]]
var_binsize = [2, 2, 0.5,0.4,10]

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


for var in range(len(var_shortname)):
    
    if after2070_1 == True:
        GWL_data1 = getGWLdata(var_shortname[var], model1, scenario1, GWLs,after2070=True)
        GWL_data2 = getGWLdata(var_shortname[var], model2, scenario2, GWLs)
    elif after2070_2 == True:
        GWL_data1 = getGWLdata(var_shortname[var], model1, scenario1, GWLs)
        GWL_data2 = getGWLdata(var_shortname[var], model2, scenario2, GWLs,after2070=True)
    else:
        GWL_data1 = getGWLdata(var_shortname[var], model1, scenario1, GWLs)
        GWL_data2 = getGWLdata(var_shortname[var], model2, scenario2, GWLs)
    
    dayofyear = GWL_data1[0].dayofyear
    nreg = len(GWL_data1[0].region)

    MAM, JJA, SON, DJF = groupManybySeason(GWL_data1)
    seasons1 = [MAM, JJA, SON, DJF]
    MAM, JJA, SON, DJF = groupManybySeason(GWL_data2)
    seasons2 = [MAM, JJA, SON, DJF]

    binsize = var_binsize[var]

    fig = plt.figure(figsize=(30,20))
    figshape = 230

    for k in range(3):

        region_list = region_lists[k]
            
        xlims = var_xlim[var][k]
        xmin = np.min(seasons1[0].isel(region=region_list[0]))
        xmax = np.max(seasons1[0].isel(region=region_list[0]))

        for region in region_list[1:]:
            for i in range(1,len(season_shortname)):
                tempmin = np.min(seasons1[i].isel(region=region))
                tempmax = np.max(seasons1[i].isel(region=region))
                if tempmin < xmin:
                    xmin = tempmin
                if tempmax > xmax:
                    xmax = tempmax
                tempmin = np.min(seasons2[i].isel(region=region))
                tempmax = np.max(seasons2[i].isel(region=region))
                if tempmin < xmin:
                    xmin = tempmin
                if tempmax > xmax:
                    xmax = tempmax

        xlims = [xmin,xmax]

        bins = np.arange(xlims[0],xlims[1],binsize)
        print("Variable:", var_shortname[var],", Region:",regions_names[k],", xmin = ",np.array(xmin),", xmax = ", np.array(xmax))

            
        for i in range(len(season_shortname)):
    
            fig.suptitle("PDFs of daily "+var_longname[var]+" in "+season_longname[i]+" ("+season_shortname[i]+")", fontsize=32)
            f = 1

            for region in region_list:

                fig.add_subplot(figshape+f)
                plt.title(reg_longname[region])
                
                gwl_data1 = np.array(seasons1[i].isel(GWL=0,region=region)).flatten()
                density1,bins,_ = plt.hist(gwl_data1,bins=bins,histtype=u"step",density=True,color="white")

                bin_centers = 0.5*(bins[1:]+bins[:-1])

                if region == region_list[-1]:
                    plt.plot(bin_centers,density1,linewidth=4,color=colors[0],label=labels[0])
                else:
                    plt.plot(bin_centers,density1,linewidth=4,color=colors[0])

                area = np.sum(np.diff(bins)*density1)
                    
                for l in range(1,len(GWLs)):
                    
                    gwl_data1 = np.array(seasons1[i].isel(GWL=l,region=region)).flatten()
                    gwl_data2 = np.array(seasons2[i].isel(GWL=l,region=region)).flatten()

                    density1,bins,_ = plt.hist(gwl_data1,bins=bins,histtype=u"step",density=True,color="white")
                    density2,bins,_ = plt.hist(gwl_data2,bins=bins,histtype=u"step",density=True,color="white")

                    if region == region_list[-1]:
                        if after2070_1 == True:
                            if GWLs[l] == 1.5:
                                plt.plot(bin_centers,density1,linewidth=4,color=colors[l],label="SSP"+scenario1+" after 2070 "+labels[l])
                            else:
                                plt.plot(bin_centers,density1,linewidth=4,color=colors[l],label="SSP"+scenario1+" "+labels[l])                                
                            plt.plot(bin_centers,density2,linewidth=4,color=colors[l],label="SSP"+scenario2+" "+labels[l],linestyle='--')
                        elif after2070_2 == True:
                            plt.plot(bin_centers,density1,linewidth=4,color=colors[l],label="SSP"+scenario1+" "+labels[l])
                            if GWLs[l] == 1.5:
                                plt.plot(bin_centers,density2,linewidth=4,color=colors[l],label="SSP"+scenario2+" after 2070 "+labels[l],linestyle='--')
                            else:
                                plt.plot(bin_centers,density1,linewidth=4,color=colors[l],label="SSP"+scenario1+" "+labels[l])
                        else:    
                            plt.plot(bin_centers,density1,linewidth=4,color=colors[l],label="SSP"+scenario1+" "+labels[l])
                            plt.plot(bin_centers,density2,linewidth=4,color=colors[l],label="SSP"+scenario2+" "+labels[l],linestyle='--')
                    else:
                        plt.plot(bin_centers,density1,linewidth=4,color=colors[l])
                        plt.plot(bin_centers,density2,linewidth=4,color=colors[l],linestyle='--')
                                        
                    area1 = np.sum(np.diff(bins)*density1)
                    area2 = np.sum(np.diff(bins)*density2)

                    print("Area under graph: ", area1, "and", area2)

                plt.xlabel(r"Daily "+var_longname[var]+" ["+var_unit[var]+"]")
                plt.xlim(xlims)

                f += 1


            fig.legend(bbox_to_anchor=(0.5, -0.05, 0.38, 0.5))
            fig.tight_layout()
            
            if model1 == model2:
                if k == 0:
                    if after2070_1 == True:
                        fig.savefig("../figures/ACRoBEAR/allRegionsPDFs/pdf_"+var_shortname[var]+"_"+model1+"_ssp"+scenario1+"_after2070_ssp"+scenario2+"_"+season_shortname[i]+".png")
                    elif after2070_2 == True:
                        fig.savefig("../figures/ACRoBEAR/allRegionsPDFs/pdf_"+var_shortname[var]+"_"+model1+"_ssp"+scenario1+"_ssp"+scenario2+"_after2070_"+season_shortname[i]+".png")
                    else:
                        fig.savefig("../figures/ACRoBEAR/allRegionsPDFs/pdf_"+var_shortname[var]+"_"+model1+"_ssp"+scenario1+"_ssp"+scenario2+"_"+season_shortname[i]+".png")
                else:
                    if after2070_1 == True:
                        fig.savefig("../figures/OtherRegions/allRegionsPDFs/pdf_"+var_shortname[var]+"_"+model1+"_ssp"+scenario1+"_after2070_ssp"+scenario2+"_"+regions_names[k]+"_"+season_shortname[i]+".png")
                    elif after2070_2 == True:
                        fig.savefig("../figures/OtherRegions/allRegionsPDFs/pdf_"+var_shortname[var]+"_"+model1+"_ssp"+scenario1+"_ssp"+scenario2+"_after2070_"+regions_names[k]+"_"+season_shortname[i]+".png")
                    else:
                        fig.savefig("../figures/OtherRegions/allRegionsPDFs/pdf_"+var_shortname[var]+"_"+model1+"_ssp"+scenario1+"_ssp"+scenario2+"_"+regions_names[k]+"_"+season_shortname[i]+".png")
            else:
                if k == 0:
                    if after2070_1 == True:
                        fig.savefig("../figures/ACRoBEAR/allRegionsPDFs/pdf_"+var_shortname[var]+"_"+model1+"_ssp"+scenario1+"_after2070_"+model2+"_ssp+"+scenario2+"_"+season_shortname[i]+".png")
                    elif after2070_2 == True:
                        fig.savefig("../figures/ACRoBEAR/allRegionsPDFs/pdf_"+var_shortname[var]+"_"+model1+"_ssp"+scenario1+"_"+model2+"_ssp"+scenario2+"_after2070_"+season_shortname[i]+".png")
                    else:
                        fig.savefig("../figures/ACRoBEAR/allRegionsPDFs/pdf_"+var_shortname[var]+"_"+model1+"_ssp"+scenario1+"_"+model2+"_ssp"+scenario2+"_"+season_shortname[i]+".png")
                else:
                    if after2070_1 == True:
                        fig.savefig("../figures/OtherRegions/allRegionsPDFs/pdf_"+var_shortname[var]+"_"+model1+"_ssp"+scenario1+"_after2070_"+model2+"_ssp"+scenario2+"_"+regions_names[k]+"_"+season_shortname[i]+".png")
                    elif after2070_2 == True:
                        fig.savefig("../figures/OtherRegions/allRegionsPDFs/pdf_"+var_shortname[var]+"_"+model1+"_ssp"+scenario1+"_"+model2+"_ssp"+scenario2+"_after2070_"+regions_names[k]+"_"+season_shortname[i]+".png")
                    else:
                        fig.savefig("../figures/OtherRegions/allRegionsPDFs/pdf_"+var_shortname[var]+"_"+model1+"_ssp"+scenario1+"_"+model2+"_ssp"+scenario2+"_"+regions_names[k]+"_"+season_shortname[i]+".png")

            plt.clf()

