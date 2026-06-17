import json
import re

ARCHIVO_JSON = "traduccion/textos_data_text.json"

with open(ARCHIVO_JSON, encoding="utf-8") as f:
    datos = json.load(f)

for entrada in datos:
    # Limpiar TODAS las variantes de comillas
    if entrada.get("spanish_lines"):
        entrada["spanish_lines"] = [
            linea.replace('\\"', '')      # Comillas escapadas
                  .replace('"', '')        # Comillas normales
            for linea in entrada["spanish_lines"]
        ]
    
    if entrada.get("english_lines"):
        entrada["english_lines"] = [
            linea.replace('\\"', '')
                  .replace('"', '')
            for linea in entrada["english_lines"]
        ]
    
    # Reconstruir
    entrada["spanish"] = "".join(entrada.get("spanish_lines", []))
    entrada["english"] = "".join(entrada.get("english_lines", []))

with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
    json.dump(datos, f, ensure_ascii=False, indent=2)

print("✅ JSON maestro limpiado (comillas + escapes).")
