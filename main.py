import os
import gui
import librosa
import numpy as np
import soundfile as sf
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy.signal import butter, lfilter


def generar_audio(frec: float, file_name: str) -> None:
    """
    Genera un tono de frecuencia dada y lo guarda como un archivo WAV.

    Args:
        frec (float): Frecuencia del tono en Hz.
        file_name (str): Nombre del archivo WAV a guardar.

    Returns:
        None
    """
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
    nombre_archivo = file_name
    wavfile.write(nombre_archivo, 44100, tono.astype(np.float32))

    print(f"Tono de {frecuencia} Hz guardado como {nombre_archivo}")


def obtener_frecuencias(file_name: str) -> np.ndarray:
    """
    Obtiene las dos frecuencias más altas de un archivo de audio.

    Args:
        file_name (str): Nombre del archivo de audio.

    Returns:
        np.ndarray: Un arreglo de NumPy con las dos frecuencias más altas en Hz.
    """
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
    samplerate, data = wavfile.read(file_name)

    # Convertir a mono si es estéreo
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)

    # Aplicar filtro pasabajas
    cutoff = 1800  # Frecuencia de corte en Hz
    filtered_data = butter_lowpass_filter(data, cutoff, samplerate)

    # Obtener la transformada de Fourier
    fft_out = np.fft.rfft(filtered_data)

    # Obtener las frecuencias absolutas
    abs_fft = np.abs(fft_out)

    # Encontrar las 2 frecuencias más altas
    frequencies = np.argsort(abs_fft)[-2:]

    # Escalar las frecuencias para obtenerlas en Hz
    frequencies_hz = frequencies * samplerate / len(filtered_data)

    return frequencies_hz


def generar_tono_dtmf(archivo_wav: str, output_file_name: str) -> None:
    """
    Genera un tono DTMF a partir de un archivo de audio y lo guarda como un archivo WAV.

    Args:
        archivo_wav (str): Nombre del archivo de audio a partir del cual se generará el tono DTMF.
        output_file_name (str): Nombre del archivo WAV a guardar.

    Returns:
        None
    """
    # Obtener las dos frecuencias de la DTMF
    frecuencias = obtener_frecuencias(archivo_wav)
    frecuencia1 = frecuencias[0]
    frecuencia2 = frecuencias[1]

    # Generar los tonos de cada frecuencia y guardarlos como archivos WAV
    generar_audio(frecuencia1, "tono1.wav")
    generar_audio(frecuencia2, "tono2.wav")

    # Combinar los dos archivos WAV para crear el tono de la DTMF completo

    # Cargar los archivos WAV
    tono1, samplerate = sf.read("tono1.wav")
    tono2, samplerate = sf.read("tono2.wav")

    # Alinear los dos tonos
    diferencia = len(tono2) - len(tono1)
    if diferencia > 0:
        tono1 = np.pad(tono1, (0, diferencia), "constant")
    else:
        tono2 = np.pad(tono2, (0, -diferencia), "constant")

    # Combinar los dos tonos
    tono_completo = tono1 + tono2

    # Guardar el tono completo como un archivo WAV
    sf.write(output_file_name, tono_completo, samplerate)

    print(f"Tono DTMF generado a partir de {archivo_wav} y guardado como {output_file_name}")


def obtener_numero_presionado(archivo_wav: str):
    """
    Obtiene el número presionado en un teclado DTMF a partir de un archivo de audio.

    Args:
        archivo_wav (str): Nombre del archivo de audio.

    Returns:
        Union[str, None]: El número presionado en el teclado DTMF, o None si no se encontró un número.
    """
    # Obtener las dos frecuencias del tono DTMF
    samplerate, data = wavfile.read(archivo_wav)
    frecuencias = np.array(obtener_frecuencias(archivo_wav))

    # Definir la tabla de frecuencias DTMF
    tabla_frecuencias = {
        (697, 1209): "1",
        (697, 1336): "2",
        (697, 1477): "3",
        (697, 1633): "A",
        (770, 1209): "4",
        (770, 1336): "5",
        (770, 1477): "6",
        (770, 1633): "B",
        (852, 1209): "7",
        (852, 1336): "8",
        (852, 1477): "9",
        (852, 1633): "C",
        (941, 1209): "*",
        (941, 1336): "0",
        (941, 1477): "#",
        (941, 1633): "D",
    }

    # Buscar las dos frecuencias en la tabla de frecuencias
    for frecuencia1, frecuencia2 in tabla_frecuencias.keys():
        if (
            abs(frecuencias[0] - frecuencia1) <= 10
            and abs(frecuencias[1] - frecuencia2) <= 10
        ) or (
            abs(frecuencias[0] - frecuencia2) <= 10
            and abs(frecuencias[1] - frecuencia1) <= 10
        ):
            return tabla_frecuencias[(frecuencia1, frecuencia2)]

    # Si no se encontraron dos frecuencias, devolver None
    return None


