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
        contenido = f.read()

    for entrada in entradas:
        identificador = entrada["id"]
        nuevas_lineas = entrada["spanish_lines"]

        patron_bloque = (
            rf"(^{re.escape(identificador)}\s*:\s*\n)"
            rf"((?:[ \t]+\.string \"[^\"]*\"\n)*)"
        )

        match = re.search(
            patron_bloque,
            contenido,
            re.MULTILINE
        )

        if not match:
            print(f"  ❌ No encontrado: {identificador}")
            continue

        reemplazo_strings = ""
        for texto in nuevas_lineas:
            # Opción 2: Omitir comillas dobles internas
            texto_escapado = texto.replace('"', '')
            
            reemplazo_strings += f'        .string "{texto_escapado}"\n'

        nuevo_bloque = match.group(1) + reemplazo_strings

        contenido = contenido[:match.start()] + nuevo_bloque + contenido[match.end():]

        print(f"  ✅ Actualizado: {identificador}")

    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(contenido)

print("\n✅ Inyección finalizada.")