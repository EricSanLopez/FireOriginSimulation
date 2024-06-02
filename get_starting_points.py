import pandas as pd
import sys
import os
import csv
import shapely as shp
import shapefile
from myLibrary.myMetrics import *
from myLibrary.myUtils import *


#carregar arguments en variables 
idx = 0
final_day = 17
final_hour = 300

print("INICIANT EL PROGRAMA")

#Arxius .shp que es faran servir
simulation_shape = f'./Output/Mijas_{idx}.shp'


# Open existing shapefile
sf = shapefile.Reader(f"Output/Mijas_{idx}")


# Get the shapefile fields
fields = sf.fields[1:]  # Exclude the first field (DeletionFlag)
records = sf.records()
shapes = sf.shapes()

# New file
w = shapefile.Writer(f"aux2_{idx}")


# Copy the fields from the existing shapefile
for field in fields:
    w.field(*field)

fields = [i[0] for i in fields]

df = pd.DataFrame(records, columns=fields)

final_idx = df[(df['Hour'] == final_hour)&\
                        (df['Day'] == final_day)&\
                        (df['Fire_Type'] == 'Expanding Fire')].index[0]


existing_polygon = shapes[final_idx].points
existing_record = records[final_idx]

w.poly([existing_polygon])
w.record(*existing_record)

w.close()


