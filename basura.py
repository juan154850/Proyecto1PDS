
# -------------------------
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from scipy.signal import square
import sounddevice as sd

# Función para generar la señal de sonido
def generar_senal():
    frecuencia = float(frecuencia_entry.get())
    duracion = float(duracion_entry.get())

    tiempo = np.linspace(0, duracion, int(44100 * duracion), endpoint=False)
    señal = square(2 * np.pi * frecuencia * tiempo)

    # Visualizar la señal
    plt.plot(tiempo, señal)
    plt.title('Señal Generada')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.show()

    # Guardar la señal en una variable global para poder reproducirla más tarde
    global señal_generada
    señal_generada = señal

# Función para reproducir la señal
def reproducir_senal():
    if 'señal_generada' in globals():
        sd.play(señal_generada, 44100)
        sd.wait()

# Configuración de la interfaz gráfica
app = tk.Tk()
app.title("Generador y Reproductor de Señales")
app.geometry("300x200")

frecuencia_label = tk.Label(app, text="Frecuencia (Hz):")
frecuencia_label.pack()
frecuencia_entry = tk.Entry(app)
frecuencia_entry.pack()

duracion_label = tk.Label(app, text="Duración (s):")
duracion_label.pack()
duracion_entry = tk.Entry(app)
duracion_entry.pack()

generar_button = tk.Button(app, text="Generar Señal", command=generar_senal)
generar_button.pack()

reproducir_button = tk.Button(app, text="Reproducir Señal", command=reproducir_senal)
reproducir_button.pack()

app.mainloop()