def analizar_audio_dtmf(archivo_audio: str, duracion_segmento: float) -> None:
    """
    Analiza un archivo de audio en busca de tonos DTMF y muestra los números presionados en la consola.

    Args:
        archivo_audio (str): Nombre del archivo de audio a analizar.
        duracion_segmento (float): Duración de cada segmento de tiempo en segundos.

    Returns:
        None
    """
    # Crear la carpeta "temp" si no existe
    temp_folder = "temp"
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)

    # Cargar el archivo de audio completo
    with open(archivo_audio, "rb") as file:
        samplerate, data = wavfile.read(file)

    # Dividir el archivo de audio en segmentos de tiempo y analizar cada uno
    numeros_presionados = []
    for i in range(0, len(data), int(samplerate * duracion_segmento)):
        segmento = data[i : i + int(samplerate * duracion_segmento)]

        # Crear un archivo temporal para el segmento en la carpeta "temp"
        temp_filename = os.path.join(
            temp_folder, f"segmento_{i // int(samplerate * duracion_segmento)}.wav"
        )
        wavfile.write(temp_filename, samplerate, segmento)

        # Analizar el archivo temporal
        numero_presionado = obtener_numero_presionado(temp_filename)

        if numero_presionado is not None:
            numeros_presionados.append(numero_presionado)

    # Imprimir los números que se presionaron en la consola
    if len(numeros_presionados) > 0:
        print("Se presionaron los números:", " - ".join(numeros_presionados))
    else:
        print("No se detectó ningún número DTMF en el archivo de audio.")

    # Eliminar los archivos temporales
    for file in os.listdir(temp_folder):
        file_path = os.path.join(temp_folder, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error al eliminar el archivo {file_path}: {e}")

    # Eliminar la carpeta "temp" si está vacía
    if not os.listdir(temp_folder):
        os.rmdir(temp_folder)


def visualizar_espectro(archivo_audio: str) -> None:
    """
    Carga un archivo de audio y muestra su espectro en frecuencia.

    Args:
        archivo_audio (str): Nombre del archivo de audio a cargar.

    Returns:
        None
    """
    # Cargar el archivo de audio
    y, sr = librosa.load(archivo_audio)

    # Calcular la transformada de Fourier del audio
    Y = np.fft.fft(y)

    # Obtener el valor absoluto de la transformada
    Y_abs = np.abs(Y)

    # Crear el gráfico del espectro en frecuencia
    plt.figure(figsize=(14, 5))
    plt.plot(
        np.linspace(0, sr / 2, len(Y_abs) // 2),
        Y_abs[: len(Y_abs) // 2],
        label="Espectro en frecuencia",
    )
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Amplitud")
    plt.title("Espectro en frecuencia de la señal de audio")
    plt.grid()
    plt.legend()
    plt.show()


def visualizar_audio(archivo_audio: str) -> None:
    """
    Carga un archivo de audio y muestra su forma de onda en el tiempo.

    Args:
        archivo_audio (str): Nombre del archivo de audio a cargar.

    Returns:
        None
    """
    # Cargar el archivo de audio
    fs, x = read(archivo_audio)

    # Crear el vector de tiempo
    time = np.arange(0, len(x) / fs, 1.0 / fs)

    # Graficar la forma de onda de audio
    plt.figure(figsize=(15, 5))
    plt.plot(time, x)
    plt.title("Forma de Onda de Audio")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    gui.GUI()
