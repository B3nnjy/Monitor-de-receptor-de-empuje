import serial
import time
from datetime import datetime

def serial_reader(data_queue, PORT='COM3', BAUDRATE=250000):
    """Hilo para lectura continua de datos serial"""
    try:
        with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
            print(f"Conectado a {ser.name}")

            last_time = time.time()
            
            while True:
                curret_time = time.time()
                # Leer datos cada segundo
                if curret_time - last_time >= 1:
                    if ser.in_waiting > 0:
                        try:
                            # Leer y decodificar línea
                            linea = ser.readline().decode('utf-8').strip()
                            
                            if linea and linea.startswith('Empuje:'):
                                # Extraer valor numérico
                                parts = linea.split()
                                if len(parts) >= 2:
                                    valor = float(parts[1])
                                    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                                    
                                    # Poner en cola para el gráfico u otro procesamiento
                                    data_queue.put((timestamp, valor))
                                    
                                    print(f"{timestamp} | Empuje: {valor:.2f} kg")
                        except Exception as e:
                            print(f"Error procesando dato: {e}")
                            
    except serial.SerialException as e:
        print(f"Error de conexión: {e}")
    finally:
        print("Hilo serial terminado")
