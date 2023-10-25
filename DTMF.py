import numpy as np
from scipy.io import wavfile

# Cargar el archivo de audio
audio_file = 'tu_archivo_de_audio.wav'
fs, x = wavfile.read(audio_file)

# Diseñar los filtros para las frecuencias DTMF
f1 = [697, 770, 852, 941]
f2 = [1209, 1336, 1477]
dtmf = f1 + f2

# Inicializar matrices para almacenar las amplitudes de las frecuencias DTMF
amplitudes_f1 = np.zeros(len(dtmf))
amplitudes_f2 = np.zeros(len(dtmf))

# Calcular la DFT de la señal de audio
X = np.fft.fft(x)
N = len(x)
frequencies = np.arange(N) * (fs / N)

# Calcular las amplitudes de las frecuencias DTMF
for i in range(len(dtmf)):
    f1_freq = dtmf[i]
    f2_freq = dtmf[i + len(f1)]

    index_f1 = np.argmin(np.abs(frequencies - f1_freq))
    index_f2 = np.argmin(np.abs(frequencies - f2_freq))

    amplitudes_f1[i] = np.abs(X[index_f1])
    amplitudes_f2[i] = np.abs(X[index_f2])

# Encontrar las frecuencias DTMF dominantes
threshold = 0.2  # Ajusta este valor según tus necesidades
max_amplitude_f1 = max(amplitudes_f1)
max_amplitude_f2 = max(amplitudes_f2)
dominant_f1 = [i for i, amplitude in enumerate(amplitudes_f1) if amplitude > threshold * max_amplitude_f1]
dominant_f2 = [i for i, amplitude in enumerate(amplitudes_f2) if amplitude > threshold * max_amplitude_f2]

# Mapear las frecuencias dominantes a dígitos
dtmf_symbols = [['1', '2', '3', 'A'], ['4', '5', '6', 'B'], ['7', '8', '9', 'C'], ['*', '0', '#', 'D']]

if dominant_f1 and dominant_f2:
    detected_digit = dtmf_symbols[dominant_f2[0]][dominant_f1[0]]
    print(f'El dígito detectado es: {detected_digit}')
else:
    print('No se detectó ninguna señal DTMF.')
