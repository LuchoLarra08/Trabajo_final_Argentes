import pygame

pygame.init()
pygame.mixer.init()

from modules.constantes import *
from modules.menu import *
from modules.juego import *
from modules.configuracion import *
from modules.rankings import *
from modules.terminado import *

from modules.constantes import MAX_VOLUMEN_REAL


pygame.display.set_caption("Argentest")

pantalla = pygame.display.set_mode(VENTANA)

icono = pygame.image.load("assets/images/icono.png") 
pygame.display.set_icon(icono)

corriendo = True
reloj = pygame.time.Clock()
datos_juego = {"puntuacion": 0,
                "vidas": CANTIDAD_VIDAS,
                "nombre": "",
                "volumen_musica": 50, 
                "tiempo": 180,
                "acierto": 100,
                "fallo": 25
                }
ventana_actual = "menu"
bandera_musica_juego = False
bandera_musica_menu = False


while corriendo:
    reloj.tick(FPS)
    
    cola_eventos = pygame.event.get()
    
# En el bloque del MENÚ:
    if ventana_actual == "menu":
        if bandera_musica_menu == False:
            pygame.mixer.music.load("assets/sounds/musica_menu.mp3")
            # Aplicar volumen escalado usando MAX_VOLUMEN_REAL
            pygame.mixer.music.set_volume((datos_juego["volumen_musica"] / 100) * MAX_VOLUMEN_REAL)
            pygame.mixer.music.play(-1)
            bandera_musica_menu = True
        ventana_actual = mostrar_menu(pantalla, cola_eventos)
        
# En el bloque del JUEGO:
    elif ventana_actual == "juego":
        if datos_juego["vidas"] <= 0:
            ventana_actual = "terminado"
        else:
            # Calcular el porcentaje de volumen escalado para Pygame
            porcentaje_volumen_pygame = (datos_juego["volumen_musica"] / 100) * MAX_VOLUMEN_REAL
            # Si la música del juego no está sonando, cargarla y empezar a reproducir
            if bandera_musica_juego == False:
                pygame.mixer.music.load("assets/sounds/musica_juego.mp3")
                pygame.mixer.music.play(-1)
                bandera_musica_juego = True
            # Siempre aplicar el volumen actual (en caso de que se haya cambiado en configuraciones)
            pygame.mixer.music.set_volume(porcentaje_volumen_pygame)
            ventana_actual = mostrar_juego(pantalla, cola_eventos, datos_juego)
    
    elif ventana_actual == "configuraciones":
        ventana_actual = mostrar_configuracion(pantalla, cola_eventos, datos_juego)
    elif ventana_actual == "rankings":
        ventana_actual = mostrar_rankings(pantalla, cola_eventos)
    elif ventana_actual == "terminado":
        if bandera_musica_juego == True:
            pygame.mixer.music.stop()
            bandera_musica_juego = False
        if bandera_musica_menu == True:
            pygame.mixer.music.stop()
            bandera_musica_menu = False
        ventana_actual = mostrar_fin_juego(pantalla, cola_eventos, datos_juego)

    elif ventana_actual == "salir":
        corriendo = False
    
    pygame.display.flip()

pygame.quit()