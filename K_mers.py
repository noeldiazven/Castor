import re #se importa la libreria para trabajar con expresiones regulares 

# Función que genera los k_mers pertenecientes a las secuencias
def generate_K_mers(data, k):
	# List of k-mer
	K_mers = []
	dict = {}

	# Inicialización del diccionario
	for d in data:
		for i in range(0, len(d[1]) - k + 1, 1): dict[d[1][i:i + k]] = 0;
		
	# Eliminar patrones no utilizados
	for key in dict.keys():
		if bool(re.match('^[ACGT]+$', str(key))) == True: K_mers.append(str(key))
	
	# Retorna los kmers
	return K_mers


