import numpy as np
import xarray as xr

var_name = "mrso"
scenario = "ssp585"

fn = var_name+"_historical_"+scenario+"_rAll.nc"

print("Ensemble member 1:")

historical = xr.open_dataset("../CMIP6/"+var_name+"_day_MPI-ESM1-2-LR_historical_r1i1p1f1_18500101-20141231.nc")
ssp = xr.open_dataset("../CMIP6/"+var_name+"_day_MPI-ESM1-2-LR_"+scenario+"_r1i1p1f1_20150101-21001231.nc")

ds = xr.concat([historical, ssp], "time")
print("Done with concatination")

Nmv1 = len(np.where(np.isfinite(ds[var_name])==False)[0])
Nmv2 = len(np.where(abs(ds[var_name]) >= 1e20)[0])

if Nmv1 != 0:

   # ds[var_name][np.where(np.isfinite(ds[var_name])==False)] = np.nan
    for k in range(Nmv1):
        
        n = np.where(np.isfinite(ds[var_name])==False)[0][k]
        j = np.where(np.isfinite(ds[var_name])==False)[1][k]
        i = np.where(np.isfinite(ds[var_name])==False)[2][k]
        ds[var_name][n,j,i] = np.nan
    
    print(Nmv1," missing values found!")

elif Nmv2 != 0:
        
    #ds[var_name][np.where(abs(ds[var_name]) >= 1e20)[0]] = np.nan
    for k in range(Nmv2):
        n = np.where(abs(ds[var_name])>=1e20)[0][k]
        j = np.where(abs(ds[var_name])>=1e20)[1][k]
        i = np.where(abs(ds[var_name])>=1e20)[2][k]
        ds[var_name][n,j,i] = np.nan

    print(Nmv2," missing values found!")

else:

    print("No missing values found!\n")


for i in range(2,11):

    print("Ensemble member ",i,":")

    historical = xr.open_dataset("../CMIP6/"+var_name+"_day_MPI-ESM1-2-LR_historical_r"+str(i)+"i1p1f1_18500101-20141231.nc")
    ssp = xr.open_dataset("../CMIP6/"+var_name+"_day_MPI-ESM1-2-LR_"+scenario+"_r"+str(i)+"i1p1f1_20150101-21001231.nc")
    comb = xr.concat([historical, ssp], "time")

    Nmv1 = len(np.where(np.isfinite(comb[var_name])==False)[0])
    Nmv2 = len(np.where(abs(comb[var_name]) >= 1e20)[0])

    if Nvm1 != 0:

       # comb[var_name][np.where(np.isfinite(ds[var_name])==False)] = np.nan
        
        for k in range(Nmv1):
            n = np.where(np.isfinite(comb[var_name])==False)[0][k]
            j = np.where(np.isfinite(comb[var_name])==False)[1][k]
            i = np.where(np.isfinite(comb[var_name])==False)[2][k]
            comb[var_name][n,j,i] = np.nan

        print(Nmv1," missing values found!")
    
    elif Nmv2 != 0:
        
        #comb[var_name][np.where(abs(ds[var_name]) >= 1e20)] = np.nan
        
        for k in range(Nmv2):
            n = np.where(abs(comb[var_name])>=1e20)[0][k]
            j = np.where(abs(comb[var_name])>=1e20)[1][k]
            i = np.where(abs(comb[var_name])>=1e20)[2][k]
            comb[var_name][n,j,i] = np.nan

        print(Nmv2," missing values found!")

    else:

        print("No missing values found!\n")
    
    ds = xr.concat([ds,comb],"memb")

ds.to_netcdf("../outputdata/"+fn, "w",format="NETCDF4")


print("New dataset time:\n",ds.time)
print("New dataset ensemble members:\n",ds.memb)
