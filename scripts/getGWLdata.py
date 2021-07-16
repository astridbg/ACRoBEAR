import xarray as xr

# This is a function that returns a list of global warming level (GWL)
# data for a specified variable, model and scenario. If the variable is
# not given directly from the climate data, it gets the variable
# from the available data (must be specified for each variable)

def getGWLdata(variable, model, scenario, GWLs,after2070=False):
    
    fns = ['pi','plus1','plus1-5','plus2', 'plus3','plus4'] # Names of GWL data files
    
    GWL_name = [fns[l] for l in range(len(GWLs))]
    datasets = []
    
    # Find relevant available climate variable for index variable
    if variable == 'TX90p' or variable == 'WSDI':
        variable = 'tasmax'
    elif variable == 'CDD':
        variable = 'pr'

    for gwl in GWL_name:
    
        if variable == 'abswind':
            
            # Calculate absolute windspeed

            if gwl == "pi":
                ds = xr.open_dataset("../outputdata/uas_pi_"+model+"_regAll.nc")
                ds['abswind'] = (ds.uas**2 + xr.open_dataset("../outputdata/vas_"+gwl+"_"+model+"_regAll.nc").vas**2)**0.5

            elif gwl == "plus1-5" and after2070==True:
                ds = xr.open_dataset("../outputdata/uas_plus1-5_"+model+"_ssp"+scenario+"_after2070_regAll.nc")
                ds['abswind'] = (ds.uas**2 + xr.open_dataset("../outputdata/vas_"+gwl+"_"+model+"_ssp"+scenario+"_after2070_regAll.nc").vas**2)**0.5

            else: 
                ds = xr.open_dataset("../outputdata/uas_"+gwl+"_"+model+"_ssp"+scenario+"_regAll.nc")
                ds['abswind'] = (ds.uas**2 + xr.open_dataset("../outputdata/vas_"+gwl+"_"+model+"_ssp"+scenario+"_regAll.nc").vas**2)**0.5
            
        elif variable == 'tdiff':

            # Calculate temperature difference

            if gwl == "pi":
                ds = xr.open_dataset("../outputdata/ts_pi_"+model+"_regAll.nc")
                ds['tdiff'] = ds['ts'] - xr.open_dataset("../outputdata/tas_"+gwl+"_"+model+"_regAll.nc").tas

            elif gwl == "plus1-5" and after2070==True:
                ds = xr.open_dataset("../outputdata/ts_plus1-5_"+model+"_ssp"+scenario+"_after2070_regAll.nc")
                ds['tdiff'] = ds['ts'] - xr.open_dataset("../outputdata/tas_"+gwl+"_"+model+"_ssp"+scenario+"_after2070_regAll.nc").tas

            else:
                ds = xr.open_dataset("../outputdata/ts_"+gwl+"_"+model+"_ssp"+scenario+"_regAll.nc")
                ds['tdiff'] = ds['ts'] - xr.open_dataset("../outputdata/tas_"+gwl+"_"+model+"_ssp"+scenario+"_regAll.nc").tas
            
        else:

            if gwl == "pi":
                ds = xr.open_dataset("../outputdata/"+variable+"_pi_"+model+"_regAll.nc")
            elif gwl == "plus1-5" and after2070==True:
                ds = xr.open_dataset("../outputdata/"+variable+"_plus1-5_"+model+"_ssp"+scenario+"_after2070_regAll.nc")
            else:
                ds = xr.open_dataset("../outputdata/"+variable+"_"+gwl+"_"+model+"_ssp"+scenario+"_regAll.nc")

            
        if variable == 'tas' or variable == 'ts' or variable == 'tasmax':
            
            ds[variable] -= 273.15  # Temperature in degrees Celsius

        elif variable == 'pr':
           
            ds[variable] *= 86400 # Precipitation in mm/day
        
        datasets.append(ds[variable])
        
    return datasets
