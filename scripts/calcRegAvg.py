import numpy as np
import math
import xarray as xr
import netCDF4 as nc
from makeRegion import makeRegion
from makeAreagrid import makeAreagrid

var_names = ['tas','ts','pr','uas', 'vas','mrso']
var_units = ['K','K','kg m-2 s-2','m s-1','m s-1','kg m-2']
var_list = [2]
model = "MPI-ESM1-2-LR"
scenario = '585'
after2070 = False
GWLs = [0, 1, 1.5, 2, 3,4]
reg_name = 'All'

regAreagrid = xr.open_dataset("../regions/regAreagrid_"+model+"_"+reg_name+".nc")
nreg = len(regAreagrid.region)

print("Regions found")

gmst = xr.open_dataset("../outputdata/gmst_"+model+"_ssp"+scenario+".nc")

nGWLs = len(GWLs)
nmemb = len(gmst.ensmemb)

warmlvls = np.zeros((nmemb, nGWLs, 2))

def find_nearest_index(array, value):
    
    array = np.asarray(array)
    idx = np.nanargmin(np.abs(array - value))

    return idx

for memb in range(nmemb):

    warmlvls[memb,0,0] = 0
    warmlvls[memb,0,1] = 20

    baseline = np.mean(gmst.tas.isel(ensmemb=memb)[:20])

    deltaT = gmst.tas.isel(ensmemb=memb)-baseline

    twentyyrmean = deltaT.rolling(time=20,center=True).mean()
 
    for l in range(1,nGWLs):
        
        if after2070 == True:
            
            if GWLs[l] == 1.5:
                
                idx_after2070 = find_nearest_index(twentyyrmean.sel(time=slice(2070,2101)),GWLs[l])
                idx = 2070-1850+idx_after2070 
            
            else:

                idx = find_nearest_index(twentyyrmean,GWLs[l])
        else:
            
            idx = find_nearest_index(twentyyrmean,GWLs[l])

        warmlvls[memb,l,0] = idx - 10
        warmlvls[memb,l,1] = idx + 10

print("Warming levels found")

fns = ['pi','plus1','plus1-5','plus2', 'plus3','plus4']

if model == "CanESM5":
    yrlen = 365
else:
    yrlen = 365.25

for i in var_list:
    
    var_name = var_names[i]
    var_unit = var_units[i]
    dataset = xr.open_dataset("../outputdata/"+var_name+"_"+model+"_historical_ssp"+scenario+"_memb"+str(nmemb)+".nc")
    da = dataset[var_name]
    print("Variable: ",var_name)


    for l in range(1):
    
        if GWLs[l]==1.5 and after2070==True:
            fn = "../outputdata/"+var_name+"_"+fns[l]+"_"+model+"_ssp"+scenario+"_after2070_reg"+reg_name+".nc"
        else:
            fn = "../outputdata/"+var_name+"_"+fns[l]+"_"+model+"_ssp"+scenario+"_reg"+reg_name+".nc"

        ds = nc.Dataset(fn, 'w', format='NETCDF4')

        dayofyear = ds.createDimension('dayofyear', 365)
        year = ds.createDimension('year', 20*nmemb)
        region = ds.createDimension('region', nreg)

        daysofyear = ds.createVariable('dayofyear', 'i4', ('dayofyear',))
        years = ds.createVariable('year', 'i4', ('year',))
        regions = ds.createVariable('region','i4',('region',))

        daysofyear[:] = np.arange(1,366,1)
        years[:] = np.arange(1,20*nmemb+1,1)
        regions[:] = np.arange(1,nreg+1,1)

        value = ds.createVariable(var_name, 'f4', ('dayofyear','year','region'))
        value.units = var_unit

        for k in range(nreg):
        
            Region = np.array(regAreagrid.mask.isel(region=k))
    
            for memb in range(nmemb):

                start = math.floor(warmlvls[memb,l,0]*yrlen)
                stop = math.floor(warmlvls[memb,l,1]*yrlen)
                print(stop)
                print(len(da.time))
                gwl_data = da.isel(time=slice(start,stop),memb=memb)

                for yr in range(20):

                    print("Global warming level:",str(GWLs[l]),"degrees C,  Region number:", k+1,", Ensemble member: ", memb+1, ", Year: ",yr+1)

                    for day in range(365):

                        gwlyear_idx = memb*20+yr
                        time_idx = math.floor(yr*yrlen)+day

                        value[day,gwlyear_idx,k] = np.nansum(gwl_data[time_idx,:,:]*Region) / np.nansum(Region)
            
                # print("Start: ",np.array(histssp5.time[start]),", Stop: ",np.array(histssp5.time[stop]), ", Last day: ", np.array(histssp5.time[start+time_idx]))
   
        ds.close()

