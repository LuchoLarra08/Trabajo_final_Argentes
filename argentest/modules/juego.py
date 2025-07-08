import pygame
import random 
from .constantes import * 
from .preguntas import * 
from .funciones import * 

fondo = pygame.image.load("assets/images/fondo_juego.png") # Ruta corregida
fondo = pygame.transform.scale(fondo, VENTANA)

cuadro_pregunta = {}
cuadro_pregunta["superficie"] = pygame.image.load("assets/images/fondo_pregunta.png")
cuadro_pregunta["superficie"] = pygame.transform.scale(cuadro_pregunta["superficie"], TAMAÑO_IMAGEN_PREG)
cuadro_pregunta["rectangulo"] = cuadro_pregunta["superficie"].get_rect()


bandera_comodin_usado_pasar = False
bandera_comodin_visible_pasar = True
imagen_comodin_pasar = pygame.image.load("assets/images/pasar.png") 
imagen_comodin_pasar = pygame.transform.scale(imagen_comodin_pasar, TAMAÑO_IMAGEN_COMODIN)

imagen_comodin_x2 = pygame.image.load("assets/images/x2.png") 
imagen_comodin_x2 = pygame.transform.scale(imagen_comodin_x2, TAMAÑO_IMAGEN_COMODIN)

imagen_comodin_doble_chance = pygame.image.load("assets/images/doble_chance.png")
imagen_comodin_doble_chance = pygame.transform.scale(imagen_comodin_doble_chance, TAMAÑO_IMAGEN_COMODIN)

imagen_comodin_bomba = pygame.image.load("assets/images/bomba.png") # Cargar imagen Bomba
imagen_comodin_bomba = pygame.transform.scale(imagen_comodin_bomba, TAMAÑO_IMAGEN_COMODIN)


cartas_respuestas = []
for i in range(4):
    cuadro_respuesta = {}
    cuadro_respuesta["superficie"] = pygame.Surface(TAMAÑO_RESPUESTA)
    cuadro_respuesta["rectangulo"] = cuadro_respuesta["superficie"].get_rect()
    cartas_respuestas.append(cuadro_respuesta)

fuente_prgunta = pygame.font.SysFont("Arial Narrow", 30)
fuente_respuesta = pygame.font.SysFont("Arial Narrow", 30)
fuente_texto = pygame.font.SysFont("Arial Narrow", 25)

bandera_vida_extra_visible = False
tiempo_fin_vida_extra_display = 0

bandera_comodin_doble_chance_usado = False
bandera_comodin_doble_chance_visible = True
bandera_doble_chance_activa_pregunta = False 

bandera_comodin_bomba_usado = False
bandera_comodin_bomba_visible = True

mezclar_lista(lista_preguntas)
indice = 0
respuestas_correctas_consecutivas = 0
bandera_respuesta = False 

opciones_visibles = [True, True, True, True] 

clock = pygame.time.Clock()
evento_tiempo_1s = pygame.USEREVENT
pygame.time.set_timer(evento_tiempo_1s, 1000)

bandera_comodin_x2_usado = False 
bandera_comodin_x2_visible = True

