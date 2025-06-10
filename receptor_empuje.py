import serial
import time
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import queue
import random


PORT = 'COM3'       
BAUDRATE = 250000


plt.style.use('ggplot')
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)



data_queue = queue.Queue()
start_time = time.time()
x_data = []
y_data = []

def serial_reader_simulado():
    """Simula la lectura continua de datos de un puerto serial generando números aleatorios"""
    try:
        while True:
            # Simular un valor de empuje aleatorio entre 0 y 100 (en kg)
            empuje = random.uniform(0, 150)
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            
            # Guardar los datos en la cola
            data_queue.put((time.time() - start_time, empuje))
            
            # Imprimir para mostrar el valor simulado
            #print(f"{timestamp} | Empuje: {empuje:.2f} kg")
            
            # Pausar un momento antes de generar el siguiente valor (simulando un intervalo de lectura)
            time.sleep(1)
    except Exception as e:
        print(f"Error en la simulación de lectura: {e}")
    finally:
        print("Hilo de lectura simulado terminado")


def serial_reader():
    """Hilo para lectura continua de datos serial"""
    try:
        with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
            print(f"Conectado a {ser.name}")
            
            with open('datos_empuje.csv', 'a') as f:
                f.write("Timestamp,Empuje(kg)\n")
                
                while True:
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
                                    
                                    # Guardar en CSV
                                    f.write(f"{timestamp},{valor:.2f}\n")
                                    
                                    # Poner en cola para el gráfico
                                    data_queue.put((time.time() - start_time, valor))
                                    
                                    print(f"{timestamp} | Empuje: {valor:.2f} kg")
                        except Exception as e:
                            print(f"Error procesando dato: {e}")
    except serial.SerialException as e:
        print(f"Error de conexión: {e}")
    finally:
        print("Hilo serial terminado")
    
    pass


# Contador para el eje x
cont = 0
x_data = list(range(11))
y_data = [0] * 11 

def update(frame):
    """Actualizar gráfico con nuevos datos"""
    global cont
    global x_data, y_data
    while not data_queue.empty():
        t, valor = data_queue.get()
        # Asegurar que el eje x tenga un rango adecuado
        if cont > 10:
            y_data.pop(0)  # Eliminar el primer valor
            y_data.append(valor)
            x_data.pop(0)
            x_data.append(cont)
        else:
            print(x_data[cont])
            y_data.pop(-1)
            y_data.insert(x_data[cont], valor)
        cont += 1
        
        print("Datos:", x_data, y_data)  # Debug
        
    
    if x_data and y_data:
        fig.canvas.draw_idle()
        line.set_data(x_data, y_data)
        
        # Ajuste de límites con margen
        y_min, y_max = min(y_data), max(y_data)
        x_min, x_max = min(x_data), max(x_data)

        print(f"Límites: x({x_min}, {x_max}), y({y_min}, {y_max})")  # Debug
        
        y_margin = 0.1 * (y_max - y_min) if y_max != y_min else 0.1
        x_margin = 0.1 * (x_max - x_min) if x_max != x_min else 0.1
        
        
        ax.set_xlim(x_min - x_margin, x_max + x_margin)

        ax.set_ylim(y_min - y_margin, y_max + y_margin)
          # Forzar marcas de 1 en 1 en ambos ejes
        ax.set_xticks(range(x_min, x_max + 1))  # +1 para incluir el último valor
    
    return line,

def init_plot():
    """Inicializar gráfico"""
    ax.set_title("Monitor de Empuje en Tiempo Real")
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Empuje (kg)")
    ax.grid(True)

    return line,

if __name__ == "__main__":
    
    serial_thread = threading.Thread(target=serial_reader_simulado, daemon=True)
    serial_thread.start()
    
    
    ani = FuncAnimation(fig, update, init_func=init_plot, 
                        interval=50, blit=False)
    
    try:
        plt.show()
    except KeyboardInterrupt:
        print("\nPrograma terminado por usuario")
    finally:
        print("Guardando datos...")