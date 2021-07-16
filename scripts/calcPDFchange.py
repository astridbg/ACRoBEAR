import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
from findOverlap import findOverlap
from groupbySeason import groupbySeason, groupManybySeason
from getGWLdata import getGWLdata
from extremeIndices import CDD, TX90p, WSDI

#-Variable specifications----------------------------------------------------------------

model = "CanESM1"               # Which model are you using?
scenario = "585"                # Which shared socio-economic pathway are you using?
GWLs = [0, 1, 1.5, 2, 3, 4]     # Which global warming levels are you using?
var_list = [0]                  # Which variables (index in var_shortname) are you using?

#----------------------------------------------------------------------------------------

var_shortname = ['tas','ts','pr','abswind','mrso','CDD','TX90p','WSDI']
var_binlims = [[-50,50],[-50,50],[0,10],[0,8],[200,1750]]
var_binsize = [2, 2, 0.5,0.4,10,1,2,1]

reg_shortname = ["alaska","canada","fscand","wsib","esib","us","ea","eu","arc","afr","sam","sane","china","india","land"]
reg_longname = ["Alaska", "Canada", "Fennoscandia", "West Siberia", "East Siberia","USA","East Asia","Europe","Arctic","Africa","South America","Scandinavia","China", "India","Global land areas"]

season_longname = ["spring", "summer", "autumn", "winter"]
season_shortname = ["MAM", "JJA", "SON", "DJF"]

#----------------------------------------------------------------------------------------

for i in var_list:
    
    # Use the getGWLdata function to get a list of warming level data for each variable

    GWL_data = getGWLdata(var_shortname[i], model, scenario, GWLs)
    nreg = len(GWL_data[0].region)
    
    # Group the data into seasons

    MAM, JJA, SON, DJF = groupManybySeason(GWL_data)
    seasons = [MAM, JJA, SON, DJF]
    
    # If the variable is a non-daily variable, find the value per season
    
    if var_shortname[i] == "CDD":
        seasons = CDD(seasons)
    elif var_shortname[i] == "TX90p":
        seasons = TX90p(seasons)
    elif var_shortname[i] == "WSDI":
        seasons = WSDI(seasons)
    
    # Find the bins of the probability histogram

    xlims = var_binlims[i]
    binsize = var_binsize[i]
    bins = np.arange(xlims[0],xlims[-1],binsize)
    bin_centers = 0.5*(bins[1:]+bins[:-1])

    # Create a dataset for the different PDF changes for each GWL, season and region
    
    fn = "../outputdata/pdfchange_"+var_shortname[i]+"_"+model+"_ssp"+scenario+".nc"
    ds = nc.Dataset(fn, 'w', format='NETCDF4')

    GWL = ds.createDimension('GWL', len(GWLs))
    season = ds.createDimension('season', len(seasons))
    region = ds.createDimension('region', nreg)

    GWL_list = ds.createVariable('GWL', 'f4', ('GWL',))
    season_list = ds.createVariable('season', 'str', ('season',))
    region_list = ds.createVariable('region','str',('region',))

    GWL_list[:] = np.array(GWLs)
    season_list[:] = np.array(season_shortname) 
    region_list[:] = np.array(reg_shortname)
    
    # Calculate PDF change values

    A_overlap = ds.createVariable('overlapArea', 'f4', ('GWL','season','region'))
    mean_value = ds.createVariable('meanValue', 'f4', ('GWL','season','region'))
    std_value = ds.createVariable('stdValue', 'f4', ('GWL','season','region'))

    for seas in range(len(seasons)):

        for reg in range(nreg):

            gwl_data = np.array(seasons[seas].isel(GWL=0,region=reg)).flatten()

            pi_density,bins,_ = plt.hist(gwl_data,bins=bins,histtype=u"step",density=True)
            pi_mean = np.mean(gwl_data)
            pi_std = np.std(gwl_data)
 
            A_overlap[0,seas,reg] = 1
            mean_value[0,seas,reg] = pi_mean
            std_value[0,seas,reg] = pi_std

            for l in range(1,len(GWLs)):

                gwl_data = np.array(seasons[seas].isel(GWL=l,region=reg)).flatten()

                density,bins,_ = plt.hist(gwl_data,bins=bins,histtype=u"step",density=True)
                

                # Use the findOverlap function to calculate the change in overlap area from preindustrial climate
                overlap_area = findOverlap(bin_centers, pi_density, bin_centers, density)
                print("Warming level: ",GWLs[l],", Season: ",season_shortname[seas],", Region: ", reg_longname[reg],", Overlap area: ",overlap_area)
                mean_ = np.mean(gwl_data)
                std_ = np.std(gwl_data)
                
                A_overlap[l,seas,reg] = overlap_area
                mean_value[l,seas,reg] = mean_
                std_value[l,seas,reg] = std_
                

    ds.close()


