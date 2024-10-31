import io
import pulp
import re
import sys
from typing import List, Tuple
from helper import *


class MetodoEnteroMixto:
    def __init__(self):
        self.hornos_count = 0
        self.hornos = []
        self.demanda = 0
        self.stream = None
        self.modelo = None

    def leer_input(self):
        self.stream = io.StringIO()

        print_step("Parte 1: Crear problema", file=self.stream)

        self.hornos_count = input_int("Ingrese el número de hornos")
        while self.hornos_count < 1:
            print_err("Debe ser mayor a 1")
            self.hornos_count = input_int("Ingrese el número de hornos")

        print(f"Número de hornos {self.hornos_count}", file=self.stream)

        for i in range(self.hornos_count):
            print_section(f"Datos para el horno {i+1}")
            capacidad = input_int("Capacidad")
            costo_fijo = input_float("Costo fijo diario")
            costo_variable = input_float("Costo por barra")
            self.hornos.append([capacidad, costo_fijo, costo_variable])
            print(f"Datos para el horno {i+1}: {dict(capacidad=capacidad, costo_fijo=costo_fijo, costo_variable=costo_variable)}", file=self.stream)

        self.demanda = input_int("Ingrese la demanda total de unidades")

        self.modelo = pulp.LpProblem("MetodoEnteroMixto", pulp.LpMinimize)

        # Variables de decisión
        x = [pulp.LpVariable(f"x{i}", lowBound=0, cat='Integer') for i in range(self.hornos_count)]
        y = [pulp.LpVariable(f"y{i}", cat='Binary') for i in range(self.hornos_count)]
        
        print(f"Variable de decisión: {",".join(xi.name for xi in x)}", file=self.stream)
        print(f"Variable de decisión: {",".join(yi.name for yi in y)}", file=self.stream)

        # Función objetivo
        self.modelo += pulp.lpSum([self.hornos[i][1] * y[i] + self.hornos[i][2] * x[i] for i in range(self.hornos_count)])
        print(f"Función objetivo: {" + ".join(f"{self.hornos[i][1]} * y{i} + {self.hornos[i][2]} * x{i}" for i in range(self.hornos_count))}", file=self.stream)
        
        # Restricciones
        self.modelo += pulp.lpSum(x) == self.demanda, "Demanda_Total"
        for i in range(len(self.hornos)):
            print(f"Restricción: x{i} <= {self.hornos[i][0]} * y{i}", file=self.stream)
            self.modelo += x[i] <= self.hornos[i][0] * y[i], f"Capacidad_Horno_{i+1}"

    def encontrar_solucion(self):
        print_step("Parte 2: Resolviendo el problema usando el algoritmo entero mixto", file=self.stream)
        
        # Configurar el solucionador con opciones específicas
        status = self.modelo.solve()
    
        print_step("Parte 3: Resolver", file=self.stream)
        print(f"Estado de la solución: {pulp.LpStatus[status]}", file=self.stream)

        print_step("Parte 4: Detalles de la solución", file=self.stream)
        for v in self.modelo.variables():
            print(f"{v.name} = {v.varValue}", file=self.stream)

        print(f"Costo total = {pulp.value(self.modelo.objective)}", file=self.stream)

    def exportar(self):
        self.stream.seek(0)
        output = list(self.stream.readlines())
        sys.stdout.writelines(output)

        nombre = input_str("Indique un nombre para el archivo de salida")
        if not nombre.endswith(".txt"):
            nombre = nombre + ".txt"
        with open(f"03 Panaderia - {nombre}", "w") as f:
            f.writelines(output)

    def resolver(self):
        self.leer_input()
        self.encontrar_solucion()
        self.exportar()


if __name__ == "__main__":
    print_title("Panaderia")

    MetodoEnteroMixto().resolver()
    

