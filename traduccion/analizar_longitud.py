import json

ARCHIVO = "traduccion/textos_data_text.json"

LIMITE = 37

with open(ARCHIVO, encoding="utf-8") as f:
    datos = json.load(f)

problemas = []

for entrada in datos:

    if not entrada.get("translated", False):
        continue

    for i, linea in enumerate(
        entrada.get("spanish_lines", [])
    ):

        texto = (
            linea
            .replace("\\n", "")
            .replace("\\p", "")
            .replace("\\l", "")
            .replace("$", "")
        )

        longitud = len(texto)

        if longitud > LIMITE:

            problemas.append({
                "id_num": entrada["id_num"],
                "id": entrada["id"],
                "linea": i + 1,
                "longitud": longitud,
                "texto": texto
            })

print("\n===== LÍNEAS POTENCIALMENTE LARGAS =====\n")

if not problemas:
    print("No se encontraron líneas largas.")
else:

    print(f"Total: {len(problemas)}\n")

    for p in problemas[:100]:

        print(
            f"[{p['longitud']:02d}] "
            f"{p['id_num']} "
            f"{p['id']} "
            f"(línea {p['linea']})"
        )

        print(f"  {p['texto']}\n")