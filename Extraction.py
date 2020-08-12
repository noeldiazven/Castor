# Imports
import numpy
import K_mers
import Matrices
import Preprocessing
from sklearn import svm
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score
from sklearn.feature_selection import RFE
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_predict

# Función básica de extracción de características
def extractKmers(T, training_data, k_min, k_max, features_min, features_max):
	# Contiene listas de puntuaciones de diferentes longitudes de k
	scores_list = []
	# Contiene una lista de k-mer para cada iteración de rfe
	supports_list = []
	# Lista de diferentes longitudes de k-mer
	k_mers_range = range(k_min, k_max + 1)
	# Clasificador svm
	classifier = svm.SVC(kernel = 'linear', C = 1)

	# Realizar el análisis para los diferentes tamaños de k
	for k in k_mers_range:
		# Iniciar extracción de características basada en k-mers de longitud k
		print("\nBeginning of the " + str(k) + "_mer(s) analysis")

		# Generarte lista de k-mer
		print("Generate K-mers...")
		k_mers = K_mers.generate_K_mers(training_data, k)
		
		# Generar atributos de matrices y clases de matrices
		print("Generate matrices...")
		X, y = Matrices.generateMatrice(training_data, k_mers, k)
		y = numpy.asarray(y)

		# Aplicar MinMaxScaler (0, 1)
		X = Preprocessing.minMaxScaling(X)

		# Si hay más de features_max, aplique RFE (elimine el 10% de las características para eliminar en cada iteración)
		if len(X[0]) > features_max:
			print("Preliminary recursive feature elimination...")	
			rfe = RFE(estimator = classifier, n_features_to_select = features_max, step = 0.1)
			X = numpy.matrix(X)
			X = rfe.fit_transform(X, y)

			# Actualizar lista de k_mers
			for i, value in enumerate(rfe.support_):
				if value == False: k_mers[i] = None
			k_mers = list(filter(lambda a: a != None, k_mers))

		# Eliminación de características recursivas
		from RFE import RFE
		print("Recursive feature elimination...")
		rfe = RFE(estimator = classifier, n_features_to_select = 1, step = 1)
		rfe.fit(X,y) 
		
		# Puntajes y apoyos de la iteración actual 
		scores = [] 
		supports = []
		
		# Evaluación
		for i, supports_rfe in enumerate(rfe.supports):
			# Variables
			temp_index = []
			temp_k_mers = []

			# Imprimir porcentaje de avance
			print("\rFeature subset evaluation :", round((i + 1) / len(rfe.supports) * 100, 0), "%", end = '')

			# Selecciona k-mers con soporte igual True
			for j, support in enumerate(supports_rfe):
				if rfe.supports[i][j] == True: temp_index.append(j)

			# Reemplazar el soporte por los k-mers
			for t in temp_index: temp_k_mers.append(k_mers[t])
			rfe.supports[i] = temp_k_mers

			# Método de evaluación
			stratifiedKFold = StratifiedKFold(n_splits = 5, shuffle = False, random_state = None)
			y_pred = cross_val_predict(classifier, X[:,temp_index], y, cv = stratifiedKFold, n_jobs = 4)
			score = f1_score(y, y_pred, average = 'weighted')

			# Guardar la puntuación y las características de esta iteración
			scores.append(score)
			supports.append(rfe.supports[i])

		# Guarde la lista de puntuaciones y subconjuntos de funciones para esta longitud de k-mers
		scores_list.append(scores)
		supports_list.append(supports)

	# Cambia el orden de las listas para el gráfico. 
	for i, e in enumerate(scores_list):
		scores_list[i].reverse()
		supports_list[i].reverse()

	# Identificar solución
	print("\n\nIdentify optimal solution...")
	# Mejor puntuación de las evaluaciones
	best_score = 0
	# Puntuación óptima en relación con el treshold
	optimal_score = 0
	# Mejor lista de k-mer
	extracted_k_mers = []
	# Mejor longitud de k
	identified_k_length = 0

	# Identificar la mejor solución
	for i, s in enumerate(scores_list):
		if max(s) > best_score:
			best_score = max(s)
			index = s.index(max(s))
			identified_k_length = k_mers_range[i]
			extracted_k_mers = supports_list[i][index]
		elif max(s) == best_score:
			if s.index(max(s)) < index:
				best_score = max(s)
				index = s.index(max(s))
				identified_k_length = k_mers_range[i]
				extracted_k_mers = supports_list[i][index]
		else: pass

	# Identificar la solución óptima
	for i, l in enumerate(scores_list):
		for j, s in enumerate(l):
			if s >=  best_score * T and j <= index: 
				optimal_score = s
				index = j
				identified_k_length = k_mers_range[i]
				extracted_k_mers = supports_list[i][index]
	if optimal_score == 0: optimal_score = best_score


	# Guardar los resultados del gráfico
	fig = plt.figure(figsize = (12, 10) )
	for i, s in enumerate(scores_list):
		label = str(k_mers_range[i]) + "-mers"
		plt.plot(range(len(s)), s, label = label)
	plt.ylabel("F-measure")
	plt.xlabel("Number of features")
	plt.axvline(index + 1, linestyle = ':', color = 'r')
	title = "F-measure : " + str(round(optimal_score, 3)) + " K-mer size : " + str(identified_k_length) + " Number of features : " + str(index + 1)
	plt.title(title)
	plt.legend()
	fname = str("Output/Analysis.png")
	plt.savefig(fname)

	# Guardar k-mers extraídos
	f = open("Output/Kmers.txt", "w")
	for i in extracted_k_mers: f.write(str(i) + "\n");
	f.close()

	# Devuelve k-mers identificados y su longitud
	return extracted_k_mers, identified_k_length
