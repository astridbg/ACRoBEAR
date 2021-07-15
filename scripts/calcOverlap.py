import numpy as np
#from shapely.geometry import Polygon
from shapely.geometry import LineString
from shapely.ops import unary_union, polygonize

def calcOverlap(pi_x, pi_y, gwl_x, gwl_y):
    
    pi_coords = []
    gwl_coords = []

    for i in range(len(pi_x)):
        pi_coords.append((pi_x[i],pi_y[i]))
    for i in range(len(gwl_x)):
        gwl_coords.append((gwl_x[i],gwl_y[i]))

    polygon_points = [] #creates a empty list where we will append the points to create the polygon
    
    for xyvalue in pi_coords:
        polygon_points.append([xyvalue[0],xyvalue[1]]) #append all xy points for curve 1
    
    for xyvalue in gwl_coords[::-1]:
        polygon_points.append([xyvalue[0],xyvalue[1]]) #append all xy points for curve 2 in the reverse order (from last point to first point)
    
    for xyvalue in pi_coords[0:1]:
        polygon_points.append([xyvalue[0],xyvalue[1]]) #append the first point in curve 1 again, to it "closes" the polygon
    
    pi_poly = []
    gwl_poly = []

    for xyvalue in pi_coords:
        pi_poly.append([xyvalue[0],xyvalue[1]])

    for xyvalue in gwl_coords:
        gwl_poly.append([xyvalue[0],xyvalue[1]])


    line_non_simple = LineString(polygon_points)
    mls = unary_union(line_non_simple)

    Area_cal =[]
    
    if (pi_y == gwl_y).all():
        
        overlap_area = 1
    
    else:
    
        for polygon in polygonize(mls):
            Area_cal.append(polygon.area)
            Area_poly = (np.asarray(Area_cal).sum())

        pi_x_binsize = pi_x[1]-pi_x[0]                  #binsize must be uniform
        gwl_x_binsize = gwl_x[1]-gwl_x[0]
        totarea = np.sum(pi_x_binsize*pi_y) + np.sum(gwl_x_binsize*gwl_y)

        overlap_area = (totarea - Area_poly)*0.5

    return overlap_area
    


