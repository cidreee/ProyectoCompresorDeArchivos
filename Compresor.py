"""
@author: Christopher Oswaldo Márquez Reyes
@author: Valeria Marian Andrade Monreal
"""

# Importación de las librerías necesarias para el diseño y funcionamiento de la interfaz
# Así como la importación de los distintos métodos de compresión y descompresión
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from Texto import TextHuffmanEncoder
from Imagenes import ImageHuffmanEncoder
from Audio import AudioCompressor
from Video import VideoCompressor


# Clase de la interfaz gráfica, donde el usuario interactuara para comprimir y descomprimir los archivos
class HuffmanGUI:
    def __init__(self, master):
        # Inicialización de la interfaz gráfica
        self.master = master
        self.master.title("COMPRESSOR")
        self.selected_folder = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # Configuración de la ventana principal
        app_width = 450
        app_height = 250
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_position = (screen_width - app_width) // 2
        y_position = (screen_height - app_height) // 2
        self.master.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")

        # Creación y empaquetado de widgets en la ventana principal
        output_folder_label = tk.Label(self.master, text="Output Folder:")
        output_folder_entry = tk.Entry(self.master, width=60, textvariable=self.selected_folder)
        select_folder_button = tk.Button(self.master, text="Select Folder", command=self.select_folder)
        compress_button = tk.Button(self.master, text="Compress", command=self.compress)
        decompress_button = tk.Button(self.master, text="Decompress", command=self.decompress)

        output_folder_label.pack(pady=10)
        output_folder_entry.pack(pady=10)
        select_folder_button.pack(pady=10)
        compress_button.pack(pady=10)
        decompress_button.pack(pady=10)

    def select_folder(self):
        # Método para seleccionar una carpeta y actualizar la variable asociada
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder.set(folder)

    def compress(self):
        # Método para la compresión de archivos
        file_types = [("Text and Image Files", "*.txt;*.bmp;*.wav;*.mp4")]
        input_file_path = filedialog.asksaveasfilename(title="Select a file to compress", filetypes=file_types, defaultextension=".txt")
        output_folder = self.selected_folder.get()

        if input_file_path and output_folder:
            # Selecciona el codificador adecuado según la extensión del archivo de entrada
            if input_file_path.lower().endswith('.txt'):
                encoder = TextHuffmanEncoder()
                compressed_file_extension = '.txt.bin'
            elif input_file_path.lower().endswith('.bmp'):
                encoder = ImageHuffmanEncoder()
                compressed_file_extension = '.bmp.bin'
            elif input_file_path.lower().endswith('.wav'):
                encoder = AudioCompressor()
                compressed_file_extension = '.wav'
            elif input_file_path.lower().endswith('.mp4'):
                encoder = VideoCompressor()
                compressed_file_extension = '.mp4'
            else:
                # Muestra un mensaje de advertencia si el tipo de archivo no es compatible
                messagebox.showwarning("Unsupported File Type", "Unsupported file type. Please select a .txt, .bmp, .wav, or .mp4 file.")
                return

            # Realiza la compresión y muestra un mensaje informativo
            output_file = encoder.compress_file(input_file_path, output_folder)
            compressed_file_path = os.path.splitext(output_file)[0] + compressed_file_extension
            os.rename(output_file, compressed_file_path)
            messagebox.showinfo("Compression Complete", f"File compressed and saved at:\n{compressed_file_path}")

    def decompress(self):
        # Método para la descompresión de archivos
        file_types = [("MP4, Wave and Binary Files", "*.wav;*.bin;*.mp4")]
        input_file = filedialog.askopenfilename(title="Select a file to decompress", filetypes=file_types)
        output_folder = self.selected_folder.get()

        if input_file and output_folder:
            # Selecciona el decodificador adecuado según la extensión del archivo de entrada
            if input_file.lower().endswith('.txt.bin'):
                encoder = TextHuffmanEncoder()
                original_file_extension = '.txt'
            elif input_file.lower().endswith('.bmp.bin'):
                encoder = ImageHuffmanEncoder()
                original_file_extension = '.bmp'
            elif input_file.lower().endswith('.wav'):
                encoder = AudioCompressor()
                original_file_extension = '.wav'
            elif input_file.lower().endswith('.mp4'):
                encoder = VideoCompressor()
                original_file_extension = '.mp4'
            else:
                # Muestra un mensaje de advertencia si el tipo de archivo no es compatible
                messagebox.showwarning("Unsupported File Type", "Unsupported file type. Please select a .bin or .wav file.")
                return

            # Realiza la descompresión y muestra un mensaje informativo
            output_file = encoder.decompress_file(input_file, output_folder)
            decompressed_file_path = output_file + original_file_extension
            os.rename(output_file, decompressed_file_path)
            messagebox.showinfo("Decompression Complete", f"File decompressed and saved at:\n{decompressed_file_path}")


if __name__ == "__main__":
    # Inicia la aplicación
    root = tk.Tk()
    app = HuffmanGUI(root)
    # Inicia el bucle principal de la interfaz gráfica
    root.mainloop()
