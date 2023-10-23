import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
from pydub.playback import play

# Cargar el archivo de audio
audio = AudioSegment.from_file("latidos.wav")

# Extraer los datos de audio y convertirlos a una matriz NumPy
audio_data = np.array(audio.get_array_of_samples())

# Calcular la duración en segundos
duration = len(audio_data) / audio.frame_rate

# Crear un eje de tiempo
time = np.linspace(0, duration, num=len(audio_data))

# Graficar la forma de onda de audio
plt.figure(figsize=(10, 4))
plt.plot(time, audio_data, lw=0.5)
plt.title("Forma de Onda de Audio")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.show()

audio = AudioSegment.from_file("latidos.wav")
play(audio)
