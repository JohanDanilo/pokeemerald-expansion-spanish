import json

ARCHIVO_JSON = "traduccion/textos_data_text.json"

with open(ARCHIVO_JSON, encoding="utf-8") as f:
    datos = json.load(f)

for entrada in datos:
    # Limpiar TODAS las comillas dobles de TODOS los campos
    if entrada.get("english_lines"):
        entrada["english_lines"] = [
            linea.replace('"', '') 
            for linea in entrada["english_lines"]
        ]
    
    if entrada.get("spanish_lines"):
        entrada["spanish_lines"] = [
            linea.replace('"', '') 
            for linea in entrada["spanish_lines"]
        ]
    
    # Reconstruir campos completos
    entrada["english"] = "".join(entrada.get("english_lines", []))
    entrada["spanish"] = "".join(entrada.get("spanish_lines", []))

with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
    json.dump(datos, f, ensure_ascii=False, indent=2)

print("✅ JSON maestro limpiado (post-importar).")
