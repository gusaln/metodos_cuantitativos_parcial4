from pulp import LpMaximize, LpProblem, LpVariable, LpStatus, value, PULP_CBC_CMD, LpMinimize


### Funciones para facilitar IO

def print_err(err: str):
    print("ERROR: ", err)

def print_info(err: str):
    print("INFO: ", err)

def print_title(text: str):
    border_width = 2
    margin_width = 1
    offset = border_width*2 + margin_width*2
    min_size = 80


    text = text.strip()
    text_l = len(text)

    # Length of the title with margins and border
    l = max(min_size, text_l + offset)

    needed_space = l - text_l - offset
    left_margin = needed_space // 2
    right_margin = needed_space - left_margin

    print()
    print()
    print("#" * l)
    print(f"{"#"*border_width} {" "*left_margin}{text}{" "*right_margin} {"#"*border_width}")
    print("#" * l)
    print()


def print_section(text: str):
    text = text.strip()

    print()
    print()
    print(f":: {text} ::")
    print()

def print_step(text: str):
    text = text.strip()

    print()
    print(f"--- {text} ---")

def input_option(m: str, options: list):
    mapped = dict(enumerate(options))

    while True:
        print(m.strip(), ": ")
        for i, op in mapped.items():
            print(f"[{i}] {op}")
        raw = input_int("indique el [n]úmero de la opción")

        if raw in mapped:
            return mapped[raw]
        
        print_err(f"{raw} no es una opción válida")
        


def input_str(m: str):
    return input(f"--> {m}: ").strip()


def input_int(m: str):
    while True:
        raw = input_str(m)

        try:
            return int(raw)
        except ValueError:
            print_err(f"'{raw}' debe ser número un entero")


def input_float(m: str):
    while True:
        raw = input_str(m)

        try:
            return float(raw.replace(",", "."))
        except ValueError:
            print_err(f"'{raw}' debe ser número un decimal")

# def input_array(m: str, count: int, transform: None):
#     while True:
#         raw = input_str(m)
#         parts = [s.strip() for s in raw.split(",")]
#         if len(parts) != count:
#             print_err(f"no se indicó el número correcto de valores ({count})")
#             continue

#         for i, vi in enumerate(parts):
#             try:
#                 if transform is None:
#                     pesos[i] = vi
#                 else:
#                     pesos[i] = transform(vi)
#             except Exception:
#                 print_err(f"'{vi}' no es válido")
#                 break
#         else:
#             continue
        
#         break

### Modelos

def resolver_mochila():
    print_section("El problema de la mochila")

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

    # Paso 1: Crear el problema de maximización
    print_step("Paso 1: Crear el problema de maximización")
    problema_mochila = LpProblem("Problema_de_la_Mochila", LpMaximize)
    
    # Paso 2: Definir las variables de decisión (0 o 1 para cada objeto)
    print_step("Paso 2: Definir las variables de decisión")
    x = [LpVariable(f"x_{i+1}", cat='Binary') for i in range(pesos_count)]
    print("Variables de decisión definidas (0 = no seleccionado, 1 = seleccionado):")
    for i in range(pesos_count):
        print(f"x_{i+1} -> Objeto {i+1}")

    # Paso 3: Definir la función objetivo (maximizar el valor total)
    print_step("Paso 3: Definir la función objetivo")
    problema_mochila += sum(valores[i] * x[i] for i in range(pesos_count)), "Valor_total"
    print("Función objetivo formulada: Maximizar el valor total de los objetos seleccionados.")

    # Paso 4: Definir la restricción de capacidad de la mochila
    print_step("Paso 4: Definir la restricción de capacidad")
    problema_mochila += sum(pesos[i] * x[i] for i in range(pesos_count)) <= capacidad, "Capacidad_mochila"
    print(f"Restricción de capacidad formulada: La suma de los pesos no debe exceder {capacidad} kg.")

    # Paso 5: Resolver el problema
    print_step("Paso 5: Resolver el problema")
    problema_mochila.solve()
    print(f"Estado de la solución: {LpStatus[problema_mochila.status]}")

    # Paso 6: Mostrar los valores óptimos de las variables (objetos seleccionados)
    print_step("Paso 6: Mostrar los objetos seleccionados")
    for i in range(pesos_count):
        print(f"Objeto {i+1}: {'Seleccionado' if x[i].varValue == 1 else 'No seleccionado'} (Peso: {pesos[i]}, Valor: {valores[i]})")

    # Paso 7: Calcular y mostrar el valor total en la mochila y el peso total
    valor_total = sum(valores[i] * x[i].varValue for i in range(pesos_count))
    peso_total = sum(pesos[i] * x[i].varValue for i in range(pesos_count))
    print_step(f"Paso 7: Resultados finales")
    print(f"Valor total en la mochila: {valor_total}")
    print(f"Peso total en la mochila: {peso_total}")

# Datos del problema de la mochila
pesos = [3, 6, 5, 5, 7]       # Pesos de los objetos
valores = [15, 25, 12, 10, 15]  # Valores de los objetos
capacidad = 120              # Capacidad máxima de la mochila

if __name__ == "__main__":
    print_title("Menú")

    problema = input_option("Indique el tipo de problema a resolver", ["mochila"])

    if problema == "mochila":
        resolver_mochila()
    

