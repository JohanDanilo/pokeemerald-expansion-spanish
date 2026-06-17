import json
import os
import sys

ARCHIVO_MAESTRO = "traduccion/textos_data_text.json"
CARPETA_LOTES = "traduccion/lotes"

if len(sys.argv) != 3:
    print(
        "Uso:\n"
        "python3 traduccion/exportar_lote.py INICIO FIN"
    )
    sys.exit(1)

inicio = int(sys.argv[1])
fin = int(sys.argv[2])

os.makedirs(CARPETA_LOTES, exist_ok=True)

with open(ARCHIVO_MAESTRO, encoding="utf-8") as f:
    datos = json.load(f)

lote = [
    item
    for item in datos
    if inicio <= item["id_num"] <= fin
]

nombre = (
    f"lote_{inicio:04d}_{fin:04d}.json"
)

ruta_salida = os.path.join(
    CARPETA_LOTES,
    nombre
)

with open(
    ruta_salida,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        lote,
        f,
        ensure_ascii=False,
        indent=2
    )

print(
    f"Lote exportado: {ruta_salida}"
)

print(
    f"Entradas exportadas: {len(lote)}"
)