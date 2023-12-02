"""
@author: Christopher Oswaldo Márquez Reyes
@author: Valeria Marian Andrade Monreal
"""

# Importación de las librerías necesarias para su funcionamiento
from tkinter import messagebox
import bitarray
import os
from PIL import Image
import numpy as np


class HuffmanNode:
    def __init__(self, char=None, freq=0):
        # Inicializa un nodo del árbol de Huffman
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        # Define la comparación de nodos basada en la frecuencia
        return self.freq < other.freq


class ImageHuffmanEncoder:
    # Variable de clase para almacenar datos de imagen original
    original_img_data = None

    def __init__(self):
        # Inicializa el codificador Huffman para imágenes
        self.nodes = []

    def build_frequency_map(self, data):
        """
        Construye y devuelve un diccionario con la frecuencia de cada caracter en los datos.
        """
        frequency_map = {}
        for char in data:
            frequency_map[char] = frequency_map.get(char, 0) + 1
        return frequency_map

    def build_tree(self, frequency_map):
        """
        Construye y devuelve un árbol de Huffman basado en el mapa de frecuencias dado.
        """
        self.nodes = [HuffmanNode(char, freq) for char, freq in frequency_map.items()]

        while len(self.nodes) > 1:
            # Combina nodos de menor frecuencia para construir el árbol
            self.nodes.sort(key=lambda x: x.freq)
            left = self.nodes.pop(0)
            right = self.nodes.pop(0)

            merged_node = HuffmanNode(freq=left.freq + right.freq)
            merged_node.left = left
            merged_node.right = right

            self.nodes.append(merged_node)

        return self.nodes[0]

    def build_codebook(self, root, current_code="", codebook=None):
        """
        Construye y devuelve un diccionario con los códigos binarios para cada caracter en el árbol.
        """
        if codebook is None:
            codebook = {}

        if root is not None:
            if root.char is not None:
                codebook[root.char] = current_code
            self.build_codebook(root.left, current_code + "0", codebook)
            self.build_codebook(root.right, current_code + "1", codebook)

        return codebook

    def compress(self, data):
        """
        Comprime los datos utilizando el algoritmo de Huffman y devuelve los datos comprimidos y el árbol de Huffman.
        """
        frequency_map = self.build_frequency_map(data)
        root = self.build_tree(frequency_map)
        codebook = self.build_codebook(root)

        encoded_data = "".join(codebook[char] for char in data)
        return encoded_data, root

    def decompress(self, encoded_data, root):
        """
        Descomprime los datos comprimidos utilizando el árbol de Huffman.
        """
        decoded_data = []
        current_node = root

        for bit in encoded_data:
            if current_node is not None:
                if bit == "0" and current_node.left:
                    current_node = current_node.left
                elif bit == "1" and current_node.right:
                    current_node = current_node.right

                if current_node.char is not None:
                    decoded_data.append(current_node.char)
                    current_node = root
            else:
                break

        return decoded_data

    def compress_file(self, input_image, output_folder, progress_callback=None):
        """
        Comprime un archivo de imagen y guarda el archivo comprimido en la carpeta de salida.
        """
        with Image.open(input_image) as img:
            img_data = np.array(img)
            ImageHuffmanEncoder.original_img_data = img_data  # Almacenamos la información de la imagen original como variable de clase

        print("Original Image Shape:", img_data.shape)

        encoded_data, root = self.compress(img_data.tobytes())
        bit_array = bitarray.bitarray(encoded_data)

        file_name, _ = os.path.splitext(os.path.basename(input_image))
        output_file_path = os.path.join(output_folder, f"{file_name}_compressed.bin")

        with open(output_file_path, 'wb') as file:
            tree_bytes = self.encode_tree(root)
            file.write(len(tree_bytes).to_bytes(4, byteorder='big'))
            file.write(tree_bytes)
            bit_array.tofile(file)

        if progress_callback:
            progress_callback(100)

        return output_file_path

    def show_image(self, original_img, decompressed_img):
        # Aquí abrimos la imagen en la misma aplicación para verificar que la imagen original y la descomprimida sean la misma
        import matplotlib.pyplot as plt

        plt.subplot(1, 2, 1)
        plt.title('Original Image')
        plt.imshow(original_img)

        plt.subplot(1, 2, 2)
        plt.title('Decompressed Image')
        plt.imshow(decompressed_img)

        plt.show()

    def decompress_file(self, input_file, output_folder, progress_callback=None):
        """
        Descomprime un archivo binario y guarda el archivo descomprimido en la carpeta de salida.
        """
        if ImageHuffmanEncoder.original_img_data is None:
            messagebox.showerror("Error", "Please compress an image first.")
            return  # Evitamos que continúe si no hay información de la imagen original

        with open(input_file, 'rb') as file:
            tree_size = int.from_bytes(file.read(4), byteorder='big')
            tree_bytes = file.read(tree_size)
            encoded_data = bitarray.bitarray()
            encoded_data.fromfile(file)

        root = self.decode_tree(tree_bytes)
        decoded_data = self.decompress(encoded_data.to01(), root)

        # Convertir los datos decodificados a bytes
        decoded_data_bytes = bytes(decoded_data)

        # Reconstruir la imagen descomprimida
        decompressed_img_data = np.frombuffer(decoded_data_bytes, dtype=np.uint8).reshape(ImageHuffmanEncoder.original_img_data.shape)

        # Mostrar las imágenes
        self.show_image(ImageHuffmanEncoder.original_img_data, decompressed_img_data)

        file_name, _ = os.path.splitext(os.path.basename(input_file))
        output_file_path = os.path.join(output_folder, f"{file_name}_decompressed.bmp")

        with open(output_file_path, 'wb') as file:
            file.write(decoded_data_bytes)

        if progress_callback:
            progress_callback(100)

        return output_file_path

    def encode_tree(self, root):
        """
        Codifica el árbol de Huffman en bytes.
        """
        if root is None:
            return b''

        if isinstance(root.char, int):
            return b'\x01' + root.char.to_bytes(4, byteorder='big')
        elif root.char is not None:
            return b'\x02' + root.char.encode('utf-8')
        else:
            left_bytes = self.encode_tree(root.left)
            right_bytes = self.encode_tree(root.right)
            return b'\x00' + len(left_bytes).to_bytes(4, byteorder='big') + left_bytes + right_bytes

    def decode_tree(self, tree_bytes):
        """
        Decodifica los bytes y reconstruye el árbol de Huffman.
        """
        if not tree_bytes:
            return None

        if tree_bytes[0] == 1:
            char = int.from_bytes(tree_bytes[1:5], byteorder='big')
            return HuffmanNode(char)
        elif tree_bytes[0] == 2:
            char = tree_bytes[1:].decode('utf-8')
            return HuffmanNode(char)
        else:
            left_size = int.from_bytes(tree_bytes[1:5], byteorder='big')
            left_tree = self.decode_tree(tree_bytes[5:5 + left_size])
            right_tree = self.decode_tree(tree_bytes[5 + left_size:])
            root = HuffmanNode()
            root.left = left_tree
            root.right = right_tree
            return root
