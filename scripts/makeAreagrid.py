import numpy as np

def makeAreagrid(lon_values, lat_values, mf=[]):

    nlon = len(lon_values)
    nlat = len(lat_values)
    pi = np.pi

    if len(mf) == 0:
        mf = np.ones((nlat, nlon))
    else:
        mf = np.array(mf)

    areafrac = np.zeros(nlat)
    areafracgrid = np.zeros((nlat, nlon))

    for j in range(nlat):
        # Calculate area fraction
        areafrac[j] = (2.0*pi/nlon * pi/nlat * np.cos( lat_values[j]*pi/180.0 )) / (4.0*pi)
        for i in range(nlon):

            if mf[j,i] != 0:
                    
                areafracgrid[j,i] = areafrac[j]
                
            else:

                areafracgrid[j,i] = np.nan

    r_mask = areafracgrid * mf

    return r_mask 

