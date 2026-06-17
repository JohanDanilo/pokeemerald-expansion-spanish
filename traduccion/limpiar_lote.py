import json
import sys

if len(sys.argv) != 2:
    print("Uso: python3 traduccion/limpiar_lote.py archivo_lote.json")
    sys.exit(1)

archivo_lote = sys.argv[1]

with open(archivo_lote, encoding="utf-8") as f:
    lote = json.load(f)

for entrada in lote:
    # Limpiar comillas dobles de spanish_lines
    entrada["spanish_lines"] = [
        linea.replace('"', '') 
        for linea in entrada.get("spanish_lines", [])
    ]
    
    # Reconstruir spanish sin comillas
    entrada["spanish"] = "".join(entrada["spanish_lines"])

with open(archivo_lote, "w", encoding="utf-8") as f:
    json.dump(lote, f, ensure_ascii=False, indent=2)

print(f"✅ Lote limpiado: {archivo_lote}")
