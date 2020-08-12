# Imports
import os
import sys
import csv
from Bio import SeqIO

# Función de comprobación de la existencia y accesibilidad de archivos de formación. 
def checkTrainFile(training_fasta, training_csv):
	# Ver archivo fasta
	if os.path.isfile(training_fasta) and os.access(training_fasta, os.R_OK): 
		print(training_fasta, "file exists and is readable")
		# Comprobar archivo csv
		if os.path.isfile(training_csv) and os.access(training_csv, os.R_OK): 
			print(training_csv, "file exists and is readable")
			# Devuelve verdadero si todo es correcto
			return True
		# Salir y mostrar un mensaje en caso de error
		else: sys.exit("Training csv file is missing or not readable")
	else: sys.exit("Training fasta file is missing or not readable")

# Función que comprueba la existencia y accesibilidad de los archivos de prueba.
def checkTestFile(testing_fasta, testing_csv):
	# Ver archivo fasta
	if os.path.isfile(testing_fasta) and os.access(testing_fasta, os.R_OK): 
		print(testing_fasta, "file exists and is readable")
		# Comprobar archivo csv
		if os.path.isfile(testing_csv) and os.access(testing_csv, os.R_OK): 
			# Devuelve True si todo es correcto (predicción con evaluación)
			print(testing_csv, "file exists and is readable")
			return True
		else: 
			# Devuelve True si solo el archivo fasta es correcto (predicción sin evaluación)
			print("Testing csv file is missing or not readable")
			return True
	else: sys.exit("Testing fasta file is missing or not readable")

# Función que genera la tabla de datos
def generateTrainData(fasta_file, csv_file):
	# Variable data 
	data = []

	# Abrir el archivo de la clase
	with open(csv_file) as f: reader = dict(csv.reader(f))

	#Abrir el archivo de secuencias
	for record in SeqIO.parse(fasta_file, "fasta"):
		# Generar tabla [Id, Sequences, Class]
		if record.id in reader: data.append([record.id, record.seq.upper(), reader[record.id]])

	# Return data
	return data

# Función que genera la tabla de datos
def generateTestData(fasta_file, csv_file):
	# Variable data 
	data = []

	# Llamar a la función clásica
	if csv_file: data = generateTrainData(fasta_file, csv_file)
	else: 
		# Abra el archivo de secuencias y genere la tabla [Id, Sequences]
		for record in SeqIO.parse(fasta_file, "fasta"): data.append([record.id, record.seq.upper()])
			
	# Return data
	return data


