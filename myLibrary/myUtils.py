from shapely import LineString, polygonize

def remove_knots(line):
    #Ensure usability of line
    line = line.loc[line.index[0]].geometry
    # Create a thin buffer around the LineString
    buffered = line.buffer(0.001, resolution=1)
    
    # Extract the exterior boundary as a LineString
    outer_boundary = LineString(buffered.exterior.coords)
    
    # Polygonize the resulting boundary to handle any remaining issues
    polygons = polygonize([outer_boundary])
    return polygons