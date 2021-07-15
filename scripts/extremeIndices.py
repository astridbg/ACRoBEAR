import xarray as xr
import numpy as np

def CDD(seasons):
 
    for season in seasons:

        nyear = len(season.year)
        nreg = len(season.region)
        nGWLs = len(season.GWL)
        print(nyear)
        CDDs = np.zeros((nGWLs,nyear,nreg))

        for yr in range(nyear):

            for region in range(nreg):

                for gwl in range(nGWLs):

                    dry = np.array(season.isel(GWL=gwl,region=region,year=yr)) < 1
                    drycum = np.zeros(len(dry))
                    drySUM = 0
                    for i in range(len(dry)):
                        if dry[i] == True:
                            drySUM += 1
                        else:
                            drySUM = 0
                                        
                        drycum[i] = int(drySUM)
                    
                    CDDs[gwl,yr,region] = drycum.max()

        season["CDD"] = (('GWL','year','region'),CDDs)
    
    return seasons

def TX90p(seasons):

    for season in seasons:

        nyear = len(season.year)
        nreg = len(season.region)
        nGWLs = len(season.GWL)
        TX90ps = np.zeros((nGWLs,nyear,nreg))
        
        
        for yr in range(nyear):

            for region in range(nreg):

                for gwl in range(1,nGWLs):
                    
                    baseline = np.array(season.isel(GWL=0,region=region,year=yr).rolling(dayofyear=5,center=True).mean())
                    baseline = np.sort(baseline)
                    n = len(baseline)
                    k = 0.90
                    idx = int(n*k)
                    TX90 = baseline[idx]

                    TX = np.array(season.isel(GWL=gwl,region=region,year=yr))
                    ndays = len(TX)
                    
                    SUM = sum(TX > TX90)
                    prc = SUM/ndays*100
                    
                    TX90ps[gwl,yr,region] = prc

        season["TX90p"] = (('GWL','year','region'),TX90ps)

    return seasons

def WSDI(seasons):

    for season in seasons:

        nyear = len(season.year)
        nreg = len(season.region)
        nGWLs = len(season.GWL)
        WSDIs = np.zeros((nGWLs,nyear,nreg))

        for yr in range(nyear):

            for region in range(nreg):

                for gwl in range(1,nGWLs):

                    baseline = np.array(season.isel(GWL=0,region=region,year=yr).rolling(dayofyear=5,center=True).mean())
                    baseline = np.sort(baseline)
                    n = len(baseline)
                    k = 0.90
                    idx = int(n*k)
                    TX90 = baseline[idx]
                    TX = np.array(season.isel(GWL=gwl,region=region,year=yr))
                    
                    warm = TX > TX90
                    warmcum = np.zeros(len(warm))
                    warmSUM = 0
                    for i in range(len(warm)):
                        if warm[i] == True:
                            warmSUM += 1
                        else:
                            warmSUM = 0

                        warmcum[i] = int(warmSUM)
                    
                    warmspell = warmcum >= 6
                    WSDIs[gwl,yr,region] = int(sum(warmspell))

        season["WSDI"] = (('GWL','year','region'),WSDIs)

    return seasons

