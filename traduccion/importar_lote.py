import json
import sys

ARCHIVO_MAESTRO = "traduccion/textos_data_text.json"

if len(sys.argv) != 2:
    print(
        "Uso:\n"
        "python3 traduccion/importar_lote.py archivo_lote.json"
    )
    sys.exit(1)

archivo_lote = sys.argv[1]

with open(
    ARCHIVO_MAESTRO,
    encoding="utf-8"
) as f:
    maestro = json.load(f)

with open(
    archivo_lote,
    encoding="utf-8"
) as f:
    lote = json.load(f)

indice = {
    item["id_num"]: item
    for item in maestro
}

actualizados = 0

for entrada in lote:

    id_num = entrada["id_num"]

    if id_num not in indice:
        continue

    indice[id_num]["spanish"] = entrada["spanish"]

    indice[id_num]["translated"] = entrada["translated"]

    indice[id_num]["reviewed"] = entrada["reviewed"]

    actualizados += 1

with open(
    ARCHIVO_MAESTRO,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        maestro,
        f,
        ensure_ascii=False,
        indent=2
    )

print(
    f"Entradas actualizadas: {actualizados}"
)