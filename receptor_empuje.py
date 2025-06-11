import serial
import time
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import queue
from save_data import guardar_datos  # Importar la función de guardado

from serial_simulado import serial_reader_simulado  # Importar la función simulada
from serial_reader import serial_reader  # Importar la función real si se desea usarla


plt.style.use('ggplot')
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)



data_queue = queue.Queue()
start_time = time.time()
x_data = []
y_data = []

# Contador para el eje x
cont = 0
x_data = list(range(11))
y_data = [0] * 11 

data_save = []  # Lista para guardar datos

def update(frame):
    """Actualizar gráfico con nuevos datos"""
    global cont
    global x_data, y_data
    while not data_queue.empty():
        t, valor = data_queue.get()
        strTime = str(t)
        data_save.append((strTime, valor))



        print(f"Tiempo: {strTime} s | Empuje: {valor:.2f} kg")

        # Asegurar que el eje x tenga un rango adecuado
        if cont > 10:
            y_data.pop(0)  # Eliminar el primer valor
            y_data.append(valor)
            x_data.pop(0)
            x_data.append(cont)
        else:
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
    
    serial_thread = threading.Thread(target=serial_reader, args=(data_queue, ),daemon=True)
    serial_thread.start()
    
    
    ani = FuncAnimation(fig, update, init_func=init_plot, 
                        interval=50, blit=False)
    
    try:
        plt.show()
    except KeyboardInterrupt:
        print("\nPrograma terminado por usuario")
    finally:
        guardar_datos(data_save,)  # Guardar los datos al finalizar
        print("Datos guardados correctamente.")