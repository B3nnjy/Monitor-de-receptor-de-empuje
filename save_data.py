import csv
from datetime import datetime

def guardar_datos(data_queue):
    if not data_queue:
        print("La lista de datos está vacía. No se guardará ningún archivo.")
        return

    # Obtener timestamp para el nombre del archivo
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"datos_{timestamp}.csv"

    with open(nombre_archivo, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["tiempo", "empuje"])  # Escribir encabezados

        for tiempo, empuje in data_queue:
            writer.writerow([tiempo, empuje])

    print(f"Datos guardados en: {nombre_archivo}")
