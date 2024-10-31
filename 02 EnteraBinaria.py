import io
import pulp
import re
import sys
from typing import List, Tuple
from helper import *


class MetodoBinario:
    def __init__(self):
        self.ciudades_count = 0
        self.tiempos = []
        self.stream = None
        self.modelo = None

    def leer_input(self):
        self.stream = io.StringIO()

        print_step("Parte 1: Crear problema", file=self.stream)

        self.ciudades_count = input_int("Ingrese el número de ciudades")
        while self.ciudades_count < 2:
            print_err("Debe ser mayor a 2")
            self.ciudades_count = input_int("Ingrese el número de ciudades")

        print(f"Número de ciudades {self.ciudades_count}", file=self.stream)

        for i in range(self.ciudades_count):
            fila = []
            for j in range(self.ciudades_count):
                if i != j:
                    tiempo = input_int(f"Tiempo de viaje entre ciudad {i+1} y ciudad {j+1}")
                    while tiempo < 0:
                        print_err("Debe ser mayor a 0")
                        tiempo = input_int(f"Tiempo de viaje entre ciudad {i+1} y ciudad {j+1}")
                    fila.append(tiempo)
                else:
                    fila.append(0)
            self.tiempos.append(fila)
            print(fila, file=self.stream)

        self.modelo = pulp.LpProblem("MetodoBinario", pulp.LpMinimize)

        # Variables de decisión
        x = [pulp.LpVariable(f"x_{i}", cat='Binary') for i in range(self.ciudades_count)]
        print(f"Variable de decisión: {",".join(xi.name for xi in x)}", file=self.stream)

        # Función objetivo: minimizar el número de estaciones
        self.modelo += pulp.lpSum(x)

        tiempo_maximo = input_int("Ingrese la cota superior del tiempo (en minutos)")
        print(f"Cota superior del tiempo: {tiempo_maximo} minutos", file=self.stream)

        # Restricciones: cada ciudad debe estar a no más de 30 minutos de una estación
        for i in range(self.ciudades_count):
            self.modelo += pulp.lpSum(x[j] for j in range(self.ciudades_count) if self.tiempos[i][j] <= tiempo_maximo) >= 1

    def encontrar_solucion(self):
        print_step("Parte 2: Resolviendo el problema usando el algoritmo entero binario", file=self.stream)
        
        # Configurar el solucionador con opciones específicas
        status = self.modelo.solve()
    
        print_step("Parte 3: Resolver", file=self.stream)
        print(f"Estado de la solución: {pulp.LpStatus[status]}", file=self.stream)

        print_step("Parte 4: Detalles de la solución", file=self.stream)
        print(f"Nro. mínimo de estaciones: {sum(var.varValue for var in self.modelo.variables())}", file=self.stream)
        print(f"Ubicaciones:", file=self.stream)

        for i, var in enumerate(self.modelo.variables()):
            if var.varValue == 1:
                print(f"Ciudad {i+1}", file=self.stream)

    def exportar(self):
        self.stream.seek(0)
        output = list(self.stream.readlines())
        sys.stdout.writelines(output)

        nombre = input_str("Indique un nombre para el archivo de salida")
        if not nombre.endswith(".txt"):
            nombre = nombre + ".txt"
        with open(f"02 EnteraBinaria - {nombre}", "w") as f:
            f.writelines(output)

    def resolver(self):
        self.leer_input()
        self.encontrar_solucion()
        self.exportar()


if __name__ == "__main__":
    print_title("Binario")

    MetodoBinario().resolver()
    

