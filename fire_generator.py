import shapefile
import random
import os
import fileinput
import sys

# Agafem arguments
init_day = sys.argv[1]
init_time = sys.argv[2]
end_day = sys.argv[3]
end_time = sys.argv[4]
index = sys.argv[5]
both = int(sys.argv[6])


# Canvia hora i nom d'arxiu de sortida
for line in fileinput.input('Settings_simulacio.txt', inplace=1):
	if 'StartHour' in line:
		line = line.replace(line.split('\t')[-1], f'= {init_time}\n')
	elif 'StartDay' in line:
		line = line.replace(line.split('\t')[-1], f'= {init_day}\n')
	elif 'EndDay' in line:
		line = line.replace(line.split('\t')[-1], f'= {end_day}\n')
	elif 'EndHour' in line:
		line = line.replace(line.split('\t')[-1], f'= {end_time}\n')
	elif 'ignitionFile ' in line:
		line = line.replace(line.split('/')[-1], f'initial_{index}.shp\n')
	elif 'RasterFileName' in line:
		line = line.replace(line.split('/')[-1], f"Mijas_{index}\n")
	elif 'VectorFileName' in line:
		line = line.replace(line.split('/')[-1], f"Mijas_{index}.VCT\n")
	elif 'shapefile' in line:
		line = line.replace(line.split('/')[-1], f"Mijas_{index}.shp\n")
	sys.stdout.write(line)


# Create a new shapefile
w = shapefile.Writer(
    f"./Input/Starting_points/initial_{index}",
    shapeType=shapefile.POINT)

# Create fields for the attribute table
w.field("field1", "C")

# Límits de cada perímetre diferenciat
upper_left_1 = (3009549., 1632863.)
lower_right_1 = (3010045., 1632176.)
dif_x_1 = abs(upper_left_1[0] - lower_right_1[0])
dif_y_1 = abs(upper_left_1[1] - lower_right_1[1])

# Generar 4 nombres aleatoris 
i_1 = random.random() * dif_x_1 + upper_left_1[0]
j_1 = - random.random() * dif_y_1 + upper_left_1[1]
inc1 = (i_1, j_1)
print(inc1)

if both:
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
w.record("row", "one")
w.point(*inc1)

if both:
	w.record("row", "two")
	w.point(*inc2)

# Save the shapefile
w.close()

