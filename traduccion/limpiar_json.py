# limpiar_json.py
import json

ARCHIVO_JSON = "textos_data_text.json"

with open(ARCHIVO_JSON, encoding="utf-8") as f:
    datos = json.load(f)

for entrada in datos:
    # Limpiar comillas dobles de english_lines
    entrada["english_lines"] = [
        linea.replace('"', '') 
        for linea in entrada.get("english_lines", [])
    ]
    
    # Reconstruir english sin comillas
    entrada["english"] = "".join(
        entrada["english_lines"]
    )

with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
    json.dump(datos, f, ensure_ascii=False, indent=2)

print("✅ JSON maestro limpiado de comillas dobles.")