import numpy as np
import xarray as xr

var_name = "ts"
scenario = "ssp585"

fn = var_name+"_historical_"+scenario+"_rAll.nc"

print("Ensemble member 1:")

historical = xr.open_dataset("../CMIP6/"+var_name+"_Eday_MPI-ESM1-2-LR_historical_r1i1p1f1_18500101-20141231.nc")
ssp = xr.open_dataset("../CMIP6/"+var_name+"_Eday_MPI-ESM1-2-LR_"+scenario+"_r1i1p1f1_20150101-21001231.nc")

ds = xr.concat([historical, ssp], "time")


if len(np.where(np.isfinite(ds[var_name])==False)[0]) != 0:

    ds[var_name][np.where(np.isfinite(ds[var_name])==False)] = np.nan
        
    print(len(np.where(np.isfinite(ds[var_name])==False)[0])," missing values found!")

    
elif len(np.where(abs(ds[var_name]) >= 1e20)[0]) != 0:
        
    ds[var_name][np.where(abs(ds[var_name]) >= 1e20)] = np.nan

    print(len(np.where(abs(ds[var_name]) >= 1e20)[0]), " missing values found!")

else:

    print("No missing values found!\n")


for i in range(2,11):

    print("Ensemble member ",i,":")

    historical = xr.open_dataset("../CMIP6/"+var_name+"_Eday_MPI-ESM1-2-LR_historical_r"+str(i)+"i1p1f1_18500101-20141231.nc")
    ssp = xr.open_dataset("../CMIP6/"+var_name+"_Eday_MPI-ESM1-2-LR_"+scenario+"_r"+str(i)+"i1p1f1_20150101-21001231.nc")
    comb = xr.concat([historical, ssp], "time")


    if len(np.where(np.isfinite(ds[var_name])==False)[0]) != 0:

        comb[var_name][np.where(np.isfinite(ds[var_name])==False)] = np.nan
        
        print(len(np.where(np.isfinite(ds[var_name])==False)[0])," missing values found!")
    
    elif len(np.where(abs(ds[var_name]) >= 1e20)[0]) != 0:
        
        comb[var_name][np.where(abs(ds[var_name]) >= 1e20)] = np.nan

        print(len(np.where(abs(ds[var_name]) >= 1e20)[0]), " missing values found!")

    else:

        print("No missing values found!\n")
    
    ds = xr.concat([ds,comb],"memb")

ds.to_netcdf("../outputdata/"+fn, "w",format="NETCDF4")


print("New dataset time:\n",ds.time)
print("New dataset ensemble members:\n",ds.memb)
