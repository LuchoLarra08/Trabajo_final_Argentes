import pygame
import json
from datetime import datetime
import os
from .constantes import *
from .funciones import mostrar_texto 


fuente = pygame.font.SysFont("Arial Narrow", 38)
fuente_boton = pygame.font.SysFont("Arial Narrow", 23)

boton_volver = pygame.image.load("assets/images/boton_volver.png")
boton_volver = pygame.transform.scale(boton_volver, TAMAÑO_BOTON_VOLUMEN)

fondo_rankings = pygame.image.load("assets/images/fondo_rankings.png") # Asumo que tu archivo es .jpg
fondo_rankings = pygame.transform.scale(fondo_rankings,(VENTANA))

def abrir_json(ruta: str) -> list:
    '''
    Abre un archivo JSON y devuelve su contenido como una lista de dicccionarios.
    
    Parámetros:
    - ruta: Ruta del archivo JSON.
    
    Retorna una lista con el contenido del archivo o una lista vacía.
    '''
    if os.path.exists(ruta):
        with open(ruta, "r") as archivo:
            contenido = json.load(archivo)
            if len(contenido) == 0:
                contenido = []
    else:
        contenido = []
    return contenido


def guardar_ranking(nombre:str, puntaje:int) -> None:
    '''
    Guarda un nuevo ranking en un archivo JSON, añadiendo la fecha y hora actual junto con el nombre y puntaje del jugador.
    
    Parámetros:
    - nombre: Nombre del jugador.
    - puntaje: Puntaje obtenido por el jugador.
    
    No retorna nada
    '''
    nuevo_ranking = {
        "nombre": nombre,
        "puntaje": puntaje,
        "fecha": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }
    
    rankings = abrir_json("data/rankings.json")
    rankings.append(nuevo_ranking)
    
    with open("data/rankings.json", "w") as archivo:
        json.dump(rankings, archivo, indent=4)



def ordenar_rankings():
    '''
    Ordena los rankings del archivo JSON de manera descendente según el puntaje de los jugadores.
    
    Retorna una lista de diccionarios donde cada diccionario contiene la información de un jugador (nombre, puntaje, fecha).
    '''
    rankings = abrir_json("data/rankings.json")
    
    for i in range(len(rankings) - 1):
        for j in range(i + 1, len(rankings)):
            if rankings[i]["puntaje"] < rankings[j]["puntaje"]:
                aux = rankings[i]
                rankings[i] = rankings[j]
                rankings[j] = aux
    
    return rankings


def mostrar_rankings(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event]) -> str:
    '''
    Muestra la pantalla de rankings del juego (lista de los jugadores ordenados y volver al menú).
    
    Parámetros:
    - pantalla: Superficie de Pygame donde se dibujan los elementos de la pantalla.
    - cola_eventos: Lista de eventos para detectar clics del mouse y el cierre de la ventana.
    
    Retorna un string que indica a qué ventana se debe dirigir el juego. 
    '''

    retorno = "rankings"
    rankings = ordenar_rankings()
    
    pantalla.blit(fondo_rankings, (0, 0))
    boton_volver_rect = pantalla.blit(boton_volver, (10, 10))
    
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_volver_rect.collidepoint(evento.pos):
                CLICK_SONIDO.play()
                retorno = "menu"
    
    posicion_y = 80
    # Asegurarse de no intentar mostrar más elementos de los que hay en la lista
    # Usamos min(10, len(rankings)) para evitar errores si hay menos de 10 rankings
    for i in range(min(10, len(rankings))): 
        mostrar_texto(pantalla,f"{i + 1}. {rankings[i]['nombre']} - {rankings[i]['puntaje']} puntos - {rankings[i]['fecha']}",(145, posicion_y),fuente,COLOR_BLANCO)
        posicion_y += 40
    
    return retorno