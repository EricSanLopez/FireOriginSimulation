import argparse
import os
import sys
import subprocess
from subprocess import PIPE, Popen
import time


if __name__ == "__main__":
	start_time = time.time()
	parser = argparse.ArgumentParser(description='Processing the windfile with WindNinja')
	parser.add_argument('--output', dest='output', type=str, help='Path of the output folder', default=os.getcwd())
	parser.add_argument('--windfile', dest='windfile', type=str, help='Path of the windfile', required=True)
	parser.add_argument('--config', dest='config', type=str, help='Path of the configuration file', required=True)
	args = parser.parse_args()
	try:
		windfile = open(args.windfile, 'r')
		winds = []
		for line in windfile:
			if "ENGLISH" not in line and "METRIC" not in line:
				params = line[:-1].split(" ")
				if len(params) != 6:
					raise ValueError("Error: Alguna dada del fitxer de vents es incorrecta")
				winds.append(params)
	except IOError:
		raise Exception("Error: No s'ha pogut llegir el fitxer de vents.")
	except ValueError as err:
		raise ValueError(str(err))
	finally:
		windfile.close()
	atms = []
	folders = []
	dates = []
	k = 1
	total = len(winds)
	print("Executant la generacio dels camps de vents")
	for wind in winds:
		print("Processant", wind)
		start_time_local = time.time()
		month, day, hour, speed, direction, cover = wind
		try:
			if args.output[-1] != '\\':
				args.output += '\\'
			path = args.output+month+'-'+day+'-'+hour+'\\'
			folders.append(path)
			dates.append([month, day, hour])
			if not os.path.exists(path):
				os.mkdir(path)
		except OSError:
			raise OSError("No s'ha pogut crear el directori de sortida")
		command = ['C:\\WindNinja\\WindNinja-3.10.0\\bin\\WindNinja_cli', args.config, '--output_path', path, '--month', month, '--day', day, '--hour', hour, '--input_speed', speed, '--input_direction', direction]
		result = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
		out, err = result.communicate()
		# if err != '':
		# 	raise ValueError("Error: L'execucio de "+' '.join(command) +" no ha funcionat")
		try:
			for file in os.listdir("C:\\WindNinja\\mijas\\"):
				if file.endswith(".atm"):
					atm = open("C:\\WindNinja\\mijas\\"+file, 'r')
					line = atm.readlines()[2]
					atms.append(line)
					atm.close()
		except IOError:
			raise Exception("Error: No s'ha pogut llegir el fitxer ATM.")
		end_time_local = time.time()
		print("("+str(k)+'/'+str(total)+"): "+str(end_time_local-start_time_local)+" s")
		k+=1

		# Clean files
		print("Cleaning files...")
		batch_file_path = 'C:\\WindNinja\\mijas\\move_files.bat'
		result = subprocess.run([batch_file_path, day, hour], shell=True, text=True, capture_output=True)

	# if len(atms) != len(folders) or len (folders) != len(dates):
	# 	raise ValueError("Error: No coincideixen les dades")
	atm_file = open(args.windfile[:-3]+'atm', 'w')
	atm_file.write('WINDS_AND_CLOUDS\nENGLISH\n')
	vm_atm_path = "/home/wrf-chem/Desktop/FARSITE4/07-Mijas/Input/GIS_themes/Winds-res90/"
	for i in range(len(atms)):
		atm = atms[i].split(' ')
		atm[0] = dates[i][0]
		atm[1] = dates[i][1]
		atm[2] = dates[i][2]
		atm[3] = vm_atm_path + atm[3]
		atm[4] = vm_atm_path + atm[4]
		atm[5] = vm_atm_path + atm[5]
		atm = ' '.join(atm)
		atm_file.write(atm)
	atm_file.close()
	end_time = time.time()
	print("Total time: "+str(end_time-start_time)+" s")
