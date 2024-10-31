import io
import pulp
import re
import sys
from typing import List, Tuple
from helper import *


class MetodoRamificacionEntera:
    def __init__(self):
        self.problem = None
        self.variables = []
        self.restricciones = []
        self.objective = None
        # self.output = []
        self.stream = None

    def leer_input(self):
        self.stream = io.StringIO()

        print_step("Parte 1: Crear problema", file=self.stream)

        raw = input_re(
            "Ingrese las variables de decisión separadas por comas (ej. x1,x2,x3)", 
            re.compile(r'^[a-zA-Z]\d+(,[a-zA-Z]\d+)*$'), 
            err = "Entrada inválida.")
        self.variables = raw.split(',')
        print("Variables:", self.variables, file=self.stream)

        # Solicitar restricciones
        print("Ingrese las restricciones (una por línea). Presione Enter sin escribir nada para finalizar.")
        print("Formato: 2*x1 + 3*x2 <= 10 o 2*x1 + 3*x2 >= 10 o 2*x1 + 3*x2 = 10")
        while True:
            restr_raw = input_str("Restricción (formato: 2*x1 + 3*x2 <= 10 o 2*x1 + 3*x2 >= 10 o 2*x1 + 3*x2 = 10)")
            if restr_raw == "":
                break
            if self._validar_restriccion(restr_raw):
                self.restricciones.append(restr_raw)
                print(f"Restricción {len(self.restricciones)}:", restr_raw, file=self.stream)
            else:
                print_err("Restricción inválida. Por favor, intente de nuevo.")

        # Solicitar objetivo
        self.objective = input_option("¿Desea maximizar o minimizar?", ['max', 'min'])
        print(f"Tipo:", self.objective, file=self.stream)

        # Solicitar función objetivo
        while True:
            fn_objetivo = input_str("Ingrese la función objetivo (ej. 70*x1 + 100*x2 o 70x1 + 100x2): ")
            if self._validar_expresion(fn_objetivo):
                self.funcion_objectivo = fn_objetivo
                print(f"Función Objetivo:", fn_objetivo, file=self.stream)
                break
            else:
                print_err("Función objetivo inválida. Por favor, intente de nuevo.")

        self.problem = pulp.LpProblem("MetodoRamificacionEntera", pulp.LpMaximize if self.objective == 'max' else pulp.LpMinimize)

        lp_vars = {var: pulp.LpVariable(var, lowBound=0, cat='Integer') for var in self.variables}

        self.problem += pulp.LpAffineExpression(self.interpretar_expresion(self.funcion_objectivo, lp_vars))

        for constraint in self.restricciones:
            parts = re.split(r'\s*([<>=]=)\s*', constraint)
            if len(parts) != 3:
                print_err(f"Error en la restricción: {constraint}")
                continue
            lhs, operator, rhs = parts
            sense = pulp.LpConstraintLE if operator == '<=' else pulp.LpConstraintGE if operator == '>=' else pulp.LpConstraintEQ
            self.problem += pulp.LpConstraint(
                e=pulp.LpAffineExpression(self.interpretar_expresion(lhs, lp_vars)),
                sense=sense,
                rhs=float(rhs)
            )

    def _validar_restriccion(self, constraint: str) -> bool:
        pattern = r'^(\s*-?\s*\d*\.?\d*\s*\*?\s*[a-zA-Z]\d+\s*[+\-]?\s*)*\s*[<>=]=\s*-?\d+\.?\d*$'
        return re.match(pattern, constraint) is not None

    def _validar_expresion(self, expr: str) -> bool:
        pattern = r'^(\s*-?\s*\d*\.?\d*\s*\*?\s*[a-zA-Z]\d+\s*[+\-]?\s*)*\s*\d*\.?\d*\s*\*?\s*[a-zA-Z]\d+$'
        return re.match(pattern, expr) is not None

    def interpretar_expresion(self, expr: str, lp_vars: dict) -> List[Tuple[pulp.LpVariable, float]]:
        terminos = re.findall(r'(-?\s*\d*\.?\d*\s*\*?\s*[a-zA-Z]\d+)', expr)
        terminos_interpretados = []
        for term in terminos:
            if '*' in term:
                k, var = term.split('*')
            else:
                k, var = re.match(r'(-?\s*\d*\.?\d*\s*)([a-zA-Z]\d+)', term).groups()
            k = float(k.strip()) if k.strip() != '' else 1.0
            var = var.strip()
            terminos_interpretados.append((lp_vars[var], k))
        return terminos_interpretados

    def encontrar_solucion(self):
        print_step("Parte 2: Resolviendo el problema usando el algoritmo de ramificación y cortes", file=self.stream)
        
        # Configurar el solucionador con opciones específicas
        solver = pulp.PULP_CBC_CMD(msg=1, presolve=True, cuts=True, strong=True)
        status = self.problem.solve(solver)
    
        print_step("Parte 3: Resolver", file=self.stream)
        print(f"Estado de la solución: {pulp.LpStatus[status]}", file=self.stream)

        print_step("Parte 4: Detalles de la solución", file=self.stream)
        print(f"Valor objetivo: {pulp.value(self.problem.objective)}", file=self.stream)
        print(f"Valores de las variables:", file=self.stream)
        for var in self.problem.variables():
            print(f"{var.name} = {var.varValue}", file=self.stream)

    def exportar(self):
        self.stream.seek(0)
        output = list(self.stream.readlines())
        sys.stdout.writelines(output)

        nombre = input_str("Indique un nombre para el archivo de salida")
        if not nombre.endswith(".txt"):
            nombre = nombre + ".txt"
        with open(f"01 RamificacionEntera - {nombre}", "w") as f:
            f.writelines(output)

    def resolver(self):
        self.leer_input()
        self.encontrar_solucion()
        self.exportar()


if __name__ == "__main__":
    print_title("Ramificación Entera")

    MetodoRamificacionEntera().resolver()
    

