import json

# Leer el JSON
with open('data/vacunatorios_coordinates_con_barrios.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# Normalizar los barrios
data = json_data.get('data', [])
updated_count = 0

for item in data:
    if 'barrio' in item and item['barrio']:
        original = item['barrio']
        # Normalizar a Title Case
        normalized = item['barrio'].title()
        if original != normalized:
            item['barrio'] = normalized
            updated_count += 1

print(f"Barrios normalizados: {updated_count}")

# Guardar el JSON actualizado
with open('data/vacunatorios_coordinates_con_barrios.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

print("JSON actualizado exitosamente!")

# Verificar que no hay duplicados
from collections import defaultdict
barrios = defaultdict(list)
for item in data:
    if 'barrio' in item and item['barrio']:
        barrio = item['barrio']
        barrio_lower = barrio.lower()
        barrios[barrio_lower].append(barrio)

duplicados = {k: list(set(v)) for k, v in barrios.items() if len(set(v)) > 1}
print(f"\nBarrios con duplicados después de normalizar: {len(duplicados)}")
if duplicados:
    print("Ejemplos:", list(duplicados.items())[:5])
