import numpy as np

def gv3(field, lon_values, lat_values, mf=[]):

    nlon = len(lon_values)
    nlat = len(lat_values)
    pi = np.pi

    if len(mf) == 0:
        mf = np.ones((nlat, nlon))
    else:
        mf = np.array(mf)
    
    areafrac = np.zeros(nlat)
    areafracgrid = np.zeros((nlat, nlon))
    avg = 0.0

    
    for j in range(0,nlat):
        # Calculate area fraction
        areafrac[j] = (2.0*pi/nlon * pi/nlat * np.cos( lat_values[j]*pi/180.0 )) / (4.0*pi)

        for i in range(0,nlon):
            # Check input for NaN or Inf, and remove those from average
            if np.isfinite(field[j,i]) == False:
                mf[j,i] = 0
            elif abs(field[j,i]) >= 1.0e20:
                mf[j,i] = 0
           
            if mf[j,i] != 0:
                areafracgrid[j,i] = areafrac[j]

                avg = avg + float(field[j,i]) * areafracgrid[j,i] * mf[j,i]

    avg = avg / np.sum(areafracgrid * mf)

    return avg

