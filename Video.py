"""
@author: Christopher Oswaldo Márquez Reyes
@author: Valeria Marian Andrade Monreal
"""

# Importación de las librerías necesarias para su correcto funcionamiento
from moviepy.editor import VideoFileClip
import os


class VideoCompressor:
    def compress_file(self, input_file, output_folder):
        # Cargar el video usando moviepy
        clip = VideoFileClip(input_file)

        # Extraer el nombre y la extensión del archivo de entrada
        file_name, file_extension = os.path.splitext(os.path.basename(clip.filename))

        # Construir la ruta de salida para el archivo comprimido
        output_file = os.path.join(output_folder, f"compressed_{file_name}.mp4")

        # Escribir el video comprimido usando codec libx264, audio_codec aac y bitrate de 1000k (ajustable)
        clip.write_videofile(output_file, codec="libx264", audio_codec="aac", bitrate="1000k")  # Ajusta el bitrate según tus necesidades

        return output_file

    def decompress_file(self, input_file, output_folder):
        # Cargar el video usando moviepy
        clip = VideoFileClip(input_file)

        # Extraer el nombre y la extensión del archivo de entrada
        file_name, file_extension = os.path.splitext(os.path.basename(clip.filename))

        # Construir la ruta de salida para el archivo descomprimido
        output_file = os.path.join(output_folder, f"decompressed_{file_name}.mp4")

        # Escribir el video descomprimido usando codec libx264, audio_codec aac y bitrate de 5000k (ajustable)
        clip.write_videofile(output_file, codec="libx264", audio_codec="aac", bitrate="5000k")  # Ajusta el bitrate según tus necesidades

        return output_file
