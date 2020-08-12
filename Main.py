
# IMPORTS
import Data
import Extraction
import Evaluation

# INFORMACIÓN
print("*******************")
print("*** CASTOR-KRFE ***")
print("*******************\n")

print("Alignment-free method to extract discriminant genomic subsequences within pathogen sequences.\n")

# VARIABLES

# Umbral (porcentaje de pérdida de rendimiento en términos de medida F para reducir el número de atributos)
T = 0.999
# Longitud mínima de k-mer(s)
k_min = 1
# Longitud máxima de k-mer(s)
k_max = 5
# Número mínimo de características para identificar
features_min = 1
# Número maximo de características para identificar 
features_max = 100
# Ruta de archivo fasta de entrenamiento
training_fasta = "Input/HIVGRPCG/data.fasta"
# Ruta de archivo fasta de entrenamiento
training_csv = "Input/HIVGRPCG/target.csv"
# Ruta de archivo fasta de pruebas
testing_fasta = "Input/HIVGRPCG/data.fasta"
# Ruta de archivo fasta de pruebas
testing_csv = "Input/HIVGRPCG/target.csv"


# CARGAR DATOS DE ENTRENAMIENTO
print("\nLoading of the training dataset...")
if Data.checkTrainFile(training_fasta, training_csv) == True: training_data = Data.generateTrainData(training_fasta, training_csv)


# EXTRACCIÓN DE CARACTERÍSTICAS
print("\nStart feature extraction...")
extracted_k_mers, identified_k_length = Extraction.extractKmers(T, training_data, k_min, k_max, features_min, features_max)


# EVALUACIÓN DEL MODELO
print("\nEvaluation of the prediction model...")
Evaluation.cross_validation(training_data, extracted_k_mers, identified_k_length, training_data)


# CARGAR DATOS DE PRUEBA
print("\nLoading of the testing dataset...")
if Data.checkTestFile(testing_fasta, testing_csv) == True: testing_data = Data.generateTestData(testing_fasta, testing_csv)


# PREDICCION
if len(testing_data[0]) == 2: 
	print("\nPrediction without evaluation...")
	Evaluation.prediction(training_data, testing_data, extracted_k_mers, identified_k_length)
else: 
	print("\nPrediction with evaluation...")
	Evaluation.predictionEvaluation(training_data, testing_data, extracted_k_mers, identified_k_length)


print("\nEnd of the program ")