def mostrar_juego(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict) -> str:
    '''
    Muestra la pantalla de juego, maneja las interacciones del usuario con las respuestas, el uso de comodines, el temporizador y la puntuación.
    '''

    global indice
    global bandera_respuesta
    global respuestas_correctas_consecutivas
    global bandera_comodin_x2_usado
    global bandera_comodin_x2_visible
    global bandera_comodin_usado_pasar
    global bandera_comodin_visible_pasar
    global bandera_vida_extra_visible
    global tiempo_fin_vida_extra_display
    global bandera_comodin_doble_chance_usado
    global bandera_comodin_doble_chance_visible
    global bandera_doble_chance_activa_pregunta
    global bandera_comodin_bomba_usado
    global bandera_comodin_bomba_visible
    global opciones_visibles # Para controlar qué opciones se muestran/son clickeables después de Bomba
    
    retorno = "juego"

    for carta in cartas_respuestas:
        carta["superficie"].fill(COLOR_AZUL)
        
    if bandera_respuesta:
        cuadro_pregunta["superficie"] = pygame.image.load("assets/images/fondo_pregunta.png")
        cuadro_pregunta["superficie"] = pygame.transform.scale(cuadro_pregunta["superficie"], TAMAÑO_IMAGEN_PREG)
        pygame.time.delay(500) # Pequeña pausa antes de la siguiente pregunta/estado
        
        # Solo avanzar a la siguiente pregunta si no es una segunda chance fallida
        if not bandera_doble_chance_activa_pregunta: # Esto se activa al ganar o perder en el segundo intento
            if indice == len(lista_preguntas) - 1: # Si es la última pregunta, reiniciar
                indice = 0
                mezclar_lista(lista_preguntas)
            else:
                indice += 1
            opciones_visibles = [True, True, True, True]
            bandera_respuesta = False # Resetear la bandera para la siguiente interacción
        # Si bandera_doble_chance_activa_pregunta es True, significa que falló la primera vez y no avanza la pregunta

    pregunta_actual = lista_preguntas[indice]
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == evento_tiempo_1s:
            if datos_juego["tiempo"] > 0:
                datos_juego["tiempo"] -= 1
            else:
                datos_juego["tiempo"] = 60
                retorno = "terminado"
        
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = evento.pos # Obtener la posición del clic del mouse

            rect_comodin_x2 = imagen_comodin_x2.get_rect(topleft=(10, 25))
            rect_comodin_pasar = imagen_comodin_pasar.get_rect(topleft=(70, 25))
            rect_comodin_doble_chance = imagen_comodin_doble_chance.get_rect(topleft=(130, 25))
            rect_comodin_bomba = imagen_comodin_bomba.get_rect(topleft=(190, 25))

            # Lógica para comodín X2
            if not bandera_comodin_x2_usado and rect_comodin_x2.collidepoint(mouse_pos):
                bandera_comodin_x2_usado = True
                bandera_comodin_x2_visible = False
                CLICK_SONIDO.play()

            # Lógica para comodín PASAR
            elif not bandera_comodin_usado_pasar and rect_comodin_pasar.collidepoint(mouse_pos):
                CLICK_SONIDO.play()
                bandera_respuesta = True # Marcar para avanzar a la siguiente pregunta
                bandera_comodin_usado_pasar = True
                bandera_comodin_visible_pasar = False
                # La lógica de avance de pregunta se manejará centralmente en el if bandera_respuesta:
                opciones_visibles = [True, True, True, True]

            # Lógica para comodín DOBLE CHANCE
            elif not bandera_comodin_doble_chance_usado and rect_comodin_doble_chance.collidepoint(mouse_pos):
                CLICK_SONIDO.play()
                bandera_comodin_doble_chance_usado = True # Marcar como usado (una vez por partida)
                bandera_comodin_doble_chance_visible = False # Ocultar icono del comodín
                bandera_doble_chance_activa_pregunta = True 
                
            # Lógica para comodín BOMBA
            elif not bandera_comodin_bomba_usado and rect_comodin_bomba.collidepoint(mouse_pos):
                CLICK_SONIDO.play()
                bandera_comodin_bomba_usado = True # Marcar como usado (una vez por partida)
                bandera_comodin_bomba_visible = False # Ocultar icono del comodín
                
                respuesta_correcta_num = int(pregunta_actual["RespuestaCorrecta"]) - 1

                # Obtener índices de opciones incorrectas (excluyendo la correcta)
                indices_incorrectos = [i for i in range(4) if i != respuesta_correcta_num]
                
                # Eliminar dos opciones incorrectas aleatoriamente
                if len(indices_incorrectos) >= 2: # Asegurarse de que haya al menos 2 incorrectas para eliminar
                    # random.sample selecciona 2 elementos únicos de la lista
                    indices_a_eliminar = random.sample(indices_incorrectos, 2)
                    for idx in indices_a_eliminar:
                        opciones_visibles[idx] = False # Marcar la opción como no visible
                else:
                    # Si hay 0 o 1 incorrecta (por ejemplo, si la pregunta ya es muy fácil o rara)
                    pass 

            # Lógica para seleccionar respuestas (solo si no se está en un estado de 'respuesta dada' (bandera_respuesta))
            if not bandera_respuesta: 
                for i in range(len(cartas_respuestas)):
                    # Solo procesar el click si la opción es visible (no eliminada por Bomba)
                    if opciones_visibles[i] and cartas_respuestas[i]['rectangulo'].collidepoint(mouse_pos): 
                        respuesta_usuario = (i + 1) 

                        if verificar_respuesta(datos_juego, pregunta_actual, respuesta_usuario):
                            respuestas_correctas_consecutivas += 1
                            if respuestas_correctas_consecutivas == 5:
                                if datos_juego["vidas"] < 3:
                                    datos_juego["vidas"] += 1
                                    global bandera_vida_extra_visible
                                    global tiempo_fin_vida_extra_display
                                    bandera_vida_extra_visible = True
                                    tiempo_fin_vida_extra_display = pygame.time.get_ticks() + 2000
                                datos_juego["tiempo"] += 10
                                respuestas_correctas_consecutivas = 0
                            
                            if bandera_comodin_x2_usado == True: 
                                datos_juego["puntuacion"] += (datos_juego["acierto"] * 2)
                                bandera_comodin_x2_usado = False
                            else:
                                datos_juego["puntuacion"] += datos_juego["acierto"]
                            
                            ACIERTO_SONIDO.play()
                            cartas_respuestas[i]['superficie'].fill(COLOR_VERDE) # Marcar como correcta
                            bandera_doble_chance_activa_pregunta = False # Resetear doble chance si acertó (la consume)
                            bandera_respuesta = True # Marcar para pasar a la siguiente pregunta

                        else: # Respuesta Incorrecta
                            # Si la doble chance está activa (se activó por click previamente)
                            if bandera_doble_chance_activa_pregunta: 
                                # Esto es el primer intento INCORRECTO DESPUÉS DE ACTIVAR EL COMODÍN.
                                bandera_doble_chance_activa_pregunta = False # Consumir el comodín (ya no está activa la doble chance)
                                ERROR_SONIDO.play() # Sonido de error, pero sin penalización real
                                
                                # Ocultar la opción incorrecta que acaba de seleccionar (para la segunda chance)
                                opciones_visibles[i] = False 
                                
                                # Ocultar OTRA opción incorrecta aleatoria (si hay suficientes y no es la correcta)
                                # Generar indices 0,1,2,3 y filtrar
                                opciones_restantes_incorrectas = [idx for idx in range(4) 
                                                                    if idx != (int(pregunta_actual["RespuestaCorrecta"]) - 1) # No la correcta
                                                                    and idx != i # Ni la que acaba de seleccionar
                                                                    and opciones_visibles[idx] # Y que esté visible (no eliminada por bomba)
                                                                ]
                                
                                if len(opciones_restantes_incorrectas) >= 1:
                                    idx_a_ocultar_extra = random.choice(opciones_restantes_incorrectas)
                                    opciones_visibles[idx_a_ocultar_extra] = False
                                
                                # No se activa bandera_respuesta (porque no avanzamos pregunta, esperamos segundo intento)
                                # La función mostrar_juego debe continuar dibujando con las opciones ocultas.
                                return retorno # Salir del evento para esperar el siguiente clic
                            
                            # Si no había doble chance activa, O si es el segundo intento y falló de nuevo
                            else: # No hay doble chance activa o ya se consumió el intento de doble chance
                                datos_juego["vidas"] -= 1 # Ahora sí pierde vida
                                if datos_juego["puntuacion"] > 0 :                      
                                    datos_juego["puntuacion"] -= datos_juego["fallo"]
                                ERROR_SONIDO.play()
                                cartas_respuestas[i]['superficie'].fill(COLOR_ROJO) # Marcar como incorrecta
                                # bandera_doble_chance_activa_pregunta ya es False o se desactiva si lo hubiera hecho antes
                                bandera_respuesta = True # Marcar para avanzar a la siguiente pregunta


    if datos_juego["vidas"] == 0:
        datos_juego["tiempo"] = 180 # Reset tiempo al terminar la partida
        retorno = "terminado"
    
    if retorno == "terminado":
        # Reiniciar todas las banderas de comodines y estado de opciones al terminar la partida
        bandera_comodin_x2_usado = False 
        bandera_comodin_x2_visible = True
        bandera_comodin_usado_pasar = False
        bandera_comodin_visible_pasar = True
        bandera_comodin_doble_chance_usado = False
        bandera_comodin_doble_chance_visible = True
        bandera_comodin_bomba_usado = False
        bandera_comodin_bomba_visible = True
        bandera_doble_chance_activa_pregunta = False # Asegurarse de que no quede activa para la próxima partida
        opciones_visibles = [True, True, True, True] # Asegurarse de que las opciones estén visibles para la próxima partida


    mostrar_texto(cuadro_pregunta["superficie"], f'{pregunta_actual["Pregunta"]}', TAMAÑO_PREGUNTA, fuente_prgunta, COLOR_BLANCO)
    
    pantalla.blit(fondo, (0, 0))
    pantalla.blit(cuadro_pregunta["superficie"], (58, 74))
    
    if bandera_comodin_x2_visible == True:
        pantalla.blit(imagen_comodin_x2, (10, 25))
    
    if bandera_comodin_visible_pasar == True:
        pantalla.blit(imagen_comodin_pasar, (70,25))

    if bandera_comodin_doble_chance_visible:
        pantalla.blit(imagen_comodin_doble_chance, (130, 25)) # Posición para Doble Chance
    if bandera_comodin_bomba_visible:
        pantalla.blit(imagen_comodin_bomba, (190, 25)) # Posición para Bomba

    # --- DIBUJAR RESPUESTAS (solo si son visibles) ---
    # Usar 'opciones_visibles' para controlar qué respuestas se muestran
    opciones_coords = [(170, 325), (170, 450), (465, 325), (465, 450)]
    opciones_nombres = ['OpcionA', 'OpcionB', 'OpcionC', 'OpcionD']

    for i in range(4):
        if opciones_visibles[i]: # Solo dibujar si la opción está marcada como visible
            mostrar_texto(cartas_respuestas[i]["superficie"], f"{pregunta_actual[opciones_nombres[i]]}", (20, 20), fuente_respuesta, COLOR_BLANCO)
            cartas_respuestas[i]['rectangulo'] = pantalla.blit(cartas_respuestas[i]['superficie'], opciones_coords[i])
        else:
            # Si la opción no es visible, asegurarnos de que no sea clickeable o dibujarla como "vacía"
            # Para cubrir visualmente, podrías blitear una superficie del color del fondo de las cartas
            temp_surface = pygame.Surface(TAMAÑO_RESPUESTA)
            temp_surface.fill(COLOR_AZUL) # Asumiendo que COLOR_AZUL es el color de fondo de las cartas
            pantalla.blit(temp_surface, opciones_coords[i])
            pass # No dibujamos la opción si no es visible

    mostrar_texto(pantalla, f"PUNTUACION: {datos_juego['puntuacion']}", (10, 10), fuente_texto, COLOR_BLANCO)
    mostrar_texto(pantalla, f"VIDAS: {datos_juego['vidas']}", (620, 45), fuente_texto, COLOR_BLANCO) 
    mostrar_texto(pantalla, f"TIEMPO RESTANTE: {datos_juego['tiempo']}", (560, 20), fuente_texto, COLOR_ROJO)
    if bandera_vida_extra_visible:
        # Definir una fuente para el mensaje de vida extra (se crea cada frame, se podría optimizar fuera de la función)
        fuente_vida_extra = pygame.font.SysFont("Arial Narrow", 45, bold=True) 
        if pygame.time.get_ticks() < tiempo_fin_vida_extra_display:
            # Calcular posición para centrar el texto
            mensaje = "¡VIDA EXTRA!"
            texto_ancho, texto_alto = fuente_vida_extra.size(mensaje)
            pos_x = (VENTANA[0] - texto_ancho) // 2
            pos_y = (VENTANA[1] - texto_alto) // 2
            mostrar_texto(pantalla, mensaje, (pos_x, pos_y), fuente_vida_extra, COLOR_VERDE)
        else:
            bandera_vida_extra_visible = False # Desactivar la bandera si el tiempo terminó
    
    return retorno