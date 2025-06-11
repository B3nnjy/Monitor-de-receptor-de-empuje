import random
import time
from datetime import datetime
from save_data import guardar_datos


"""Simula la lectura continua de datos de un puerto serial generando números aleatorios"""

def serial_reader_simulado(data_queue):
    try:
        while True:
            # Simular un valor de empuje aleatorio entre 0 y 100 (en kg)
            empuje = random.uniform(0, 150)
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            
            # Guardar los datos en la cola
            data_queue.put((timestamp, empuje))
            
            # Imprimir para mostrar el valor simulado
            print(f"{timestamp} | Empuje: {empuje:.2f} kg")
            
            # Pausar un momento antes de generar el siguiente valor (simulando un intervalo de lectura)
            time.sleep(1)
    except Exception as e:
        print(f"Error en la simulación de lectura: {e}")
    finally:
        print("Hilo de lectura simulado terminado")
