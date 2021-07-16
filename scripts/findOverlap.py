import numpy as np
from shapely.geometry import LineString
from shapely.ops import unary_union, polygonize

# This function returns the overlap area between two curves.
# It was created specifically to calculate the overlapping area between the probability density funciton of 
# preindustrial climate (pi) and other global warming levels (gwl), but can be used generally.
# Give it the x values and the y values of curve 1 and curve 2 (x1, y1, x2, y2). The x steps must be uniform.

def findOverlap(pi_x, pi_y, gwl_x, gwl_y):
    
    # Create a list for each curve of (x,y) points

    pi_coords = []
    gwl_coords = []

    for i in range(len(pi_x)):
        pi_coords.append((pi_x[i],pi_y[i]))
    for i in range(len(gwl_x)):
        gwl_coords.append((gwl_x[i],gwl_y[i]))

    # Create an empty list where we will append the points of the two curves to create a polygon
    # The polygon consists of the space between the two curves that does *not* overlap 

    polygon_points = [] 
    
    for xyvalue in pi_coords:
        polygon_points.append([xyvalue[0],xyvalue[1]]) #append all xy points for curve 1
    
    for xyvalue in gwl_coords[::-1]:
        polygon_points.append([xyvalue[0],xyvalue[1]]) #append all xy points for curve 2 in the reverse order (from last point to first point)
    
    for xyvalue in pi_coords[0:1]:
        polygon_points.append([xyvalue[0],xyvalue[1]]) #append the first point in curve 1 again, to it "closes" the polygon
    
    # Create a bunch of small polygons from the edges of the large polygon
    
    line_non_simple = LineString(polygon_points)
    mls = unary_union(line_non_simple)

    Area_cal =[]
    
    if (pi_y == gwl_y).all():
        
        # If curve 1 and curve 2 are the same, the overlap area is 1

        overlap_area = 1
    
    else:
    
        for polygon in polygonize(mls):

            # Calculate the area of all the small polygons and summarize them

            Area_cal.append(polygon.area)
            Area_poly = (np.asarray(Area_cal).sum())
        
        # Find the sum of total area under the two separate curves
        # The x binsize must be uniform
        
        pi_x_binsize = pi_x[1]-pi_x[0]                  
        gwl_x_binsize = gwl_x[1]-gwl_x[0]
        totarea = np.sum(pi_x_binsize*pi_y) + np.sum(gwl_x_binsize*gwl_y)
        
        # Get the overlap area by subtracting the polygon area (non-overlapping area) from the total area
        # Divide by two in order to not count the overlap area twice

        overlap_area = (totarea - Area_poly)*0.5

    return overlap_area
    


