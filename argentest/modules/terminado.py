import pygame
from .constantes import * 
from .funciones import mostrar_texto 
from .rankings import guardar_ranking  

fuente = pygame.font.SysFont("Arial Narrow", 40)
cuadro = {}
cuadro["superficie"] = pygame.Surface(CUADRO_TEXTO)
cuadro["rectangulo"] = cuadro["superficie"].get_rect()
cuadro['superficie'].fill((200, 200, 200))

# Solo cargamos el fondo, que no necesita convert_alpha
fondo_termino = pygame.image.load("assets/images/fondo_game_over.png")
fondo_termino = pygame.transform.scale(fondo_termino, VENTANA)

nombre = ""
bandera_mayuscula = False

def verificar_texto(caracter: str) -> bool:
    '''
    Verifica si un carácter es alfanumérico o tiene un espacio en blanco.
    '''
    return caracter.isalnum() or caracter == " "


def mostrar_fin_juego(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict) -> str:
    '''
    Muestra la pantalla de fin de juego, permitiendo al jugador ingresar su nombre y guardar el ranking.
    '''
    global nombre
    global bandera_mayuscula
    retorno = "terminado"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.KEYDOWN:
            letra_presionada = pygame.key.name(evento.key)

            if evento.key == pygame.K_CAPSLOCK:
                bandera_mayuscula = not bandera_mayuscula

            es_mayuscula_actual = (pygame.key.get_mods() & pygame.KMOD_SHIFT) or (pygame.key.get_mods() & pygame.KMOD_CAPS)

            if len(letra_presionada) == 1:
                if verificar_texto(letra_presionada):
                    if es_mayuscula_actual:
                        nombre += letra_presionada.upper()
                    else:
                        nombre += letra_presionada.lower()

            if letra_presionada == "backspace" and len(nombre) > 0:
                nombre = nombre[:-1]
                cuadro["superficie"].fill(COLOR_VIOLETA)

            if letra_presionada == "space":
                nombre += " "

            if evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                guardar_ranking(nombre, datos_juego["puntuacion"])
                datos_juego["vidas"] = 3
                datos_juego["puntuacion"] = 0
                nombre = ""
                retorno = "menu"

    pantalla.blit(fondo_termino, (0, 0))

    # Cargar y escalar la imagen Game Over solo la primera vez
    if not hasattr(mostrar_fin_juego, "imagen_game_over"):
        imagen_original = pygame.image.load("assets/images/game.png").convert_alpha()
        ancho = int(imagen_original.get_width() * 0.8)
        alto = int(imagen_original.get_height() * 0.8)
        mostrar_fin_juego.imagen_game_over = pygame.transform.scale(imagen_original, (ancho, alto))

    game_over = mostrar_fin_juego.imagen_game_over
    rect_game_over = game_over.get_rect(center=(VENTANA[0] // 2, 100))
    pantalla.blit(game_over, rect_game_over)

    cuadro["superficie"].fill((200, 200, 200))

    if pygame.time.get_ticks() % 1000 < 500:
        texto_mostrado = nombre + "|"
    else:
        texto_mostrado = nombre

    mostrar_texto(cuadro["superficie"], texto_mostrado, (10, 0), fuente, COLOR_BLANCO)

    pos_x = (VENTANA[0] - CUADRO_TEXTO[0]) // 2
    cuadro["rectangulo"] = pantalla.blit(cuadro["superficie"], (pos_x, 260))
    mostrar_texto(pantalla, f"Usted obtuvo: {datos_juego['puntuacion']} puntos", (250, 200), fuente, COLOR_BLANCO)

    return retorno
