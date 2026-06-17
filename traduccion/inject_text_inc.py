import json
import re
from collections import defaultdict

ARCHIVO_JSON = "traduccion/textos_data_text.json"

with open(ARCHIVO_JSON, encoding="utf-8") as f:
    datos = json.load(f)

traducidos = [
    x for x in datos
    if x.get("translated", False)
       and x.get("spanish_lines")
]

por_archivo = defaultdict(list)

for entrada in traducidos:
    por_archivo[entrada["archivo"]].append(entrada)

for ruta_archivo, entradas in por_archivo.items():

    print(f"\nProcesando: {ruta_archivo}")

    with open(ruta_archivo, encoding="utf-8") as f:
        lineas = f.readlines()

    for entrada in entradas:

        identificador = entrada["id"]
        nuevas_lineas = entrada["spanish_lines"]

        inicio = None

        patron = re.compile(
            rf"^\s*{re.escape(identificador)}::?\s*$"
        )

        for i, linea in enumerate(lineas):

            if patron.match(linea):
                inicio = i
                break

        if inicio is None:
            print(f"No encontrado: {identificador}")
            continue

        j = inicio + 1

        while (
            j < len(lineas)
            and '.string "' in lineas[j]
        ):
            j += 1

        reemplazo = []

        for texto in nuevas_lineas:

            reemplazo.append(
                f'        .string "{texto}"\n'
            )

        lineas[inicio + 1:j] = reemplazo

        print(
            f"Actualizado: {identificador}"
        )

    with open(
        ruta_archivo,
        "w",
        encoding="utf-8"
    ) as f:

        f.writelines(lineas)

print("\nInyección finalizada.")