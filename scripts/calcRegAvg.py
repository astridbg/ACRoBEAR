import numpy as np
import math
import xarray as xr
import netCDF4 as nc
from makeRegion import makeRegion
from makeAreagrid import makeAreagrid

# This scripts creates a regional average of daily climate in different  warming levels for a given region

#-Variable specifications---------------------------------------------------------------------------------

model = "CanESM5"               # Which model are you using?
scenario = '585'                # Which scenario are you using?
GWLs = [0, 1, 1.5, 2, 3, 4]     # Which global warming levels (GWLs) are included?
after2070 = False               # Are you looking at the GWL after 2070? (Applicable to GWL 1.5 in SSP126)
reg_name = 'All'                # What is the postfix of the areagrid file you are using (which regions)?

var_list = [2]                  # Which variables are you looking at (indices of var_names, ex. 0 -> 'tas')?
gwl_list = [2]                  # Which GWLs are you calculating (indices of GWLs, ex. 2 -> 1.5)?

#----------------------------------------------------------------------------------------------------------

var_names = ['tas','ts','pr','uas', 'vas','mrso','tasmax']          # Variable names
var_units = ['K','K','kg m-2 s-2','m s-1','m s-1','kg m-2','K']     # Variable units

#----------------------------------------------------------------------------------------------------------

# Get the areagrid file of hte regions you are looking at

regAreagrid = xr.open_dataset("../regions/regAreagrid_"+model+"_"+reg_name+".nc")
nreg = len(regAreagrid.region)

print("Regions found")

# Get the global annual mean surface temperature of the scenario you are looking at

gmst = xr.open_dataset("../outputdata/gmst_"+model+"_ssp"+scenario+".nc")

nGWLs = len(GWLs)
nmemb = len(gmst.ensmemb)

# Find the indices of the global warming levels you are looking at for each ensemble member, and store them
# Use the find_nearest index function to find the index of the global warming level

warmlvls = np.zeros((nmemb, nGWLs, 2))

def find_nearest_index(array, value):
    
    # Find nearest index to value in array

    array = np.asarray(array)
    idx = np.nanargmin(np.abs(array - value))

    return idx

for memb in range(nmemb):
    
    # The preindustrial level/baseline is the first twenty years
    warmlvls[memb,0,0] = 0
    warmlvls[memb,0,1] = 20
    
    baseline = np.mean(gmst.tas.isel(ensmemb=memb)[:20])
    
    # Find the deviation from the basline
    deltaT = gmst.tas.isel(ensmemb=memb)-baseline
    
    # Find the index of the warming level in a twenty year mean of the baseline deviation
    
    twentyyrmean = deltaT.rolling(time=20,center=True).mean()
 
    for l in range(1,nGWLs):
        
        if after2070 == True and GWLs[l] == 1.5:
                
            # If you want to look only at the GWL 1.5 after 2070

            idx_after2070 = find_nearest_index(twentyyrmean.sel(time=slice(2070,2101)),GWLs[l])
            idx = 2070-1850+idx_after2070 
        
        else:
            
            idx = find_nearest_index(twentyyrmean,GWLs[l])
        
        # Warming levels is given by the 10 years before and after reaching the level

        warmlvls[memb,l,0] = idx - 10
        warmlvls[memb,l,1] = idx + 10

print("Warming levels found")

fns = ['pi','plus1','plus1-5','plus2', 'plus3','plus4'] # Names of output files

# Specify the year length of the model you are looking at

if model == "CanESM5":
    yrlen = 365
else:
    yrlen = 365.25

for i in var_list:
    
    var_name = var_names[i]
    var_unit = var_units[i]

    # Get the pre-cleaned dataset for you variable of combined historical and ssp data

    dataset = xr.open_dataset("../outputdata/"+var_name+"_"+model+"_historical_ssp"+scenario+"_memb"+str(nmemb)+".nc")
    da = dataset[var_name]
    print("Variable: ",var_name)

    for l in gwl_list:

        if GWLs[l]==0:
            fn = "../outputdata/"+var_name+"_"+fns[l]+"_"+model+"_reg"+reg_name+".nc"
        elif GWLs[l]==1.5 and after2070==True:
            fn = "../outputdata/"+var_name+"_"+fns[l]+"_"+model+"_ssp"+scenario+"_after2070_reg"+reg_name+".nc"
        else:
            fn = "../outputdata/"+var_name+"_"+fns[l]+"_"+model+"_ssp"+scenario+"_reg"+reg_name+".nc"

        # Create a new dataset for each warming level and variable

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
            
            # Get the areaweighted region mask for each region

            Region = np.array(regAreagrid.mask.isel(region=k))

            # Use the warming level year indices to get a timeslice of the data for each ensemble member

            for memb in range(nmemb):
                
                start = math.floor(warmlvls[memb,l,0]*yrlen)
                stop = math.floor(warmlvls[memb,l,1]*yrlen)
                gwl_data = da.isel(time=slice(start,stop),memb=memb)
                
                # For each year in each ensemble member: average over the region for each day and save the output

                for yr in range(20):

                    print("Global warming level:",str(GWLs[l]),"degrees C,  Region number:", k+1,", Ensemble member: ", memb+1, ", Year: ",yr+1)

                    # Index of year for each ensemble
                    gwlyear_idx = memb*20+yr

                    for day in range(365):
                        
                        # Index of time value for the day of year
                        time_idx = math.floor(yr*yrlen)+day

                        value[day,gwlyear_idx,k] = np.nansum(gwl_data[time_idx,:,:]*Region) / np.nansum(Region)
            
        ds.close()

