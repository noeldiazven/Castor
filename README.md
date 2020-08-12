# CASTOR-KRFE
* CASTOR-KRFE v1.1 Help file																		  
* Feature extractor for viral genomic classification                               
* Copyright (C) 2020  Dylan Lebatteux, Amine M. Remita, Abdoulaye Banire Diallo    
* Author : Dylan Lebatteux, Amine M. Remita													  
* Contact : lebatteux.dylan@courrier.uqam.ca

### Descripción
 CASTOR-KRFE es un método sin alineación que extrae características discriminantes de longitud óptima a partir de secuencias genómicas. Construye un modelo de predicción con una evaluación de éste. El modelo se puede utilizar para realizar la predicción de nuevas secuencias.

### Software requerido
* [python](https://www.python.org/downloads/) 
* [scikit-learn](https://scikit-learn.org/stable/install.html) 
* [numpy](https://numpy.org/install/)
* [scipy](https://www.scipy.org/install.html)                        
* [biopython](https://biopython.org/wiki/Download)    
* [matplotlib](https://matplotlib.org/users/installing.html) 

Lista de parámetros que requieren ajuste en el archivo Main.py:
* T: Threshold (se recomienda T = 0,999)
* k_min: longitud mínima de k-mer (s)
* k_max: longitud máxima de k-mer (s)
* features_min: número mínimo de características para identificar
* features_max: número máximo de características para identificar
* training_fasta: Ruta del archivo fasta de entrenamiento
* training_csv: Ruta del archivo cv de entrenamiento
testing_fasta: Prueba de la ruta del archivo fasta
* testing_csv: Prueba de la ruta del archivo cv

### Utilización
Especifique los parámetros de la sección anterior en el archivo Main.py.
Luego ejecuta el siguiente comando:
```sh
$ python -W ignore Main.py 
```
Información complementaria :
- Training_fasta y training_csv son necesarios para la extracción de características, la construcción y evaluación de modelos.
- Si no se especifican testing_fasta y testing_csv, no habrá predicción.
- Si testing_fasta se especifica solo, habrá una predicción sin evaluación.
- Finalmente, si se especifican tanto testing_fasta como testing_csv, habrá predicción con evaluación.

### Entrada
* FASTA: Contiene las secuencias en formato fasta. Ejemplo: 
```sh
>id_sequence_1.description_sequence_1 
CTCAACTCAGTTCCACCAGGCTCTGTTGGATCCGAGGGTAAGGGCTCTGTATTTTCCTGC 
>id_sequence_2.description_sequence_2						
CTCAACTCAGTTCCACCAGGCTCTGTTGGATCCGAGGGTAAGGGCTCTGTATTTTCCTGC
...
...
...
>id_sequence_n-1.description_sequence_n-1												 
CTCAACTCAGTTCCACCAGGCTCTGTTGGATCCGAGGGTAAGGGCTCTGTATTTTCCTGC 
>id_sequence_n.description_sequence_n															 
CTCAACTCAGTTCCACCAGGCTCTGTTGGATCCGAGGGTAAGGGCTCTGTATTTTCCTGC 
```

* CSV : Contiene las clases asociadas con cada secuencia. Ejemplo:
```sh
id_sequence_1,class_sequence_1																 
id_sequence_2,class_sequence_2																		 
...																		 
...																			 
...	
id_sequence_n-1,class_sequence_n-1																 
id_sequence_n,class_sequence_n	
```

* Para obtener ejemplos más detallados, consulte los conjuntos de datos en la carpeta Datos

### Salida
* Analysis.png: muestra el gráfico de decisión del conjunto óptimo de k-mers mediante el algoritmo CASTOR
* model.pkl: modelo de predicción generado por CASTOR-KRFE
* Kmers.txt: Archivo de la lista de k-mers extraída
* Matrice.csv: contiene la matriz formada con las características extraídas
* Model_Evaluation.txt: Archivo de resultados de la evaluación de un modelo con un conjunto de datos de secuencias etiquetadas
* Prediction_Evaluation.txt: Archivo de resultados de la evaluación del conjunto de pruebas
* Prediction.csv: Archivo de resultados de la predicción de secuencias genómicas desconocidas sin evaluación
* Prediction_Evaluation.csv: Archivo de resultados de la predicción de secuencias genómicas desconocidas con evaluación

### Referencia para citar CASTOR-KRFE
* [Lebatteux, D., Remita, A. M., & Diallo, A. B. (2019). Toward an alignment-free method for feature extraction and accurate classification of viral sequences. Journal of Computational Biology, 26(6), 519-535.](https://www.liebertpub.com/doi/pdfplus/10.1089/cmb.2018.0239)
                                                                                   
