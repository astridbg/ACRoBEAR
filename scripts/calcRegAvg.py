import numpy as np
import math
import xarray as xr
import netCDF4 as nc
from makeRegion import makeRegion
from makeAreagrid import makeAreagrid


regAreagrid = xr.open_dataset("../regions/regAreagrid_all.nc")
nreg = len(regAreagrid.region)

print("Regions found")

gmst = xr.open_dataset("../outputdata/gmst.nc")

Tlevels = [1, 1.5, 2, 3, 4]
nTlev = len(Tlevels)
nmemb = len(gmst.ensmemb)

warmlvls = np.zeros((nmemb, nTlev+1, 2))

def find_nearest_index(array, value):
    
    array = np.asarray(array)
    idx = np.nanargmin(np.abs(array - value))

    return idx

for i in range(nmemb):

    warmlvls[i,0,0] = 0
    warmlvls[i,0,1] = 20

    baseline = np.mean(gmst.tas.isel(ensmemb=i)[:20])

    deltaT = gmst.tas.isel(ensmemb=i)-baseline

    twentyyrmean = deltaT.rolling(time=20,center=True).mean()
 
    for l in range(len(Tlevels)):

        idx = find_nearest_index(twentyyrmean,Tlevels[l])

        warmlvls[i,l+1,0] = idx - 10
        warmlvls[i,l+1,1] = idx + 10

print("Warming levels found")

model_scenario = xr.open_dataset("../outputdata/histssp5_allmembs.nc")
data = model_scenario.tas
var_name = 'tas'
var_unit = 'K'

fns = ['preInd','plus1','plus1_5','plus2', 'plus3','plus4']

for l in range(3,5):

    fn = "../outputdata/"+fns[l]+"_allreg.nc"
    ds = nc.Dataset(fn, 'w', format='NETCDF4')

    dayofyear = ds.createDimension('dayofyear', 365)
    year = ds.createDimension('year', 200)
    region = ds.createDimension('region', nreg)

    daysofyear = ds.createVariable('dayofyear', 'i4', ('dayofyear',))
    years = ds.createVariable('year', 'i4', ('year',))
    regions = ds.createVariable('region','i4',('region',))

    daysofyear[:] = np.arange(1,366,1)
    years[:] = np.arange(1,201,1)
    regions[:] = np.arange(1,nreg+1,1)

    value = ds.createVariable(var_name, 'f4', ('dayofyear','year','region'))
    value.units = var_unit

    for k in range(nreg):
        
        Region = np.array(regAreagrid.mask.isel(region=k))
    
        for i in range(nmemb):

            start = math.floor(warmlvls[i,l,0]*365.25)
            stop = math.floor(warmlvls[i,l,1]*365.25)

            gwl_data = data.isel(time=slice(start,stop),memb=i)
            
            for yr in range(20):

                print("Global warming level: ",str(Tlevels[l])," degrees C, Region number:", k+1,", Ensemble member: ", i+1, ", Year: ",yr+1)

                for day in range(365):

                    gwlyear_idx = i*20+yr
                    time_idx = math.floor(yr*365.25)+day

                    value[day,gwlyear_idx,k] = np.nansum(gwl_data[time_idx,:,:]*Region) / np.nansum(Region)
            
           # print("Start: ",np.array(histssp5.time[start]),", Stop: ",np.array(histssp5.time[stop]), ", Last day: ", np.array(histssp5.time[start+time_idx]))
   
    ds.close()

