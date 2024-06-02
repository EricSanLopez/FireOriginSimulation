import geopandas as gpd
import sys
import os
import csv
import shapely as shp
from myLibrary.myMetrics import *
from myLibrary.myUtils import *

if len(sys.argv)!=4:
    print("Remember to input: Simulation shape path Final_Day Final_Hour")
    exit()

#carregar arguments en variables 
idx = sys.argv[1]
final_day = int(sys.argv[2])
final_hour = int(sys.argv[3]) - 30

print("INICIANT EL PROGRAMA")
#Arxius .shp que es faran servir
final_ground_truth = './Input/GIS_themes/Mijas_17_07_2022_0315.shp'
intermediate_ground_truth = './Input/GIS_themes/Mijas_15_07_2022.shp'
simulation_shape = f'./Output/Mijas_{idx}.shp'
city_shape = './Input/GIS_themes/City.shp'

#Extracció dels poligons que formen l'incendi
Sim_mijas = gpd.read_file(simulation_shape)

intermediate_entry = Sim_mijas[(Sim_mijas['Hour']==1200.0)&\
                                (Sim_mijas['Day']==15)&\
                                (Sim_mijas['Fire_Type'] == 'Expanding Fire')]
intermediate_shape = remove_knots(intermediate_entry)

final_entry = Sim_mijas[(Sim_mijas['Hour'] == final_hour)&\
                        (Sim_mijas['Day'] == final_day)&\
                        (Sim_mijas['Fire_Type'] == 'Expanding Fire')]
final_shape = remove_knots(final_entry)

del(intermediate_entry)
del(final_entry)

print("CALCULANT I ESCRIVINT L'ARXIU DE MÈTRIQUES")
#Obrim l'arxiu i fem el csv
with open('fire_scores.csv','a',newline='\n') as csvfile:
    csvwriter = csv.writer(csvfile)
    file_size = os.path.getsize('./fire_scores.csv')

    if file_size==0:
        csvwriter.writerow(['File','Ended_simulation','GT_area','Sim_area','F1','TP','FP','FN'])

    #Calcular dades i metriques de simulacio acabada
    f1_score = calculate_f1_score(final_shape, final_ground_truth, city_shape)
    clarification = clarification_array(final_shape, final_ground_truth, city_shape)
    data = [['Mijas_'+idx, True, clarification['Total_GT'],
            clarification['Total_Pred'], f1_score, clarification['TP'],
            clarification['FP'], clarification['FN']]]
    
    #Calcular dades i metriques de simulacio intermitja
    f1_score = calculate_f1_score(intermediate_shape, intermediate_ground_truth, city_shape)
    clarification = clarification_array(intermediate_shape, intermediate_ground_truth, city_shape)
    data.append(['Mijas_'+idx, False, clarification['Total_GT'],
            clarification['Total_Pred'], f1_score, clarification['TP'],
            clarification['FP'], clarification['FN']])
    
    #Guardem les dades al csv
    csvwriter.writerows(data)

print("CALCUL I GUARDAT FINALITZAT. TINGUI UN BON DIA")

