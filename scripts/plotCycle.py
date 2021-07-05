import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 12})

var_shortname = ['tas','pr']
var_longname = ['Surface temperature','Precipitation']
var_unit = ['$^{\circ}$C','mm d$^{-1}$']

for var in range(2):
    preInd = xr.open_dataset("../outputdata/pi_"+var_shortname[var]+"_regAll.nc")
    plus1 = xr.open_dataset("../outputdata/plus1_"+var_shortname[var]+"_regAll.nc")
    plus1_5 = xr.open_dataset("../outputdata/plus1-5_"+var_shortname[var]+"_regAll.nc")
    plus2 = xr.open_dataset("../outputdata/plus2_"+var_shortname[var]+"_regAll.nc")
    plus3 = xr.open_dataset("../outputdata/plus3_"+var_shortname[var]+"_regAll.nc")
    plus4 = xr.open_dataset("../outputdata/plus4_"+var_shortname[var]+"_regAll.nc")

    dayofyear = preInd.dayofyear
    nreg = len(preInd.region)

    if var == 0:
        preInd[var_shortname[var]] -= 273.15
        plus1[var_shortname[var]] -= 273.15
        plus1_5[var_shortname[var]] -= 273.15
        plus2[var_shortname[var]] -= 273.15
        plus3[var_shortname[var]] -= 273.15
        plus4[var_shortname[var]] -= 273.15

    elif var == 1:
        preInd[var_shortname[var]] *= 86400
        plus1[var_shortname[var]] *= 86400
        plus1_5[var_shortname[var]] *= 86400
        plus2[var_shortname[var]] *= 86400
        plus3[var_shortname[var]] *= 86400
        plus4[var_shortname[var]] *= 86400


    pi_annavg = preInd[var_shortname[var]].mean("year")
    pi_min = preInd[var_shortname[var]].min("year")
    pi_max = preInd[var_shortname[var]].max("year")

    p2_annavg = plus2[var_shortname[var]].mean("year")
    p2_min = plus2[var_shortname[var]].min("year")
    p2_max = plus2[var_shortname[var]].max("year")

    #pi_annspread = preInd[var_shortname[var]].std("year")
    #p2_annspread = plus2[var_shortname[var]].std("year")

    fname = ["alaska","canada","fscand","wsib","esib","us","ea","eu","arc","afr","sam","sane","china","india","land"]
    name = ["Alaska", "Canada", "Fennoscandia", "West Siberia", "East Siberia","the USA","East Asia","Europe","the Arctic","Africa","South America","Sane","China", "India","global land areas"]

    fig = plt.figure(figsize=(10,5))

    for i in range(nreg):

        fig.suptitle("Mean and spread of annual cycle of "+name[i])
    
        fig.add_subplot(121)
        plt.hlines(y=0,  xmin=0, xmax=365, linestyle="--",color="grey")
        plt.scatter(dayofyear,pi_annavg.isel(region=i),s=5,color="black",label="Preindustrial")
        plt.scatter(dayofyear,pi_min.isel(region=i),s=1,color="black")
        plt.scatter(dayofyear,pi_max.isel(region=i),s=1,color="black")
        #plt.scatter(dayofyear,pi_annavg.isel(region=i)+pi_annspread.isel(region=i),s=1, color="black")
        #plt.scatter(dayofyear,pi_annavg.isel(region=i)-pi_annspread.isel(region=i),s=1,color="black")
        plt.scatter(dayofyear,p2_annavg.isel(region=i),s=5,color="green",label=r"+2$^{\circ}$C")
        plt.scatter(dayofyear,p2_min.isel(region=i),s=1,color="green")
        plt.scatter(dayofyear,p2_max.isel(region=i),s=1,color="green")
        #plt.scatter(dayofyear,p2_annavg.isel(region=i)+p2_annspread.isel(region=i),s=1, color="green")
        #plt.scatter(dayofyear,p2_annavg.isel(region=i)-p2_annspread.isel(region=i),s=1,color="green")
        plt.xlabel("Day")
        plt.xticks([100, 200, 300], ['100','200','300'])
        plt.ylabel(var_longname[var]+" ["+var_unit[var]+"]")
        #plt.legend(loc="lower right")
        plt.grid()
    
        fig.add_subplot(122)
        plt.scatter(dayofyear,pi_annavg.isel(region=i)-pi_annavg.isel(region=i),s=5,color="black",label="Preindustrial")
        plt.scatter(dayofyear,pi_min.isel(region=i)-pi_annavg.isel(region=i),s=1,color="black")
        plt.scatter(dayofyear,pi_max.isel(region=i)-pi_annavg.isel(region=i),s=1,color="black")
        #plt.scatter(dayofyear,pi_annspread.isel(region=i),s=1, color="black")
        #plt.scatter(dayofyear,-pi_annspread.isel(region=i),s=1,color="black")
        plt.scatter(dayofyear,p2_annavg.isel(region=i)-pi_annavg.isel(region=i),s=5,color="green",label=r"+2$^{\circ}$C")
        plt.scatter(dayofyear,p2_min.isel(region=i)-pi_annavg.isel(region=i),s=1,color="green")
        plt.scatter(dayofyear,p2_max.isel(region=i)-pi_annavg.isel(region=i),s=1,color="green")
        #plt.scatter(dayofyear,p2_annavg.isel(region=i)-pi_annavg.isel(region=i)+p2_annspread.isel(region=i),s=1, color="green")
        #plt.scatter(dayofyear,p2_annavg.isel(region=i)-pi_annavg.isel(region=i)-p2_annspread.isel(region=i),s=1,color="green")
        plt.xlabel("Day")
        plt.xticks([100, 200, 300], ['100','200','300'])
        plt.ylabel(var_longname[var]+" change"+" ["+var_unit[var]+"]")
        #plt.yticks(np.arange(-20,21,5), ['-20','-15','-10','-5','0','5','10','15','20'])
        plt.legend(loc="lower right")
        plt.grid()

        fig.tight_layout()
        if i < 5:
            fig.savefig("../figures/ACRoBEAR/annualCycles/cycle_"+var_shortname[var]+"_"+fname[i]+".png")
        else:
            fig.savefig("../figures/OtherRegions/annualCycles/cycle_"+var_shortname[var]+"_"+fname[i]+".png")

        plt.clf()
