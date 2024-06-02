import shapefile
import random
import sys
import fileinput

# Agafem arguments
init_time = sys.argv[1]
end_day = sys.argv[2]
end_time = sys.argv[3]
index = sys.argv[4]


# Canvia hora i nom d'arxiu de sortida
for line in fileinput.input('Settings_simulacio.txt', inplace=1):
	if 'StartHour' in line:
		line = line.replace(line.split('\t')[-1], f'= {init_time}\n')
	if 'EndDay' in line:
		line = line.replace(line.split('\t')[-1], f'= {end_day}\n')
	elif 'EndHour' in line:
		line = line.replace(line.split('\t')[-1], f'= {end_time}\n')
	elif 'ignitionFile ' in line:
		line = line.replace(line.split('/')[-1], f'second_{index}.shp\n')
	sys.stdout.write(line)


# Open existing shapefile
sf = shapefile.Reader(f"Output/Mijas_{index}")

# Get the shapefile fields
fields = sf.fields[1:]  # Exclude the first field (DeletionFlag)
records = sf.records()
shapes = sf.shapes()

# Create a new shapefile for editing
w = shapefile.Writer(f"Input/Starting_points/second_{index}")

# Copy the fields from the existing shapefile
for field in fields:
    w.field(*field)

existing_polygon = shapes[-1].points
existing_record = records[-1]

w.poly([existing_polygon])
w.record(*existing_record)

# Add a new polygon
upper_left_2 = (3010875., 1631557.)
lower_right_2 = (3011371., 1631190.)
dif_x_2 = abs(upper_left_2[0] - lower_right_2[0])
dif_y_2 = abs(upper_left_2[1] - lower_right_2[1])

# Generar 4 nombres aleatoris 
i_2 = random.random() * dif_x_2 + upper_left_2[0]
j_2 = - random.random() * dif_y_2 + upper_left_2[1]
inc2 = (i_2, j_2)
print(inc2)

# Crear els punts
w.poly(
       [[(inc2[0] + 10, inc2[1]),
        (inc2[0] + 10, inc2[1] + 10),
        (inc2[0], inc2[1] + 10)]]
)
w.record(2, 67)

# Save the edited shapefile
w.close()
