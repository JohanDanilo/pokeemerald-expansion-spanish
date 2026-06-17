import json
import re

ARCHIVO_JSON = "traduccion/textos_data_text.json"

patron_variables = re.compile(r"\{[^}]+\}")
patron_control = re.compile(r"(\\n|\\p|\\l|\$)")


def extraer_variables(texto):
    return sorted(set(patron_variables.findall(texto)))


def extraer_controles(texto):
    return sorted(set(patron_control.findall(texto)))


with open(ARCHIVO_JSON, encoding="utf-8") as f:
    datos = json.load(f)

errores = []

for entrada in datos:

    if not entrada.get("translated", False):
        continue

    english = entrada["english"]
    spanish = entrada["spanish"]

    vars_en = extraer_variables(english)
    vars_es = extraer_variables(spanish)

    ctrl_en = extraer_controles(english)
    ctrl_es = extraer_controles(spanish)

    if vars_en != vars_es:

        errores.append({
            "id_num": entrada["id_num"],
            "id": entrada["id"],
            "tipo": "variables",
            "esperadas": vars_en,
            "encontradas": vars_es
        })

    if ctrl_en != ctrl_es:

        errores.append({
            "id_num": entrada["id_num"],
            "id": entrada["id"],
            "tipo": "control_codes",
            "esperados": ctrl_en,
            "encontrados": ctrl_es
        })

print("\n========== VALIDACIÓN ==========\n")

if not errores:
    print("No se encontraron errores.")
else:

    print(f"Errores encontrados: {len(errores)}\n")

    for error in errores[:50]:

        print(
            f"[{error['tipo']}] "
            f"{error['id_num']} - {error['id']}"
        )

        if error["tipo"] == "variables":

            print(
                f"  Esperadas : {error['esperadas']}"
            )

            print(
                f"  Encontradas: {error['encontradas']}"
            )

        if error["tipo"] == "control_codes":

            print(
                f"  Esperados : {error['esperados']}"
            )

            print(
                f"  Encontrados: {error['encontrados']}"
            )

        print()

print("\n================================")