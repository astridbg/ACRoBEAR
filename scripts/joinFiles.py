import xarray as xr
import glob
import os
hist_date = "18500101-20141231"
ssp_date = "20150101-21001231"

# This is a program that joins time slices of one experiment into
# one large dataset.

#-Variable specifications----------------------------------------
model = "MPI-ESM1-2-LR"
experiment = "historical"
date = hist_date
variable = "tasmax"
nmemb = 1
#----------------------------------------------------------------

folderpath = "../../../CMIP6/CMIP6_downloads/MPI-ESM1-2-LR/"
for memb in range(nmemb):
    filepaths = variable+"_day_"+model+"_"+experiment+"_r"+str(memb+1)+"i1p1f1_gn_*"

    files =  glob.glob(os.path.join(folderpath,filepaths))
    files.sort()

    ds = xr.open_dataset(files[0])

    for fil in files[1:]:
        ds_new = xr.open_dataset(fil)
        ds = xr.concat([ds,ds_new],dim="time")
    
    ds.to_netcdf("../CMIP6/"+variable+"_day_"+model+"_"+experiment+"_r"+str(memb+1)+"i1p1f1_"+date+".nc")


