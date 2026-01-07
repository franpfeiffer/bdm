import json
import csv

# Leer el CSV y crear un mapeo de CUIT -> Teléfono
cuit_to_phone = {}
with open('vacunas.csv', 'r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    next(reader)  # Saltar el header
    for row in reader:
        if len(row) >= 9:
            cuit = row[7].strip()  # Columna CUIT
            telefono = row[8].strip()  # Columna Teléfono
            if cuit and telefono:
                cuit_to_phone[cuit] = telefono

print(f"Mapeados {len(cuit_to_phone)} CUITs a teléfonos")

# Leer el JSON
with open('data/vacunatorios_coordinates_con_barrios.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# Actualizar los teléfonos
updated_count = 0
not_found_count = 0
not_found_cuits = set()

# Los datos están en json_data['data']
data = json_data.get('data', [])

for item in data:
    if 'telefono' in item:
        current_value = item['telefono']
        # Si el valor actual está en el mapeo (es un CUIT), reemplazarlo
        if current_value in cuit_to_phone:
            item['telefono'] = cuit_to_phone[current_value]
            updated_count += 1
        else:
            # Verificar si parece un CUIT (formato XX-XXXXXXXX-X)
            if current_value and '-' in current_value and len(current_value.split('-')) == 3:
                not_found_count += 1
                not_found_cuits.add(current_value)

print(f"Actualizados: {updated_count}")
print(f"CUITs no encontrados en el CSV: {not_found_count}")
if not_found_cuits:
    print(f"Ejemplos de CUITs no encontrados: {list(not_found_cuits)[:5]}")

# Guardar el JSON actualizado
with open('data/vacunatorios_coordinates_con_barrios.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

print("JSON actualizado exitosamente!")
