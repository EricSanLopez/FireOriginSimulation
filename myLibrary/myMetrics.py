import geopandas as gpd
from shapely.ops import unary_union

def calculate_f1_score(predicted_shp, actual_shp_path, city_shp_path):
    # Lectura shapefiles
    #gdf1 = gpd.read_file(predicted_shp_path)  # Area predita
    gdf2 = gpd.read_file(actual_shp_path)  # Area real
    gdf3 = gpd.read_file(city_shp_path) # Area de les ciutats

    # Transformació dels shapefiles
    predicted_geom = predicted_shp
    actual_geom = unary_union(gdf2.geometry)
    city_geom = unary_union(gdf3.geometry)

    # Ajust per tenir en compte l'actuació dels bombers
    adjusted_predicted_geom = predicted_geom.difference(city_geom)
    
    # Càlcul true positive
    intersection = adjusted_predicted_geom.intersection(actual_geom)
    true_positive = intersection.area

    # Càlcul false positive i false negative
    false_positive = predicted_geom.area - true_positive
    false_negative = actual_geom.area - true_positive

    # Precision i recall
    if true_positive + false_positive == 0:
        precision = 0
    else:
        precision = true_positive / (true_positive + false_positive)

    if true_positive + false_negative == 0:
        recall = 0
    else:
        recall = true_positive / (true_positive + false_negative)

    # F1 score
    if precision + recall == 0:
        f1_score = 0
    else:
        f1_score = 2 * (precision * recall) / (precision + recall)

    return f1_score

def clarification_array(predicted_shp, actual_shp_path, city_shp_path):
    clarified = {}
    
    # Load shapefiles
    #gdf1 = gpd.read_file(predicted_shp_path)  # Predicted area
    gdf2 = gpd.read_file(actual_shp_path)  # Actual area
    gdf3 = gpd.read_file(city_shp_path) # Area de les ciutats

    # Combine all geometries in each GeoDataFrame into a single geometry
    predicted_geom = predicted_shp
    city_geom = unary_union(gdf3.geometry)
    actual_geom = unary_union(gdf2.geometry)

    # Ajust per tenir en compte l'actuació dels bombers
    adjusted_predicted_geom = predicted_geom.difference(city_geom)
    
    # Calculate intersection
    intersection = adjusted_predicted_geom.intersection(actual_geom)
    true_positive = intersection.area

    # Calculate false positive and false negative
    false_positive = adjusted_predicted_geom.area - true_positive
    false_negative = adjusted_predicted_geom.area - true_positive

    clarified['TP']=true_positive
    clarified['FP']=false_positive
    clarified['FN']=false_negative
    clarified['Total_GT']=actual_geom.area
    clarified['Total_Pred']=predicted_geom.area

    return clarified