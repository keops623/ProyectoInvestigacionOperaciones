# Trabajo realizado por: 
# Nestor David Steven Cespedes Castiblanco
# Codigo: 29408
# Proyecto Final de Investigacion de Operaciones
# Clase 9AN - 2024-1 

# Documentacion del codigo

# Importacion de Libreria Flask para Ejecucion en web service
# Importacion de Libreria Numpy para manejo de numeros y metodos matematicos
from flask import Flask, request, render_template
import numpy as np

# Inicio de la aplicacion Main
app = Flask(__name__)

# Metodo laplace, la cual se recoje los valores de la matriz.
# El resultado recoje bajo el metodo np.mean el promedio de los valores
# la variable axis controla que saque el promedio a lo largo del eje de las filas
# el metodo mejor opcion, saca el valor maximo y lo retorna como la mejor opcion
def metodo_laplace(matriz):
    resultados = np.mean(matriz, axis=1)
    mejor_opcion = np.argmax(resultados)
    return resultados, mejor_opcion

# El metodo hurwicz trae los valores de la matriz y solicita el valor alfa
# gestiona la informacion para tener dentro de la matriz maximos, el valor maximo y visceversa
# la variable axis controla que saque el promedio a lo largo del eje de las filas
# Realiza la ecuacion de acuerdo al ValorEsperado=(a*Max+(1-a)*minimos)
# el metodo mejor opcion, saca el valor maximo y lo retorna como la mejor opcion
def metodo_hurwicz(matriz, alfa):
    maximos = np.max(matriz, axis=1)
    minimos = np.min(matriz, axis=1)
    resultados = alfa * maximos + (1 - alfa) * minimos
    mejor_opcion = np.argmax(resultados)
    return resultados, mejor_opcion

# El Metodo savage trae los valores de la matriz
# posteriormente selecciona los valores maximos de cada columna (axis=0 para columnas)
# Resta los valores de la matriz con los maximos de acuerdo a la metodologia y da resultados
# el metodo mejor opcion, saca el valor minimo y lo retorna como la mejor opcion
def metodo_savage(matriz):
    maximos_columna = np.max(matriz, axis=0)
    matriz_regret = maximos_columna - matriz
    resultados = np.max(matriz_regret, axis=1)
    mejor_opcion = np.argmin(resultados)
    return resultados, mejor_opcion


# El Metodo Optimista trae los valores de la matriz
# saca el maximo en valores horizontales e imprime los resultados
#el metodo mejor opcion, saca el valor maximo y lo retorna como la mejor opcion
def metodo_optimista(matriz):
    resultados = np.max(matriz, axis=1)
    mejor_opcion = np.argmax(resultados)
    return resultados, mejor_opcion

# El Metodo Pesimista trae los valores de la matriz
# saca el minimo en valores horizontales e imprime los resultados
#el metodo mejor opcion, saca el valor maximo y lo retorna como la mejor opcion
def metodo_pesimista(matriz):
    resultados = np.min(matriz, axis=1)
    mejor_opcion = np.argmax(resultados)
    return resultados, mejor_opcion

# Gestion y conexiones get y set para entregar a la aplicacion Web.
@app.route('/', methods=['GET', 'POST'])
def index():
    matriz = None
    resultados = None
    alfa = None
# Enviando informacion inicial, se declaran variables N y M para campo en pag web
    if request.method == 'POST':
        try:
            n = int(request.form['n'])
            m = int(request.form['m'])
            matriz = []
# Condicional Si para armar la Matriz de acuerdo a los valores de tamaño de la matriz.
            for i in range(n):
                fila = []
                for j in range(m):
                    valor = request.form.get(f'matriz_{i}_{j}')
                    if valor is None or valor == '':
                        raise ValueError("Faltan valores en la matriz")
                    fila.append(float(valor))
                matriz.append(fila)
            matriz = np.array(matriz)
# Declaracion de la variable alfa para metodo hurwicz
            alfa = float(request.form['alfa'])
# Extraccion y ejecucion de los valores recibidos en los diferentes metodos.
            resultados = {
                'laplace': metodo_laplace(matriz),
                'hurwicz': metodo_hurwicz(matriz, alfa),
                'savage': metodo_savage(matriz),
                'optimista': metodo_optimista(matriz),
                'pesimista': metodo_pesimista(matriz),
            }
# Condicionales de errores
        except (ValueError, TypeError) as e:
            matriz = None
            resultados = None
            print(f"Error en la entrada de datos: {e}")
# Retorno de variables e impresion de las mismas.
    return render_template('index.html', matriz=matriz, resultados=resultados, alfa=alfa)
# Inicio de la aplicacion
if __name__ == '__main__':
    app.run(debug=True)
