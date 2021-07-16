import numpy as np
import xarray as xr

# This program checks datasets of a given variable for non-finite numbers
# or unrealistic numbers. It replaces all of these values with NaN,
# and creates a new dataset with all ensemble members combined.
# It requires that the dataset filename is on the same form as seen below. 

#-Variable specifications------------------------------------------------------

model = "MPI-ESM1-2-LR"     # Which model are you using?
scenario = "126"            # Which shared socio-economic pathway are you using?
nmemb = 10                  # How many ensemble member are you using?
var_name = "tasmax"         # Which variable are you using?

#-------------------------------------------------------------------------------

fn = var_name+"_"+model+"_historical_ssp"+scenario+"_memb"+str(nmemb)+".nc"

print("Ensemble member 1:")

historical = xr.open_dataset("../CMIP6/"+var_name+"_day_"+model+"_historical_r1i1p1f1_18500101-20141231.nc")
ssp = xr.open_dataset("../CMIP6/"+var_name+"_day_"+model+"_ssp"+scenario+"_r1i1p1f1_20150101-21001231.nc")

# Concatenate the historical years and scenario years of first ensemble member

ds = xr.concat([historical, ssp], "time")

# The variable mrso had so many non-finite number that the replacement had to be done one-by-one in a loop
if var_name == "mrso":
    ds_array = np.array(ds[var_name])

falseFinite = np.where(np.isfinite(ds[var_name])==False)    # Indices where array element is not a finite number
highNumber = np.where(abs(ds[var_name]) >= 1e20)            # Indices where absolute value of array element is very high

Nmv1 = len(falseFinite[0])
Nmv2 = len(highNumber[0])

# Go through indices and replace with NaN

if Nmv1 != 0:
    
    if var_name == "mrso":
        for k in range(Nmv1):
        
            n = falseFinite[0][k]
            j = falseFinite[1][k]
            i = falseFinite[2][k]
            ds_array[n,j,i] = np.nan
    else:
        ds[var_name][falseFinite] = np.nan

    print(Nmv1," missing values found!")

elif Nmv2 != 0:
        
    if var_name == "mrso":
        for k in range(Nmv2):
    
            n = highNumber[0][k]
            j = highNumber[1][k]
            i = highNumber[2][k]
            ds_array[n,j,i] = np.nan
    else:
        ds[var_name][highNumber] = np.nan

    print(Nmv2," missing values found!")

else:

    print("No missing values found!\n")

if var_name == "mrso":
    ds.assign(var_name = (('time','lat','lon'),ds_array))

# Repeat for other ensemble members and concatenate these together with the others

for memb in range(2,nmemb+1):

    print("Ensemble member ",memb,":")
    
    historical = xr.open_dataset("../CMIP6/"+var_name+"_day_"+model+"_historical_r"+str(memb)+"i1p1f1_18500101-20141231.nc")
    ssp = xr.open_dataset("../CMIP6/"+var_name+"_day_"+model+"_ssp"+scenario+"_r"+str(memb)+"i1p1f1_20150101-21001231.nc")

    comb = xr.concat([historical, ssp], "time")

    falseFinite = np.where(np.isfinite(comb[var_name])==False)
    highNumber = np.where(abs(comb[var_name]) >= 1e20)

    Nmv1 = len(falseFinite[0])
    Nmv2 = len(highNumber[0])
    
    if var_name == "mrso":
        ds_array = np.array(comb[var_name])

    if Nmv1 != 0:

        if var_name == "mrso":
            for k in range(Nmv1):
                n = falseFinite[0][k]
                j = falseFinite[1][k]
                i = falseFinite[2][k]
                ds_array[n,j,i] = np.nan
        else:
            comb[var_name][falseFinite] = np.nan

        print(Nmv1," missing values found!")
    
    elif Nmv2 != 0:
        
        if var_name == "mrso":
            for k in range(Nmv2):
                n = highNumber[0][k]
                j = highNumber[1][k]
                i = highNumber[2][k]
                ds_array[n,j,i] = np.nan
        else:
            comb[var_name][highNumber] = np.nan

        print(Nmv2," missing values found!")

    else:

        print("No missing values found!\n")

    if var_name == "mrso":
        comb.assign(var_name = (('time','lat','lon'),ds_array))

    ds = xr.concat([ds,comb],"memb")

# Save dataset

ds.to_netcdf("../outputdata/"+fn, "w",format="NETCDF4")
