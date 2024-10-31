### Funciones para facilitar IO

import re


def print_err(err: str, **kwargs):
    print("ERROR: ", err, **kwargs)

def print_info(err: str, **kwargs):
    print("INFO: ", err, **kwargs)

def print_title(text: str, **kwargs):
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

    print(**kwargs)
    print(**kwargs)
    print("#" * l, **kwargs)
    print(f"{"#"*border_width} {" "*left_margin}{text}{" "*right_margin} {"#"*border_width}", **kwargs)
    print("#" * l, **kwargs)
    print(**kwargs)


def print_section(text: str, **kwargs):
    text = text.strip()

    print(**kwargs)
    print(**kwargs)
    print(f":: {text} ::", **kwargs)
    print(**kwargs)

def print_step(text: str, **kwargs):
    text = text.strip()

    print(**kwargs)
    print(f"--- {text} ---", **kwargs)

def input_option(m: str, options: list):
    mapped = dict(enumerate(options))

    while True:
        print(m.strip(), ": ")
        for i, op in mapped.items():
            print(f"[{i}] {op}")
        raw = input_int("indique el [n]úmero de la opción")

        if raw in mapped:
            print()
            return mapped[raw]
        
        print_err(f"{raw} no es una opción válida")
        


def input_str(m: str):
    raw = input(f"--> {m}: ").strip()
    print()
    return raw

def input_re(m: str, pattern: re.Pattern, err: str = None):
    while True:
        raw = input(f"--> {m}: ").strip()

        if re.match(pattern, raw):
            print()
            return raw
        print_err(err if err is not None else f"'{raw}' no es válido")
        

def input_int(m: str):
    while True:
        raw = input_str(m)

        try:
            res =  int(raw)
            print()
            return res
        except ValueError:
            print_err(f"'{raw}' debe ser número un entero")


def input_float(m: str):
    while True:
        raw = input_str(m)

        try:
            res = float(raw.replace(",", "."))
            print()
            return res
        except ValueError:
            print_err(f"'{raw}' debe ser número un decimal")