def generar_audio(frec):
    import numpy as np
    from scipy.io import wavfile

    # Configuración del tono
    frecuencia = frec  # Frecuencia en Hz
    duracion = 1  # Duración en segundos
    amplitud = 0.5  # Amplitud del tono

    # Crear un vector de tiempo
    tiempo = np.linspace(
        0, duracion, int(44100 * duracion), endpoint=False
    )  # 44.1 kHz de muestreo

    # Generar el tono
    tono = amplitud * np.sin(2 * np.pi * frecuencia * tiempo)

    # Guardar el tono como un archivo WAV
    nombre_archivo = "1.wav"
    wavfile.write(nombre_archivo, 44100, tono.astype(np.float32))

    print(f"Tono de {frecuencia} Hz guardado como {nombre_archivo}")


def obtener_frecuencias():
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.io import wavfile
    from scipy.signal import butter, lfilter

    # Función para crear un filtro pasabajas
    def butter_lowpass(cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype="low", analog=False)
        return b, a

    # Función para aplicar el filtro pasabajas a los datos
    def butter_lowpass_filter(data, cutoff, fs, order=5):
        b, a = butter_lowpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    # Cargar archivo de audio
    samplerate, data = wavfile.read("audio.wav")

    # Convertir a mono si es estéreo
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)

    # Aplicar filtro pasabajas
    cutoff = 1000  # Frecuencia de corte en Hz
    filtered_data = butter_lowpass_filter(data, cutoff, samplerate)

    # Obtener la transformada de Fourier
    fft_out = np.fft.rfft(filtered_data)

    # Obtener las frecuencias absolutas
    abs_fft = np.abs(fft_out)

    # Encontrar las 3 frecuencias más altas
    frequencies = np.argsort(abs_fft)[-3:]

    # Escalar las frecuencias para obtenerlas en Hz
    frequencies_hz = frequencies * samplerate / len(filtered_data)

    print("Las tres frecuencias principales son:", frequencies_hz)

    # Graficar el espectro
    freqs = np.fft.rfftfreq(len(filtered_data), 1 / samplerate)
    plt.plot(freqs, abs_fft)
    plt.title("Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.show()


# obtener_frecuencias()
generar_audio(frec=696.70834749)
