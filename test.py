# def grabar_audio_en_tiempo_real(nombre_archivo):
#     import pyaudio
#     import wave
#     """
#     Graba audio en tiempo real y lo guarda en un archivo WAV.

#     Args:
#         nombre_archivo (str): El nombre del archivo WAV en el que se guardará la grabación.

#     Returns:
#         None
#     """
#     # Configuración de la grabación
#     FORMAT = pyaudio.paInt16
#     CHANNELS = 1  # Para audio mono, 2 para estéreo
#     RATE = 4000  # Tasa de muestreo en Hz (puedes ajustarla según tus necesidades)
#     CHUNK = 1024  # Tamaño del búfer para la grabación (puedes ajustarlo según tus necesidades)

#     # Inicializar PyAudio
#     p = pyaudio.PyAudio()

#     # Abrir un flujo de audio para la captura
#     stream = p.open(format=FORMAT,
#                     channels=CHANNELS,
#                     rate=RATE,
#                     input=True,
#                     frames_per_buffer=CHUNK)

#     print("Grabando...")

#     frames = []  # Aquí se almacenarán los datos de audio

#     try:
#         while True:
#             data = stream.read(CHUNK)
#             frames.append(data)
#     except KeyboardInterrupt:
#         print("Grabación detenida.")

#     # Detener el flujo de audio
#     stream.stop_stream()
#     stream.close()

#     # Terminar PyAudio
#     p.terminate()

#     # Guardar los datos de audio en un archivo WAV
#     wf = wave.open(nombre_archivo, "wb")
#     wf.setnchannels(CHANNELS)
#     wf.setsampwidth(p.get_sample_size(FORMAT))
#     wf.setframerate(RATE)
#     wf.writeframes(b"".join(frames))
#     wf.close()

#     print(f"La grabación se ha guardado en {nombre_archivo}")





# def procesar_audio(nombre_archivo):
#     import numpy as np
#     import matplotlib.pyplot as plt
#     from scipy.io import wavfile
#     # Paso 1: Leer el audio
#     samplerate, data = wavfile.read(nombre_archivo)

#     # Paso 2: Reemplazar valores de amplitud menores a 12,000 por 0
#     data[data < 12000] = 0

#     # Paso 3: Inicializar nuevos arrays para la señal procesada
#     new_array_signal = []

#     # Paso 4: Procesar la señal
#     in_interval = False
#     interval_start = 0
#     for i in range(len(data)):
#         if data[i] > 0 and not in_interval:
#             interval_start = i
#             in_interval = True
#         elif in_interval and data[i] == 0:
#             # Agregar el intervalo al nuevo array
#             new_array_signal.extend(data[interval_start:i])
#             # Rellenar con ceros durante 2 segundos
#             sample_interval = int(samplerate * 2)
#             new_array_signal.extend([0] * sample_interval)
#             in_interval = False

#     # Paso 5: Graficar la nueva señal
#     plt.plot(new_array_signal)
#     plt.title("Nueva Señal Procesada")
#     plt.xlabel("Muestras")
#     plt.ylabel("Amplitud")
#     plt.show()

#     return new_array_signal


import numpy as np
from scipy.io import wavfile

# Cargar el archivo de audio
audioFile = 'harold.wav'
fs, x = wavfile.read(audioFile)

# Diseñar los filtros para las frecuencias DTMF
f1 = [697, 770, 852, 941]
f2 = [1209, 1336, 1477]
dtmf = np.concatenate((f1, f2))

# Inicializar matrices para almacenar las amplitudes de las frecuencias DTMF
amplitudes_f1 = np.zeros(len(dtmf))
amplitudes_f2 = np.zeros(len(dtmf))

# Calcular la DFT de la señal de audio
X = np.fft.fft(x)
N = len(x)
frequencies = np.arange(N) * (fs/N)

# Calcular las amplitudes de las frecuencias DTMF
for i in range(len(dtmf)):
    f1_freq = dtmf[i]
    f2_freq = dtmf[i + len(f1)]
    
    index_f1 = np.argmin(np.abs(frequencies - f1_freq))
    index_f2 = np.argmin(np.abs(frequencies - f2_freq))
    
    if index_f1 < len(X):
        amplitudes_f1[i] = np.abs(X[index_f1])
    else:
        amplitudes_f1[i] = 0
        
    if index_f2 < len(X):
        amplitudes_f2[i] = np.abs(X[index_f2])
    else:
        amplitudes_f2[i] = 0

# Encontrar las frecuencias DTMF dominantes
threshold = 0.2 # Ajusta este valor según tus necesidades
dominant_f1 = np.where(amplitudes_f1 > threshold * np.max(amplitudes_f1))[0]
dominant_f2 = np.where(amplitudes_f2 > threshold * np.max(amplitudes_f2))[0]

# Mapear las frecuencias dominantes a dígitos
dtmf_symbols = np.array([['1', '2', '3', 'A'], ['4', '5', '6', 'B'], ['7', '8', '9', 'C'], ['*', '0', '#', 'D']])

if dominant_f1.size > 0 and dominant_f2.size > 0:
    detected_digit = dtmf_symbols[dominant_f2[0], dominant_f1[0]]
    print(f'El dígito detectado es: {detected_digit}')
else:
    print('No se detectó ninguna señal DTMF.')