import xarray as xr
import numpy as np

# These are functions that take relevant global warming level (GWL) data grouped by season,
# and returns a climate index. 
# CDD: consecutive dry days
# TX90p: percentage of days when TX > 90th percentile
# WSDI: warm spell duration index - seasonal count of days with at least 6 consecutive days when TX > 90th percentile


def CDD(seasons):
    
    new_seasons = []

    for season in seasons:

        nyear = len(season.year)
        nreg = len(season.region)
        nGWLs = len(season.GWL)
        CDDs = np.zeros((nGWLs,nyear,nreg))

        for yr in range(nyear):

            for region in range(nreg):

                for gwl in range(nGWLs):

                    dry = np.array(season.isel(GWL=gwl,region=region,year=yr)) < 1
                    
                    # Count cumulative dry days
                    drycum = np.zeros(len(dry))
                    drySUM = 0
                    for i in range(len(dry)):
                        if dry[i] == True:
                            drySUM += 1
                        else:
                            drySUM = 0
                                        
                        drycum[i] = int(drySUM)
                    
                    # Find maximum of cumulative dry days in season
                    CDDs[gwl,yr,region] = drycum.max()

        season["CDD"] = (('GWL','year','region'),CDDs)
        new_seasons.append(season.CDD)
    
    return new_seasons

def TX90p(seasons):

    new_seasons = []
    
    for season in seasons:

        nyear = len(season.year)
        nreg = len(season.region)
        nGWLs = len(season.GWL)
        TX90ps = np.zeros((nGWLs,nyear,nreg))
        
        for yr in range(nyear):

            for region in range(nreg):

                for gwl in range(1,nGWLs):
                    
                    # Use preindustrial climate as baseline
                    baseline = np.array(season.isel(GWL=0,region=region,year=yr).rolling(dayofyear=5,center=True).mean())
                    baseline = np.sort(baseline) # Sort data in ascending order
                    n = len(baseline)
                    k = 0.90
                    idx = int(n*k) # Find the index of the 90th percentile of data
                    TX90 = baseline[idx] # Find 90th percentile value

                    TX = np.array(season.isel(GWL=gwl,region=region,year=yr))
                    ndays = len(TX)
                    
                    SUM = sum(TX > TX90)
                    prc = SUM/ndays*100 # Find seasonal percentage of days warmer than this value 
                    
                    TX90ps[gwl,yr,region] = prc

        season["TX90p"] = (('GWL','year','region'),TX90ps)
        new_seasons.append(season.TX90p)
    
    return new_seasons

def WSDI(seasons):
    
    new_seasons = []
    
    for season in seasons:

        nyear = len(season.year)
        nreg = len(season.region)
        nGWLs = len(season.GWL)
        WSDIs = np.zeros((nGWLs,nyear,nreg))

        for yr in range(nyear):

            for region in range(nreg):

                for gwl in range(1,nGWLs):
                    
                    # Use preindustrial climate as baseline
                    baseline = np.array(season.isel(GWL=0,region=region,year=yr).rolling(dayofyear=5,center=True).mean())
                    baseline = np.sort(baseline) # Sort data in ascending order
                    n = len(baseline)
                    k = 0.90
                    idx = int(n*k) # Find index of 90th percentile of data
                    TX90 = baseline[idx] # Find 90th percentile value 
                    TX = np.array(season.isel(GWL=gwl,region=region,year=yr))
                    
                    warm = TX > TX90 # Find days warmer than 90th percentile
                    
                    # Count cumulative warm days
                    warmcum = np.zeros(len(warm))
                    warmSUM = 0
                    for i in range(len(warm)):
                        if warm[i] == True:
                            warmSUM += 1
                        else:
                            warmSUM = 0

                        warmcum[i] = int(warmSUM)
                    
                    # Find the sum of days that are warmer than 90th percentile for 6 days or longer
                    warmspell = warmcum >= 6
                    WSDIs[gwl,yr,region] = int(sum(warmspell))

        season["WSDI"] = (('GWL','year','region'),WSDIs)
        new_seasons.append(season.WSDI)
    
    return new_seasons

