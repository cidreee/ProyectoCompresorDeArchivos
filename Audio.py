"""
@author: Christopher Oswaldo Márquez Reyes
@author: Valeria Marian Andrade Monreal
"""

# Importación de las librerías necesarias para su funcionamiento
import os
import wave
import numpy as np


class AudioCompressor:
    def compress_file(self, input_file, output_folder):
        # Abrir el archivo WAV de entrada para lectura binaria
        with wave.open(input_file, 'rb') as wave_file:
            # Obtener la configuración del archivo WAV
            sample_width = wave_file.getsampwidth()
            channels = wave_file.getnchannels()
            framerate = wave_file.getframerate()
            frames = wave_file.readframes(wave_file.getnframes())

        # Convertir los frames del audio a un array de NumPy con tipo de dato int16
        audio_array = np.frombuffer(frames, dtype=np.int16)

        # Reducir el número de muestras (puedes ajustar este valor)
        factor = 2
        compressed_audio_array = audio_array[::factor]

        # Convertir el array comprimido de audio de nuevo a frames de bytes
        compressed_frames = compressed_audio_array.tobytes()

        # Construir la ruta de salida para el archivo comprimido
        output_file_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_file))[0]}_compressed.wav")

        # Crear un nuevo archivo WAV para escribir el audio comprimido
        with wave.open(output_file_path, 'wb') as compressed_wave_file:
            compressed_wave_file.setsampwidth(sample_width)
            compressed_wave_file.setnchannels(channels)
            compressed_wave_file.setframerate(int(framerate / factor))
            compressed_wave_file.writeframes(compressed_frames)

        return output_file_path

    def decompress_file(self, input_file, output_folder):
        # Abrir el archivo WAV comprimido para lectura binaria
        with wave.open(input_file, 'rb') as compressed_wave_file:
            # Obtener la configuración del archivo WAV comprimido
            sample_width = compressed_wave_file.getsampwidth()
            channels = compressed_wave_file.getnchannels()
            framerate = compressed_wave_file.getframerate()
            frames = compressed_wave_file.readframes(compressed_wave_file.getnframes())

        # Convertir los frames del audio comprimido a un array de NumPy con tipo de dato int16
        audio_array = np.frombuffer(frames, dtype=np.int16)

        # Ajustar el número de muestras para la descompresión (debería ser el mismo factor utilizado en la compresión)
        factor = 2
        decompressed_audio_array = np.zeros(len(audio_array) * factor, dtype=np.int16)
        decompressed_audio_array[::factor] = audio_array

        # Convertir el array descomprimido de audio de nuevo a frames de bytes
        decompressed_frames = decompressed_audio_array.tobytes()

        # Construir la ruta de salida para el archivo descomprimido
        output_file_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_file))[0]}_decompressed.wav")

        # Crear un nuevo archivo WAV para escribir el audio descomprimido
        with wave.open(output_file_path, 'wb') as decompressed_wave_file:
            decompressed_wave_file.setsampwidth(sample_width)
            decompressed_wave_file.setnchannels(channels)
            decompressed_wave_file.setframerate(int(framerate * factor))
            decompressed_wave_file.writeframes(decompressed_frames)

        return output_file_path
