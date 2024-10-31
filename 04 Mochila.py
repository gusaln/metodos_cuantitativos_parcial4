import io
import pulp
import re
import sys
from typing import List, Tuple
from helper import *

class MetodoMochila:
    def __init__(self) -> None:
        self.pesos_count = 0
        self.pesos = []
        self.valores = []
        self.capacidad = 0
        self.is_valid = False
        self.output = None

    def leer_input(self):
        print_section("El método de la mochila")

        self.is_valid = False

        pesos_count = input_int("indique el número de pesos objetivo")
        pesos = [i for i in range(pesos_count)]
        valores = [i for i in range(pesos_count)]

        # Determinamos los pesos
        while True:
            raw = input_str("Indique los pesos separados por coma")
            parts = [s.strip() for s in raw.split(",")]
            if len(parts) != pesos_count:
                print_err("no se indicó el número correcto de valores")
                continue

            for i, vi in enumerate(parts):
                try:
                    pesos[i] = int(vi)
                except:
                    print_err(f"'{vi}' debe ser número un entero")
                    break
            else:
                break

        # Determinamos los valores
        while True:
            raw = input_str("Indique los valores objetivo separados por coma")
            parts = [s.strip() for s in raw.split(",")]
            if len(parts) != pesos_count:
                print_err("no se indicó el número correcto de valores")
                continue

            for i, vi in enumerate(parts):
                try:
                    valores[i] = int(vi)
                except:
                    print_err(f"'{vi}' debe ser número un entero")
                    break
            else:
                break

        capacidad = input_int("Indique la capacidad")

        self.pesos_count = pesos_count
        self.pesos = pesos
        self.valores = valores
        self.capacidad = capacidad
        self.is_valid = True

        return self

    def encontrar_solucion(self):
        if not self.is_valid:
            raise Exception("Las entradas no son válidas")

        self.output = []
        stream = io.StringIO()

        # Paso 1: Crear el problema de maximización
        print_step("Paso 1: Crear el problema de maximización", file=stream)
        problema_mochila = pulp.LpProblem("Problema_de_la_Mochila", pulp.LpMaximize)
        print("Pesos:", self.pesos, file=stream)
        print("Valores:", self.valores, file=stream)
        print("Capacidad:", self.capacidad, file=stream)
        
        # Paso 2: Definir las variables de decisión (0 o 1 para cada objeto)
        print_step("Paso 2: Definir las variables de decisión", file=stream)
        x = [pulp.LpVariable(f"x_{i+1}", cat='Binary') for i in range(self.pesos_count)]
        print("Variables de decisión definidas (0 = no seleccionado, 1 = seleccionado):", file=stream)
        for i in range(self.pesos_count):
            print(f"x_{i+1} -> Objeto {i+1}", file=stream)
        print(x, file=stream)

        # Paso 3: Definir la función objetivo (maximizar el valor total)
        print_step("Paso 3: Definir la función objetivo", file=stream)
        problema_mochila += sum(self.valores[i] * x[i] for i in range(self.pesos_count)), "Valor_total"
        print("Función objetivo formulada: Maximizar el valor total de los objetos seleccionados.", file=stream)

        # Paso 4: Definir la restricción de capacidad de la mochila
        print_step("Paso 4: Definir la restricción de capacidad", file=stream)
        problema_mochila += sum(self.pesos[i] * x[i] for i in range(self.pesos_count)) <= self.capacidad, "Capacidad_mochila"
        print(f"Restricción de capacidad formulada: La suma de los pesos no debe exceder {self.capacidad} kg.", file=stream)

        # Paso 5: Resolver el problema
        print_step("Paso 5: Resolver el problema", file=stream)
        problema_mochila.solve()
        print(f"Estado de la solución: {pulp.LpStatus[problema_mochila.status]}", file=stream)

        # Paso 6: Mostrar los valores óptimos de las variables (objetos seleccionados)
        print_step("Paso 6: Mostrar los objetos seleccionados", file=stream)
        for i in range(self.pesos_count):
            print(f"Objeto {i+1}: {'Seleccionado' if x[i].varValue == 1 else 'No seleccionado'} (Peso: {self.pesos[i]}, Valor: {self.valores[i]})", file=stream)

        # Paso 7: Calcular y mostrar el valor total en la mochila y el peso total
        valor_total = sum(self.valores[i] * x[i].varValue for i in range(self.pesos_count))
        peso_total = sum(self.pesos[i] * x[i].varValue for i in range(self.pesos_count))
        print_step(f"Paso 7: Resultados finales", file=stream)
        print(f"Valor total en la mochila: {valor_total}", file=stream)
        print(f"Peso total en la mochila: {peso_total}", file=stream)

        stream.seek(0)
        self.output = list(stream.readlines())
        sys.stdout.writelines(self.output)

    def exportar(self):
        nombre = input_str("Indique un nombre para el archivo de salida")
        if not nombre.endswith(".txt"):
            nombre = nombre + ".txt"
        with open(f"04 Mochila - {nombre}", "w") as f:
            f.writelines(self.output)

    def resolver(self):
        self.leer_input()
        self.encontrar_solucion()
        self.exportar()


if __name__ == "__main__":
    print_title("Método Mochila")

    MetodoMochila().resolver()

