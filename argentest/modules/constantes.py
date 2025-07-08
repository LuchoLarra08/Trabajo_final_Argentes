import pygame

# COLORES
COLOR_BLANCO = (255,255,255)
COLOR_NEGRO = (0,0,0)
COLOR_VERDE = (0,255,0)
COLOR_ROJO = (255,0,0)
COLOR_AZUL = (0,0,35)
COLOR_VIOLETA = (134,23,219)

# PANTALLA
ANCHO = 800
ALTO = 600
VENTANA = (ANCHO,ALTO)
FPS = 60

# BOTONES
BOTON_JUGAR = 0
BOTON_CONFIG = 1
BOTON_PUNTUACIONES = 2
BOTON_SALIR = 3
BOTON_ADICIONAL = 4
BOTON_DOBLE_CHANCE = 5
BOTON_BOMBA = 6


# TAMAÑOS
TAMAÑO_PREGUNTA = (56, 74)
TAMAÑO_RESPUESTA = (200,60)
TAMAÑO_BOTON = (350,110)
CUADRO_TEXTO = (250,50)
TAMAÑO_BOTON_VOLUMEN = (60,60)
TAMAÑO_BOTON_VOLVER = (100,40)
TAMAÑO_IMAGEN_PREG = (710,210)
TAMAÑO_IMAGEN_COMODIN = (45,45)

MAX_VOLUMEN_REAL = 0.04


# SONIDO
CLICK_SONIDO = pygame.mixer.Sound("assets/sounds/click.mp3")
CLICK_SONIDO.set_volume(0.2) # Volumen inicial del sonido al cargarse
ERROR_SONIDO = pygame.mixer.Sound("assets/sounds/error.mp3")
ERROR_SONIDO.set_volume(0.02) # Volumen inicial del sonido al cargarse
ACIERTO_SONIDO = pygame.mixer.Sound("assets/sounds/acierto.mp3")
ACIERTO_SONIDO.set_volume(0.02) # Volumen inicial del sonido al cargarse


CANTIDAD_VIDAS = 3
PUNTUACION_ACIERTO = 100
PUNTUACION_ERROR = 25