import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from groupbySeason import groupbySeason, groupManybySeason
plt.rcParams.update({'font.size': 12})

preInd = xr.open_dataset("../outputdata/preInd.nc")
plus1 = xr.open_dataset("../outputdata/plus1.nc")
plus2 = xr.open_dataset("../outputdata/plus2.nc")
plus3 = xr.open_dataset("../outputdata/plus3.nc")
plus4 = xr.open_dataset("../outputdata/plus4.nc")

dayofyear = preInd.dayofyear


fname = ['alaska','canada','fscand','wsib','esib']
name = ["Alaska", "Canada", "Fennoscandia", "West Siberia", "East Siberia"]


MAM, JJA, SON, DJF = groupManybySeason([preInd, plus1, plus2, plus3, plus4])
print(DJF)
print(DJF.GWL)
print(DJF.isel(GWL=0))

