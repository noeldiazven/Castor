# Función de generación de matrices de clases y características
def generateMatrice(data, K_mer, k):
	# Variables
	X = []
	y = []

	# Generar diccionario K-mer
	X_dict = {}
	for i, e in enumerate(K_mer):  X_dict[e] = 0;
	# Generar X (atributos de matriz)
	for d in data:
		x = []
		x_dict =  X_dict.copy()

		# Contar ocurrencias de K-mer (con superposición)
		for i in range(0, len(d[1]) - k + 1, 1):
			try: x_dict[d[1][i:i + k]] = x_dict[d[1][i:i + k]] + 1; 
			except: pass
		
		# Obtener todas las ocurrencias del diccionario
		for value in x_dict:
			x.append(x_dict.get(value))
		X.append(x)

	# Genera y (clase Matrix) si existe un archivo csv
	if len(data[0]) == 3: 
		for i in data: y.append(i[2])
	
	# Retornar matrices X e y (atributos de matriz y clase de matriz)
	return X, y






