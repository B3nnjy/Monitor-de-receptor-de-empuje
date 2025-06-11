import json

def guardar_datos(data_queue):
    datos_guardados = []
    
    for tiempo, empuje in data_queue:
        nuevo_dato = {
            "tiempo": str(tiempo),
            "empuje": str(empuje)
        }
        datos_guardados.append(nuevo_dato)
    
    with open("datos.json", "w") as f:
        json.dump(datos_guardados, f, indent=4)
