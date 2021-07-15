import numpy as np
import xarray as xr
import netCDF4 as nc
from makeRegion import makeRegion
from makeAreagrid import makeAreagrid

model = "CanESM5"

lf = xr.open_dataset("../regions/landfrac_"+model+".nc")
lon_values = lf.lon
lat_values = lf.lat

if model == "CanESM5":
    landfrac = lf.sftlf/100
if model == "MPI-ESM1-2-LR":
    landfrac = lf.landfrac[0]*1.0

landfrac_binary = landfrac

for i in range(len(lon_values)):

    for  j in range(len(lat_values)):

        frac = landfrac[j,i]

        if frac >= 0.8:
            
            landfrac_binary[j,i] = 1
        
        else: 

            landfrac_binary[j,i] = 0

landfrac_binary.to_netcdf("../regions/landfrac_binary_"+model+".nc")

r_alaska = makeRegion(lon_values, lat_values, [200,230,58,72])      # Alaska
r_canada = makeRegion(lon_values, lat_values, [235,280,52,68])      # Canada
r_fscand = makeRegion(lon_values, lat_values, [4,35,57,72])         # Fennoscandia
r_wsib = makeRegion(lon_values, lat_values, [45,95,57,72])          # Western Siberia
r_esib = makeRegion(lon_values, lat_values, [95,145,57,72])         # Eastern Siberia
r_us = makeRegion(lon_values,lat_values,[360-125,360-75,30,50])     # USA 
r_ea = makeRegion(lon_values,lat_values,[75,135,15,45])             # East Asia
r_eu = makeRegion(lon_values,lat_values,[0,45,40,60])               # Europe
r_arc = makeRegion(lon_values,lat_values,[0,360,60,90])             # The Arctic
r_afr = makeRegion(lon_values,lat_values,[10,40,-35,5])             # Africa
r_sam = makeRegion(lon_values,lat_values,[360-80,360-40,-55,10])    # South America
r_sane = makeRegion(lon_values,lat_values,[0,30,55,70])             # Scandinavia and Northern Europe
r_china = makeRegion(lon_values,lat_values,[90,120,20,40])          # China
r_india = makeRegion(lon_values,lat_values,[70,90,5,30])            # India
land = np.ones((len(lat_values),len(lon_values)))                   # Global land areas

regions = [r_alaska,r_canada,r_fscand,r_wsib,r_esib,r_us,r_ea,r_eu,r_arc,r_afr,r_sam,r_sane,r_china,r_india, land]
regnames = ["alaska","canada","fscand","wsib","esib","us","ea","eu","arc","afr","sam","sane","china","india","land"]

mask = np.zeros((len(regions), len(lat_values), len(lon_values)))

for i in range(len(regions)):
    
    mask[i,:,:] = makeAreagrid(lon_values, lat_values, landfrac_binary*regions[i]) 

regAreagrid = xr.Dataset(data_vars = dict(mask = (["region", "lat", "lon"], mask)), coords = dict(region=regnames, lon=lon_values, lat = lat_values))

regAreagrid.sel(region=slice("alaska","esib")).to_netcdf("../regions/regAreagrid_"+model+"_Arc.nc")
regAreagrid.to_netcdf("../regions/regAreagrid_"+model+"_All.nc")
