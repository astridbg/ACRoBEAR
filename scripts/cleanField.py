import numpy as np
import xarray as xr

fn = "histssp5_allmembs.nc"

print("Ensemble member 1:")

historical = xr.open_dataset("../CMIP6/tas_day_MPI-ESM1-2-LR_historical_r1i1p1f1_18500101-20141231.nc")
ssp585 = xr.open_dataset("../CMIP6/tas_day_MPI-ESM1-2-LR_ssp585_r1i1p1f1_20150101-21001231.nc")
ds = xr.concat([historical, ssp585], "time")


if len(np.where(np.isfinite(ds.tas)==False)[0]) != 0:

    ds.tas[np.where(np.isfinite(ds.tas)==False)] = np.nan
        
    print(len(np.where(np.isfinite(ds.tas)==False)[0])," missing values found!")

    
elif len(np.where(abs(ds.tas) >= 1e20)[0]) != 0:
        
    ds.tas[np.where(abs(ds.tas) >= 1e20)] = np.nan

    print(len(np.where(abs(ds.tas) >= 1e20)[0]), " missing values found!")

else:

    print("No missing values found!\n")


for i in range(2,11):

    print("Ensemble member ",i,":")

    historical = xr.open_dataset("../CMIP6/tas_day_MPI-ESM1-2-LR_historical_r"+str(i)+"i1p1f1_18500101-20141231.nc")
    ssp585 = xr.open_dataset("../CMIP6/tas_day_MPI-ESM1-2-LR_ssp585_r"+str(i)+"i1p1f1_20150101-21001231.nc")
    comb = xr.concat([historical, ssp585], "time")


    if len(np.where(np.isfinite(ds.tas)==False)[0]) != 0:

        comb.tas[np.where(np.isfinite(ds.tas)==False)] = np.nan
        
        print(len(np.where(np.isfinite(ds.tas)==False)[0])," missing values found!")
    
    elif len(np.where(abs(ds.tas) >= 1e20)[0]) != 0:
        
        comb.tas[np.where(abs(ds.tas) >= 1e20)] = np.nan

        print(len(np.where(abs(ds.tas) >= 1e20)[0]), " missing values found!")

    else:

        print("No missing values found!\n")
    
    ds = xr.concat([ds,comb],"memb")

ds.to_netcdf("../outputdata/"+fn, "w",format="NETCDF4")


print(ds.time)
print(ds.memb)
