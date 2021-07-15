import xarray as xr
import numpy as np
import math
from gv3 import gv3
import netCDF4 as nc

model = "CanESM5"
scenario = "126"
nmemb = 25

historical = xr.open_dataset("../CMIP6/tas_day_"+model+"_historical_r1i1p1f1_gn_18500101-20141231.nc")
ssp = xr.open_dataset("../CMIP6/tas_day_"+model+"_ssp"+scenario+"_r1i1p1f1_gn_20150101-21001231.nc")

lon_values = historical.lon
lat_values = historical.lat

nlon = len(lon_values)
nlat = len(lat_values)
nhist = math.floor(len(historical.time)/365.0)
nssp = math.floor(len(ssp.time)/365.0)
print("Historical years: ",nhist,", Scenario years: ",nssp)

fn = "../outputdata/gmst_"+model+"_ssp"+scenario+".nc"
ds = nc.Dataset(fn, 'w', format='NETCDF4')

time = ds.createDimension('time', nhist+nssp)
ensmemb = ds.createDimension('ensmemb', nmemb)
times = ds.createVariable('time', 'int', ('time',))
ensmembs = ds.createVariable('ensmemb', 'int', ('ensmemb',))
times[:] = np.arange(1850, 2101, 1)
ensmembs[:] = np.arange(1,nmemb+1,1)
value = ds.createVariable('tas', 'f4', ('time','ensmemb'))
value.units = 'K'

annavg = np.zeros((nlat,nlon))
spatavg = np.zeros(nhist+nssp)

for memb in range(1,nmemb+1):
    
    print("Ensemble member: ", memb)

    historical = xr.open_dataset("../CMIP6/tas_day_"+model+"_historical_r"+str(memb)+"i1p1f1_gn_18500101-20141231.nc")
    ssp = xr.open_dataset("../CMIP6/tas_day_"+model+"_ssp"+scenario+"_r"+str(memb)+"i1p1f1_gn_20150101-21001231.nc")


    for yr in range(nhist):
        start = math.floor(yr*365)
        stop = math.floor((yr+1)*365)
        annavg[:,:] = historical.tas.isel(time=slice(start,stop)).mean('time')
        spatavg[yr] = gv3(annavg[:,:], lon_values, lat_values)

    for yr in range(nssp):
        start = math.floor(yr*365)
        stop = math.floor((yr+1)*365)
        annavg[:,:] = ssp.tas.isel(time=slice(start,stop)).mean('time')
        spatavg[nhist+yr] = gv3(annavg[:,:], lon_values, lat_values)
    
    value[:,memb-1] = spatavg


ds.close()
