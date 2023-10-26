import os
import sys
import main
import wave
import pyaudio
import tkinter as tk
from tkinter import ttk, filedialog


class GUI:
    def __init__(self) -> None:
        """
        Inicializa la ventana principal de la aplicación y agrega los widgets necesarios.

        Args:
            None

        Returns:
            None
        """
        # Crear la ventana principal de la aplicación
        self.window = tk.Tk()
        self.window.title("Detector de tonos DTMF mediante Fourier")
        self.window.geometry("700x700")
        
        # Agregar estilo personalizado para los botones
        style = ttk.Style()
        style.configure("Custom.TButton", font=("Helvetica", 12), padding=10)
        
        # Agregar widgets a la ventana
        self.label = ttk.Label(self.window, text="Cargar archivo de audio", font=("Helvetica", 10))
        self.label.pack(pady=20)
        
        self.button = ttk.Button(self.window, text="Cargar", command=self.load_audio_file, style="Custom.TButton")
        self.button.pack(pady=10)
        
        self.play_button = ttk.Button(self.window, text="Reproducir", command=self.play_audio_file, state=tk.DISABLED, style="Custom.TButton")
        self.play_button.pack(pady=10)      
        
        self.analyze_button = ttk.Button(self.window, text="Analizar", command=self.analyze_audio_file, state=tk.DISABLED, style="Custom.TButton")
        self.analyze_button.pack(pady=10)
        
        self.param_label = ttk.Label(self.window, text="Segundo parámetro:", font=("Helvetica", 12))
        self.param_label.pack(pady=10)
        
        self.param_entry = ttk.Entry(self.window, font=("Helvetica", 12))
        self.param_entry.pack(pady=10)
        self.param_entry.insert(0, "1.3")
        
        self.visualize_button = ttk.Button(self.window, text="Ver señal en el tiempo", command=self.visualize_audio_file, state=tk.DISABLED, style="Custom.TButton")
        self.visualize_button.pack(pady=10)
        
        self.visualize_espectro_button = ttk.Button(self.window, text="Visualizar espectro", command=self.visualize_espectro, state=tk.DISABLED, style="Custom.TButton")
        self.visualize_espectro_button.pack(pady=10)
        
        self.result_label = ttk.Label(self.window, text="Resultado:", font=("Helvetica", 14))
        self.result_label.pack(pady=20)
        
        # Agregar estilo personalizado para la etiqueta de resultado
        style.configure("Result.TLabel", font=("Helvetica", 12), foreground="green")
        
        self.result_text = tk.Text(self.window, height=10, state=tk.DISABLED)
        self.result_text.pack(pady=10)
        
        # Redirigir la salida estándar a la ventana de resultados
        sys.stdout = TextRedirector(self.result_text, "stdout")
        
        # Inicializar las variables para almacenar la información del archivo de audio
        self.audio_file_path = None
        self.audio_data = None
        self.audio_rate = None           
        
        # Iniciar el bucle principal de la ventana
        self.window.mainloop()
        
    def load_audio_file(self) -> None:
        """
        Abre un cuadro de diálogo para seleccionar un archivo de audio, carga los datos del archivo y habilita los botones de
        reproducir, analizar y visualizar.

        Args:
            None

        Returns:
            None
        """
        # Abrir el cuadro de diálogo para seleccionar un archivo de audio
        file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Seleccionar archivo de audio", filetypes=[("Archivos WAV", "*.wav")])
        
        # Actualizar la etiqueta con la ruta del archivo seleccionado
        self.label.config(text=f"Archivo de audio seleccionado: {file_path}")
        
        # Almacenar la ruta del archivo de audio en la variable de instancia
        self.audio_file_path = file_path
        
        # Cargar los datos del archivo de audio
        with wave.open(self.audio_file_path, "rb") as audio_file:
            self.audio_data = audio_file.readframes(audio_file.getnframes())
            self.audio_rate = audio_file.getframerate()
        
        # Habilitar los botones de reproducir, analizar y visualizar
        self.play_button.config(state=tk.NORMAL)
        self.analyze_button.config(state=tk.NORMAL)
        self.visualize_button.config(state=tk.NORMAL)
        self.visualize_espectro_button.config(state=tk.NORMAL)     
        
    def play_audio_file(self) -> None:
        """
        Reproduce el archivo de audio cargado en la aplicación.

        Args:
            None

        Returns:
            None
        """
        # Verificar si se ha cargado un archivo de audio
        if self.audio_file_path is None:
            tk.messagebox.showerror("Error", "Debes cargar un archivo de audio antes de reproducirlo.")
            return
        
        # Crear un objeto PyAudio para reproducir el archivo de audio
        p = pyaudio.PyAudio()
        
        # Abrir un stream de audio para reproducir el archivo
        stream = p.open(format=p.get_format_from_width(2), channels=1, rate=self.audio_rate, output=True)        
        stream.write(self.audio_data)        
        
        self.play_button.config(state=tk.DISABLED)               
        
        # Detener el stream y cerrar el objeto PyAudio
        stream.stop_stream()
        stream.close()
        p.terminate()    
        
    def analyze_audio_file(self) -> None:
        """
        Analiza el archivo de audio cargado en la aplicación utilizando la función analizar_audio_dtmf del archivo main.py.

        Args:
            None

        Returns:
            None
        """
        # Verificar si se ha cargado un archivo de audio
        if self.audio_file_path is None:
            tk.messagebox.showerror("Error", "Debes cargar un archivo de audio antes de analizarlo.")
            return
        
        # Obtener el valor del campo de entrada de texto
        segundo_parametro = float(self.param_entry.get())
        
        # Redirigir la salida estándar a la ventana de resultados
        sys.stdout = TextRedirector(self.result_text, "stdout")
        
        # Llamar a la función analizar_audio_dtmf en el archivo main.py con el archivo de audio seleccionado y el segundo parámetro como argumentos
        main.analizar_audio_dtmf(self.audio_file_path, segundo_parametro)
        
        # Restaurar la salida estándar
        sys.stdout = sys.__stdout__

    def visualize_audio_file(self) -> None:
        """
        Visualiza el archivo de audio cargado en la aplicación utilizando la función visualizar_audio del archivo main.py.

        Args:
            None

        Returns:
            None
        """
        # Verificar si se ha cargado un archivo de audio
        if self.audio_file_path is None:
            tk.messagebox.showerror("Error", "Debes cargar un archivo de audio antes de visualizarlo.")
            return
        
        # Llamar a la función visualizar_audio en el archivo main.py con el archivo de audio seleccionado como argumento
        main.visualizar_audio(self.audio_file_path)  
        
    def visualize_espectro(self) -> None:
        """
        Visualiza el espectro del archivo de audio cargado en la aplicación utilizando la función visualizar_espectro del archivo main.py.

        Args:
            None

        Returns:
            None
        """
        # Verificar si se ha cargado un archivo de audio
        if self.audio_file_path is None:
            tk.messagebox.showerror("Error", "Debes cargar un archivo de audio antes de visualizar el espectro.")
            return
        
        # Llamar a la función visualizar_espectro en el archivo main.py con el archivo de audio seleccionado como argumento
        main.visualizar_espectro(self.audio_file_path)     
        
class TextRedirector:
    """
    Clase que redirige la salida estándar a un widget de texto en una aplicación de tkinter.

    Args:
        widget (tkinter.Text): El widget de texto al que se redirigirá la salida estándar.
        tag (str): La etiqueta que se utilizará para dar formato al texto redirigido.

    Returns:
        None
    """
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag
        
    def write(self, str):
        """
        Escribe el texto redirigido en el widget de texto.

        Args:
            str (str): El texto que se redirigirá al widget de texto.

        Returns:
            None
        """
        self.widget.configure(state=tk.NORMAL)
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state=tk.DISABLED)
        
if __name__ == "__main__":
    gui = GUI()