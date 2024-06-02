#!/bin/bash

#SBATCH --partition=p_hpca4se
#SBATCH -x huberman
###SBATCH -w huberman
#SBATCH -J FARSITE_SIMPLE
#SBATCH -N 1-1
#SBATCH -n 1
#SBATCH -c 1
#SBATCH --time=000:10:00
#SBATCH --error=FARSITE_SIMPLE.err
#SBATCH --output=FARSITE_SIMPLE.out
#SBATCH --mem-per-cpu=9000
#SBATCH --cpu_bind=verbose
#SBATCH --sockets-per-node=1
#SBATCH --cores-per-socket=1
###SBATCH --threads-per-core=1
###SBATCH --ntasks-per-socket=2

# Arguments:
## Index: nombre enter indicant l'index de la simulacio, per evitar sobreescriure arxius
## Dia inicial: dia quan comencen els focus
## Temps inicial: hora i minut quan comença el primer focus
## Temps segon focus: hora i minut quan comença el segon focus
## Dia final: dia quan acaba tot l'incendi
## Temps final: hora i minut quan acaba tot l'incendi
## Index final: fins quin index simulem

START=$(date +%s)

for (( i=$1; i<$7; i++))
do
	echo "Simulacio $i"

	if [ $3 -eq $4 ]
	then
		echo "Same starting time case"
		python fire_generator.py $2 $3 $5 $6 $i 1
		echo "Both initial points generated"
	else
		python fire_generator.py $2 $3 $2 $4 $i 0		
		echo "First initial point generated"
		./farsite4P -i Settings_simulacio.txt -f 4
		echo "Simulated first fire from $3 until $4, day $2"
		python fire_generator_2.py $4 $5 $6 $i
		echo "Second initial point generated"
	fi
	
	./farsite4P -i Settings_simulacio.txt -f 4
	echo "Simulated entire fire from $4 (day $2) until $6 (day $5)"
	# python Score_processing.py $i $5 $6
done

END=$(date +%s)
DIFF=$(( $END - $START ))
echo "It took $DIFF seconds"



