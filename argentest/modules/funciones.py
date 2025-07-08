import random
from .constantes import * 
import pygame
import os
import json


def mostrar_texto(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]   
    space = font.size(' ')[0]
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, False, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]   
                y += word_height   
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  
        y += word_height 


def mezclar_lista(lista_preguntas:list) -> None:
    '''
    Mezcla aleatoriamente el orden de los elementos en la lista de preguntas.

    Parámetros:
    - lista_preguntas: Lista de preguntas que se deben mezclar, cada elemento es un diccionario que representa una pregunta y sus respuestas.

    No retorna nada.
    '''
    random.shuffle(lista_preguntas)


def verificar_respuesta(datos_juego:dict,pregunta_actual:dict,respuesta:int) -> bool:
    '''
    Verifica si la respuesta del jugador es correcta y actualiza los datos del juego en consecuencia.
    '''

    if respuesta == int(pregunta_actual["RespuestaCorrecta"]):
        retorno = True
    else:
        retorno = False
    
    return retorno


def reiniciar_estadisticas(datos_juego:dict) -> None:
    '''
    Reinicia las estadísticas del juego a sus valores iniciales.

    Parámetros:
    - datos_juego: Diccionario que contiene los datos actuales del juego.

    No retorna nada.
    '''
    datos_juego["puntuacion"] = 0
    datos_juego["vidas"] = CANTIDAD_VIDAS


# FUNCIONES DE MANEJO DE ARCHIVO PARA PREGUNTAS.

def obtener_claves(archivo,separador:str) -> list:
    '''
    Lee la primera línea de un archivo y extrae las claves separadas por un separador.
    
    Parámetros:
    - archivo: El archivo desde el que se leerá la primera línea.
    - separador: El carácter que separa las claves de la primera línea.
    
    Retorna una lista que contiene las claves extraídas de la primera línea del archivo.
    '''
    primer_linea = archivo.readline()
    primer_linea = primer_linea.replace("\n","")
    primer_linea = primer_linea.strip('\ufeff')
    lista_claves = primer_linea.split(separador)
    
    return lista_claves

def obtener_valores(linea,separador:str) -> list:
    '''
    Separa una línea de texto en valores, usando un delimitador especificado.

    Parámetros:
    - linea: La línea de texto que contiene los valores separados por el separador.
    - separador: El carácter que separa los valores en la línea.

    Retorna una lista de valores obtenidos al dividir la línea usando el separador.
    '''
    linea_aux = linea.replace("\n","")
    lista_valores = linea_aux.split(separador)
    return lista_valores

def crear_diccionario(lista_claves:list,lista_valores:list) -> dict:
    '''
    Crea un diccionario a partir de dos listas: una con claves y otra con valores.

    Parámetros:
    - lista_claves: Lista de claves que se utilizarán para el diccionario.
    - lista_valores: Lista de valores correspondientes a las claves.

    Retorna un diccionario donde las claves son extraídas de `lista_claves` y los valores son extraídos de `lista_valores`.
    '''
    diccionario_aux = {}
    for i in range(len(lista_claves)):
        clave = lista_claves[i]
        valor = lista_valores[i]
        
        # Si la clave es "RespuestaCorrecta", intentar convertir el valor a un int
        if clave == "RespuestaCorrecta": 
                valor = int(valor)   # Convertir a entero
                
        diccionario_aux[clave] = valor
    return diccionario_aux

def parse_csv(lista_elementos,nombre_archivo:str) -> bool: 
    '''
    Lee un archivo CSV, procesa su contenido y lo almacena en una lista de diccionarios.

    Parámetros:
    - lista_elementos: Lista vacía que se llenará con los diccionarios generados del archivo CSV.
    - nombre_archivo: El nombre del archivo CSV que se leerá.

    Retorna un booleano, devuelve True si el archivo fue procesado correctamente y los datos fueron agregados a lista_elementos, o False si el archivo no existe.
    '''
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo,"r",encoding='utf-8') as archivo:
            lista_claves = obtener_claves(archivo,",")
            for linea in archivo:
                lista_valores = obtener_valores(linea,",")
                diccionario_aux = crear_diccionario(lista_claves,lista_valores) 
                lista_elementos.append(diccionario_aux)         
        return True
    else:
        return False