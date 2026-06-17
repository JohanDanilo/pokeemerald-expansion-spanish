import os
import re
import json
from collections import Counter

CARPETA = "data/text"

patron_id = re.compile(r"^\s*([A-Za-z0-9_]+):{1,2}\s*$")
patron_string = re.compile(r'\.string\s+"(.*)"')

resultados = []
contador_global = 1

def extraer_variables(texto):
    return sorted(
        set(
            re.findall(r"\{[^}]+\}", texto)
        )
    )

def extraer_controles(texto):
    return sorted(
        set(
            re.findall(r"(\\n|\\p|\\l|\$)", texto)
        )
    )


def guardar_texto(identificador, ruta, lineas_texto):
    global contador_global

    if not identificador or not lineas_texto:
        return

    texto = "".join(lineas_texto)

    resultados.append({
        "id_num": contador_global,

        "id": identificador,

        "archivo": ruta,

        "english": texto,

        "english_lines": lineas_texto.copy(),

        "spanish": "",

        "spanish_lines": [],

        "variables": extraer_variables(texto),

        "control_codes": extraer_controles(texto),

        "english_length": len(texto),

        "translated": False,

        "reviewed": False
    })

    contador_global += 1


for raiz, _, archivos in os.walk(CARPETA):

    archivos.sort()

    for archivo in archivos:

        if not archivo.endswith(".inc"):
            continue

        ruta = os.path.join(raiz, archivo)

        with open(ruta, encoding="utf-8", errors="ignore") as f:

            identificador = None
            lineas_texto = []

            for linea in f:

                m_id = patron_id.match(linea)

                if m_id:

                    guardar_texto(
                        identificador,
                        ruta,
                        lineas_texto
                    )

                    identificador = m_id.group(1)
                    lineas_texto = []

                    continue

                m_string = patron_string.search(linea)

                if m_string:
                    lineas_texto.append(
                        m_string.group(1)
                    )

            guardar_texto(
                identificador,
                ruta,
                lineas_texto
            )

with open(
    "traduccion/textos_data_text.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        resultados,
        f,
        ensure_ascii=False,
        indent=2
    )

contador = Counter()

for item in resultados:
    contador[item["archivo"]] += 1

print("\nTop archivos:")

for archivo, cantidad in contador.most_common(20):
    print(f"{cantidad:5d}  {archivo}")

print(f"\nExtraídos {len(resultados)} textos.")
print("Archivo generado: traduccion/textos_data_text.json")