# Imports
import joblib
import Matrices
import Preprocessing
from sklearn import svm
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_predict

# Función de evaluación del modelo
def cross_validation(training_data, extracted_k_mers, identified_k_length, data):
	# Generar matrices
	X, y = Matrices.generateMatrice(training_data, extracted_k_mers, identified_k_length)
	X = Preprocessing.minMaxScaling(X)

	# Realice la evaluación con CV + Clasificador + Métricas
	classifier = svm.SVC(kernel = 'linear', C = 1)
	stratifiedKFold = StratifiedKFold(n_splits = 5, shuffle = False, random_state = None)
	y_pred = cross_val_predict(classifier, X, y, cv = stratifiedKFold, n_jobs = 4)
	
	# Imprimir resultados de la evaluación del modelo
	classificationReport = classification_report(y, y_pred, digits = 3)
	confusionMatrix = confusion_matrix(y, y_pred)
	print("\nClassification report of model evaluation\n", classificationReport)
	print("Confusion matrix \n", confusionMatrix)

	# Guardar Matrice
	f = open("Output/Matrice.csv", "w")
	f.write("Id,")
	for i in extracted_k_mers: f.write(str(i) + ","); 
	f.write("Class\n")

	for i, x in enumerate(X):
		f.write(str(data[i][0]) + ",")
		for j in x: f.write(str(j) + ",")
		f.write(str(y[i]) + "\n")
	f.close()

	# Guardar model
	classifier.fit(X, y)
	joblib.dump(classifier, 'Output/model.pkl') 

	# Guardar los resultados de la evaluación del modelo
	f = open("Output/Model_Evaluation.txt", "w")
	f.write("Classification report of model evaluation\n" +  classificationReport);
	f.write("\nConfusion matrix \n" + str(confusionMatrix));
	f.close()



# Función de predicción sin evaluación
def prediction(training_data, testing_data, extracted_k_mers, identified_k_length):
	# Generar matrices
	X_test, y_test = Matrices.generateMatrice(testing_data, extracted_k_mers, identified_k_length)
	X_test = Preprocessing.minMaxScaling(X_test)
	
	# Cargar model
	classifier = joblib.load('Output/model.pkl')

	# Realizar predicción
	y_pred = classifier.predict(X_test)

	# Guardar predicción
	f = open("Output/Prediction.csv", "w")
	f.write("id,y_pred\n");
	for i, y in enumerate(y_pred): f.write(testing_data[i][0] + "," + y + "\n");
	f.close()

# Función de predicción con evaluación
def predictionEvaluation(training_data, testing_data, extracted_k_mers, identified_k_length):
	# Generar matrices
	X_test, y_test = Matrices.generateMatrice(testing_data, extracted_k_mers, identified_k_length)
	X_test = Preprocessing.minMaxScaling(X_test)
	
	# Cargar model
	classifier = joblib.load('Output/model.pkl')

	# Realizar prediction
	y_pred = classifier.predict(X_test)

	# Imprimir resultados
	classificationReport = classification_report(y_test, y_pred, digits = 3)
	confusionMatrix = confusion_matrix(y_test, y_pred)
	print("\nClassification report of prediction evaluation\n", classificationReport)
	print("Confusion matrix \n", confusionMatrix)

	# Guardar predicción 
	f = open("Output/Prediction_Evaluation.csv", "w")
	f.write("id,y_pred,y_true\n");
	for i, y in enumerate(y_pred): f.write(testing_data[i][0] + "," + y + "," + y_test[i] + "\n");
	f.close()

	# Guardar los resultados de la evaluación de la predicción
	f = open("Output/Prediction_Evaluation.txt", "w")
	f.write("Classification report of prediction evaluation\n" +  classificationReport);
	f.write("\nConfusion matrix \n" + str(confusionMatrix));
	f.close()



