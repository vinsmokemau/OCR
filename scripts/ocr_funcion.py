# -*- coding: utf-8 -*-
"""OCR_funcion.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kb8GUyOOxv-DJX7T7024m1LlD_QKgVgB
"""

import cv2
import pytesseract

"""# OCR_funcion"""

def OCR_extraccion(imagen_name):
    #Lectura mediante opencv
    imagen = cv2.imread(imagen_name)
    imagen = cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR)
    
    text = pytesseract.image_to_string(imagen)
    
    names = {}
    name = ""
    name_count = 0
    for letter in text:
        if letter != "\n":
            name += letter
        else:
            names['name_' + str(name_count)] = name
            name = ""
            name_count += 1
    names['name_' + str(name_count)] = name
    
    return names
