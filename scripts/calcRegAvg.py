import numpy as np
import math
import xarray as xr
import netCDF4 as nc
from makeRegion import makeRegion
from makeAreagrid import makeAreagrid

lf = xr.open_dataset("../regions/landfrac_MPI-ESM1-2.nc")
lon_values = lf.lon
lat_values = lf.lat
landfrac = lf.landfrac[0] * 0.0001

r_alaska = makeRegion(lon_values, lat_values, [200,230,58,72])  # Alaska
r_canada = makeRegion(lon_values, lat_values, [235,280,52,68])  # Canada
r_fscand = makeRegion(lon_values, lat_values, [4,35,57,72])     # Fennoscandia
r_wsib = makeRegion(lon_values, lat_values, [45,95,57,72])      # Western Siberia
r_esib = makeRegion(lon_values, lat_values, [95,145,57,72])     # Eastern Siberia

alaska = makeAreagrid(lon_values, lat_values, landfrac*r_alaska)
canada = makeAreagrid(lon_values, lat_values, landfrac*r_canada)
fscand = makeAreagrid(lon_values, lat_values, landfrac*r_fscand)
wsib = makeAreagrid(lon_values, lat_values, landfrac*r_wsib)
esib = makeAreagrid(lon_values, lat_values, landfrac*r_esib)

region_list = [alaska, canada, fscand, wsib, esib]
nreg = len(region_list)

print("Regions found")

gmst = xr.open_dataset("../outputdata/gmst.nc")

Tlevels = [1, 2, 3, 4]
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

histssp5 = xr.open_dataset("../outputdata/histssp5_allmembs.nc")

fns = ['preInd','plus1','plus2', 'plus3','plus4']

for l in range(3,5):

    fn = "../outputdata/"+fns[l]+".nc"
    ds = nc.Dataset(fn, 'w', format='NETCDF4')

    dayofyear = ds.createDimension('dayofyear', 365)
    year = ds.createDimension('year', 200)
    region = ds.createDimension('region', 5)

    daysofyear = ds.createVariable('dayofyear', 'i4', ('dayofyear',))
    years = ds.createVariable('year', 'i4', ('year',))
    regions = ds.createVariable('region','i4',('region',))

    daysofyear[:] = np.arange(1,366,1)
    years[:] = np.arange(1,201,1)
    regions[:] = np.arange(1,6,1)

    value = ds.createVariable('tas', 'f4', ('dayofyear','year','region'))
    value.units = 'K'

    for k in range(5):

        Region = region_list[k]
    
        for i in range(nmemb):

            start = math.floor(warmlvls[i,l,0]*365.25)
            stop = math.floor(warmlvls[i,l,1]*365.25)

            gwl_tas = histssp5.tas.isel(time=slice(start,stop),memb=i)
            
            for yr in range(20):

                print("Region number:", k+1,", Ensemble member: ", i+1, ", Year: ",yr+1)

                for day in range(365):

                    gwlyear_idx = i*20+yr
                    time_idx = math.floor(yr*365.25)+day

                    value[day,gwlyear_idx,k] = np.nansum(gwl_tas[time_idx,:,:]*Region) / np.nansum(Region)
            
           # print("Start: ",np.array(histssp5.time[start]),", Stop: ",np.array(histssp5.time[stop]), ", Last day: ", np.array(histssp5.time[start+time_idx]))
   
    ds.close()

