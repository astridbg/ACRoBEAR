import numpy as np

def makeRegion (lon_values, lat_values, reglim):

    # reglim: lonmin, lonmax, latmin, latmax
    # lonrange: 0 - 360
    # latrange: -90 - 90

    nlon = len(lon_values)
    nlat = len(lat_values)

    reg = np.ones((nlat,nlon))

    for i in range(nlon):
        for j in range(nlat):
            if lon_values[i] < reglim[0]:
                reg[j,i] = 0
            elif lon_values[i] > reglim[1]:
                reg[j,i] = 0
            elif lat_values[j] < reglim[2]:
                reg[j,i] = 0
            elif lat_values[j] > reglim[3]:
                reg[j,i] = 0

    return reg
