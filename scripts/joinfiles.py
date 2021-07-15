import xarray as xr
import glob
import os

folderpath = "../../../CMIP6/CMIP6_downloads/MPI-ESM1-2-LR/"
filepaths = "tasmax_day_MPI-ESM1-2-LR_ssp585_r1i1p1f1_gn_*"

files =  glob.glob(os.path.join(folderpath,filepaths))
files.sort()
print(files)

ds = xr.open_dataset(files[0])

for fil in files[1:]:
    ds_new = xr.open_dataset(fil)
    ds = xr.combine_by_coords([ds,ds_new])
    
ds.to_netcdf("../CMIP6/tasmax_day_MPI-ESM1-2-LR_ssp585_r1i1p1f1_gn_20150101-21001231.nc")

print(ds.time)
