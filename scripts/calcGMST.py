import xarray as xr
import numpy as np
import math
from gv3 import gv3
import netCDF4 as nc


historical = xr.open_dataset("../CMIP6/tas_day_MPI-ESM1-2-LR_historical_r1i1p1f1_18500101-20141231.nc")
ssp585 = xr.open_dataset("../CMIP6/tas_day_MPI-ESM1-2-LR_ssp585_r1i1p1f1_20150101-21001231.nc")

lon_values = historical.lon
lat_values = historical.lat

nlon = len(lon_values)
nlat = len(lat_values)
nhist = math.floor(len(historical.time)/365.0)
nssp585 = math.floor(len(ssp585.time)/365.0)
print("Historical years: ",nhist,", Scenario years: ",nssp585)

fn = "../outputdata/gmst.nc"
ds = nc.Dataset(fn, 'w', format='NETCDF4')

time = ds.createDimension('time', nhist+nssp585)
ensmemb = ds.createDimension('ensmemb', 10)
times = ds.createVariable('time', 'int', ('time',))
ensmembs = ds.createVariable('ensmemb', 'int', ('ensmemb',))
times[:] = np.arange(1850, 2101, 1)
ensmembs[:] = np.arange(1,11,1)
value = ds.createVariable('tas', 'f4', ('time','ensmemb'))
value.units = 'K'

annavg = np.zeros((nlat,nlon))
spatavg = np.zeros(nhist+nssp585)

for r in range(1,11):
    historical = xr.open_dataset("../CMIP6/tas_day_MPI-ESM1-2-LR_historical_r"+str(r)+"i1p1f1_18500101-20141231.nc")
    ssp585 = xr.open_dataset("../CMIP6/tas_day_MPI-ESM1-2-LR_ssp585_r"+str(r)+"i1p1f1_20150101-21001231.nc")


    for yr in range(nhist):
        start = math.floor(yr*365)
        stop = math.floor((yr+1)*365)
        annavg[:,:] = historical.tas.isel(time=slice(start,stop)).mean('time')
        spatavg[yr] = gv3(annavg[:,:], lon_values, lat_values)

    for yr in range(nssp585):
        start = math.floor(yr*365)
        stop = math.floor((yr+1)*365)
        annavg[:,:] = ssp585.tas.isel(time=slice(start,stop)).mean('time')
        spatavg[nhist+yr] = gv3(annavg[:,:], lon_values, lat_values)
    
    value[:,r-1] = spatavg


ds.close()
