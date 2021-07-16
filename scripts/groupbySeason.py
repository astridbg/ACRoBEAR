import xarray as xr

# These are functions that group data based on seasons.
# They are specify to group into three and three months.
# The groupBySeason function groups one dataset into seasons,
# while the groupManybySeason function takes dataset with different
# global warming levels (GWL) and groups into different season
# datasets with all GWLs together in one.

def groupbySeason(ds):
    
    # Season start and end dates

    DJF_start2 = 0; DJF_stop2 = 59
    MAM_start = DJF_stop2; MAM_stop = 151
    JJA_start = MAM_stop; JJA_stop = 243
    SON_start = JJA_stop; SON_stop = 334
    DJF_start1 = SON_stop; DJF_stop1 = 365


    MAM = ds.isel(dayofyear=slice(MAM_start, MAM_stop))
    JJA = ds.isel(dayofyear=slice(JJA_start,JJA_stop))
    SON = ds.isel(dayofyear=slice(SON_start,SON_stop))
    DJF = xr.concat([ds.isel(dayofyear=slice(DJF_start1,DJF_stop1)), ds.isel(dayofyear=slice(DJF_start2,DJF_stop2))],"dayofyear")


    return MAM, JJA, SON, DJF


def groupManybySeason (ds_list):

    nds = len(ds_list)

    MAM, JJA, SON, DJF = groupbySeason(ds_list[0])

    for i in range(1,nds):

        MAM_i, JJA_i, SON_i, DJF_i= groupbySeason(ds_list[i])

        MAM = xr.concat([MAM,MAM_i],"GWL")
        JJA = xr.concat([JJA,JJA_i],"GWL")
        SON = xr.concat([SON,SON_i],"GWL")
        DJF = xr.concat([DJF,DJF_i],"GWL")


    return MAM, JJA, SON, DJF


