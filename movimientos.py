from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sound import Sound
from time import sleep
import threading
import signal
import sys
from ev3dev2.motor import MoveSteering

# Crear un objeto MoveSteering para controlar ambos motores simultáneamente
steer_pair = MoveSteering(OUTPUT_B, OUTPUT_C)
# Definir los motores y el puerto del sensor de color
INPUT_4 = 'in4'  # Ajusta el puerto según tu configuración
INPUT_2 = 'in2'
INPUT_1 = 'in1'  # Ajusta el puerto según tu configuración
sensor_proximidad = UltrasonicSensor(INPUT_1)

motor_b = LargeMotor(OUTPUT_B)
motor_c = LargeMotor(OUTPUT_C)
sensor_color = ColorSensor(INPUT_4)
altavoz = Sound()
altavoz.volume = 100
gyro_sensor = GyroSensor(INPUT_2)

# Calibrar el sensor giroscópico
gyro_sensor.mode = 'GYRO-RATE'
gyro_sensor.mode = 'GYRO-ANG'

# Función para obtener el ángulo actual del giroscopio
def obtener_angulo():
    gyro_sensor.mode = 'GYRO-ANG'  # Asegurarse de que el sensor esté en modo de ángulo
    return gyro_sensor.value()


# Función para girar el robot utilizando el giroscopio
# Función para girar el robot utilizando el giroscopio
def girar_con_giroscopio(angulo_deseado):
    global estado_robot
    estado_robot = "girando"

    velocidad_giro = 20  # Ajusta la velocidad de giro según sea necesario
    margen_error = 2  # Margen de error aceptable en grados

    angulo_actual = obtener_angulo()

    while abs(angulo_actual - angulo_deseado) > margen_error:
        if angulo_actual < angulo_deseado:
            motor_b.on(speed=velocidad_giro)
            motor_c.on(speed=-velocidad_giro)
        else:
            motor_b.on(speed=-velocidad_giro)
            motor_c.on(speed=velocidad_giro)

        angulo_actual = obtener_angulo()

    motor_b.off()
    motor_c.off()
    estado_robot = "adelante"

# Inicializar el ángulo del giroscopio al inicio del programa
gyro_sensor.mode = 'GYRO-RATE'
sleep(1)  # Esperar un segundo para asegurarse de que el modo se cambie correctamente
gyro_sensor.mode = 'GYRO-ANG'

edificios = {
    'Mi ubicacion': {
        'minutos': 0,
        'color': 'verde',
        'conexiones': {'Bomberos': {'tiempo': 1, 'direccion': 'adelante'}}
    },
    'Bomberos': {
        'minutos': 0,
        'color': 'verde',
        'conexiones': {
            'Museo': {'tiempo': 2, 'direccion': 'derecha'}, 
            'Policia':{'tiempo': 2, 'direccion': 'iquierda'}, 
            'Iglesia': {'tiempo': 1, 'direccion': 'adelante'}
            }
    },
    'Museo': {
        'minutos': 0,
        'color': 'negro',
        'conexiones': {
            'Bomberos': {'tiempo': 2, 'direccion': 'iquierda'},
            'Restaurante': {'tiempo': 1, 'direccion': 'adelante'}
            }
    },
    'Restaurante': {
        'minutos': 0,
        'color': 'azul',
        'conexiones': {
            'Museo': {'tiempo': 1, 'direccion': 'atras'},
            'Iglesia': {'tiempo': 3, 'direccion': 'izquierda'},
            'Gasolinera': {'tiempo': 1, 'direccion': 'adelante'}
            }
    },
    'Gasolinera': {
        'minutos': 0,
        'color': 'amarillo',
        'conexiones': {
            'Restaurante': {'tiempo': 1, 'direccion': 'atras'},
            'Parque': {'tiempo': 2, 'direccion': 'izquierda'},
            'Centro Comercial': {'tiempo': 7, 'direccion': 'adelante'}
            }
    },
    'Centro Comercial': {
        'minutos': 0,
        'color': 'cafe',
        'conexiones': {
            'Gasolinera': {'tiempo': 1, 'direccion': 'atras'},
            'Gym': {'tiempo': 1, 'direccion': 'izquierda'}
            }
    },
    'Gym': {
        'minutos': 0,
        'color': 'celeste',
        'conexiones': {
            'Centro Comercial': {'tiempo': 1, 'direccion': 'derecha'},
            'Parque': {'tiempo': 3, 'direccion': 'atras'},
            'Hotel': {'tiempo': 1, 'direccion': 'izquierda'}
            }
        
    },
    'Parque': {
        'minutos': 0,
        'color': 'naranja',
        'conexiones': {
            'Gym': {'tiempo': 3, 'direccion': 'adelante'},
            'Gasolinera': {'tiempo': 2, 'direccion': 'derecha'},
            'Colegio': {'tiempo': 3, 'direccion': 'izquierda'},
            'Iglesia': {'tiempo': 3, 'direccion': 'atras'}
            }
    },
    'Iglesia': {
        'minutos': 0,
        'color': 'blanco',
        'conexiones': {
            'Parque': {'tiempo': 3, 'direccion': 'adelante'}, 
            'Restaurante': {'tiempo': 3, 'direccion': 'derecha'},
            'Bomberos': {'tiempo': 1, 'direccion': 'atras'},
            'Municipalidad': {'tiempo': 2, 'direccion': 'izquierda'}
            }
    },
    'Policia': {
        'minutos': 0,
        'color': 'blanco',
        'conexiones': {
            'Bomberos': {'tiempo': 2, 'direccion': 'derecha'},
            'Municipalidad': {'tiempo': 2, 'direccion': 'adelante'}
            }
    },
    'Municipalidad': {
        'minutos': 0,
        'color': 'blanco',
        'conexiones': {
            'Policia': {'tiempo': 2, 'direccion': 'atras'},
            'Iglesia': {'tiempo': 2, 'direccion': 'derecha'},
            'Colegio': {'tiempo': 2, 'direccion': 'adelante'}
            }
    },
    'Colegio': {
        'minutos': 0,
        'color': 'blanco',
        'conexiones': {
            'Municipalidad': {'tiempo': 2, 'direccion': 'atras'},
            'Parque': {'tiempo': 3, 'direccion': 'derecha'},
            'Hotel': {'tiempo': 1, 'direccion': 'adelante'}
            }
        
    },
    'Hotel': {
        'minutos': 0,
        'color': 'blanco',
        'conexiones': {
            'Gym': {'tiempo': 1, 'direccion': 'derecha'}, 
            'Colegio': {'tiempo': 1, 'direccion': 'atras'}
            }
    },
}

# Función para encontrar la mejor ruta utilizando el algoritmo de Dijkstra
def encontrar_mejor_ruta(edificios, inicio, destino):
    tiempos_acumulativos = {edificio: float('inf') for edificio in edificios}
    tiempos_acumulativos[inicio] = 0
    rutas = {inicio: []}
    no_visitados = list(edificios.keys())

    while no_visitados:
        edificio_actual = min(no_visitados, key=lambda edificio: tiempos_acumulativos[edificio])

        if edificio_actual == destino:
            return rutas[destino] + [destino]

        conexiones = edificios[edificio_actual]['conexiones']
        for conexion, info in conexiones.items():
            tiempo = info['tiempo']
            if tiempos_acumulativos[edificio_actual] + tiempo < tiempos_acumulativos[conexion]:
                tiempos_acumulativos[conexion] = tiempos_acumulativos[edificio_actual] + tiempo
                rutas[conexion] = rutas[edificio_actual] + [edificio_actual]

        no_visitados.remove(edificio_actual)

    return None



# Variable compartida para indicar el estado del robot
estado_robot = "adelante"

# Bandera para controlar el hilo de movimientos
detener_hilo_programa = False

# Función para mover el robot hacia adelante
def mover_adelante():
    global estado_robot
    estado_robot = "adelante"
    velocidad = 12
    altavoz.speak("Moving forward")
    motor_b.on(speed=velocidad)
    motor_c.on(speed=velocidad)
    sleep(7)
    motor_b.off()
    motor_c.off()


# Función para iniciar el programa de movimientos
def iniciar_programa():
    global estado_robot
    altavoz.speak("Hello! I am ready to move.")
    inicio = 'Mi ubicacion'
    destino = 'Hotel'
    mejor_ruta = encontrar_mejor_ruta(edificios, inicio, destino)

    if mejor_ruta:

        print('Mejor ruta de {} a {}: {}'.format(inicio, destino, mejor_ruta))

        for i in range(len(mejor_ruta) - 1):
            edificio_actual = mejor_ruta[i]
            siguiente_edificio = mejor_ruta[i + 1]

            # Mover el robot entre edificios
            mover_entre_edificios(edificio_actual, siguiente_edificio)

            # Verificar la proximidad antes de seguir a la siguiente ubicación
            distancia_proximidad = sensor_proximidad.distance_centimeters
            if distancia_proximidad < 10:  # Ajusta el umbral según tus necesidades
                print('¡Objeto cercano detectado! Deteniendo el robot.')
                estado_robot = "detener"
                altavoz.speak("Object detected. Stopping the robot.")
                detener_hilo_programa = True
                sys.exit(0)
                break  # Salir del bucle si se detecta un objeto cercano

        # Realizar el último movimiento hacia el destino final
        if mejor_ruta[-1] == destino:
            edificio_actual = mejor_ruta[-1]
            siguiente_edificio = None  # Puedes establecer esto según tu lógica
            mover_entre_edificios(edificio_actual, siguiente_edificio)
    else:
        print('No hay ruta disponible de {} a {}'.format(inicio, destino))




# Función para mover el robot entre dos edificios basado en el grafo
def mover_entre_edificios(edificio_actual, siguiente_edificio):
    global estado_robot
    conexiones = edificios[edificio_actual]['conexiones']

    # Verificar si el siguiente edificio está conectado al edificio actual
    if siguiente_edificio in conexiones:
        direccion = conexiones[siguiente_edificio]['direccion']

        if direccion == 'adelante':
            steer_pair.on_for_seconds(0, 12, 7)  # Mover hacia adelante

        elif direccion == 'izquierda':
            girar_con_giroscopio(-90)  # Giro a la izquierda
            steer_pair.on_for_seconds(0, 12, 7)  # Mover hacia adelante después de girar
            girar_con_giroscopio(0)  # Ajusta el ángulo según sea necesario
        elif direccion == 'derecha':
            girar_con_giroscopio(90)  # Giro a la derecha
            steer_pair.on_for_seconds(0, 12, 7)  # Mover hacia adelante después de girar
            girar_con_giroscopio(0)  # Ajusta el ángulo según sea necesario
        elif direccion == 'atras':
            steer_pair.on_for_seconds(0, -12, 7)  # Mover hacia atrás
            girar_con_giroscopio(180)  # Giro de 180 grados
            steer_pair.on_for_seconds(0, 12, 7)  # Mover hacia adelante después de girar
            girar_con_giroscopio(0)  # Ajusta el ángulo según sea necesario

        # Ajusta este tiempo según la velocidad y la duración de tus movimientos
        sleep(3)

        steer_pair.off()  # Detener el robot
        girar_con_giroscopio(0)  # Asegurarse de que el ángulo esté en cero

    else:
        print('Error: {} no está conectado a {}'.format(siguiente_edificio, edificio_actual))


def ejecutar_programa():
    global detener_hilo_programa
    inicio = 'Mi ubicacion'
    destino = input("Ingrese el destino: ")  # Solicitar al usuario que ingrese el destino
    mejor_ruta = encontrar_mejor_ruta(edificios, inicio, destino)
    altavoz.speak("Hello world")
    if mejor_ruta:
        print('Mejor ruta de {} a {}: {}'.format(inicio, destino, mejor_ruta))

        for i in range(len(mejor_ruta) - 1):
            edificio_actual = mejor_ruta[i]
            siguiente_edificio = mejor_ruta[i + 1]

            # Mover el robot entre edificios
            mover_entre_edificios(edificio_actual, siguiente_edificio)

            # Verificar la proximidad antes de seguir a la siguiente ubicación
            distancia_proximidad = sensor_proximidad.distance_centimeters
            if distancia_proximidad < 10:  # Ajusta el umbral según tus necesidades
                print('¡Objeto cercano detectado! Deteniendo el robot.')
                break  # Salir del bucle si se detecta un objeto cercano
                detener_hilo_programa = True  # Añade esta línea
        # Realizar el último movimiento hacia el destino final de manera especial
        if mejor_ruta[-1] == destino and i == len(mejor_ruta) - 2:
            edificio_actual = mejor_ruta[-1]
            siguiente_edificio = None  # Este es el último edificio, no hay siguiente
            mover_entre_edificios(edificio_actual, siguiente_edificio)
            print("¡Llegó a su destino!")
            altavoz.speak("¡Llegó a su destino!")
    else:
        print('No hay ruta disponible de {} a {}'.format(inicio, destino))

# Manejar la señal de interrupción (Ctrl + C)
def manejar_interrupcion(signal, frame):
    print('Programa detenido por el usuario')
    sys.exit(0)

# Configurar el manejador de la señal de interrupción
signal.signal(signal.SIGINT, manejar_interrupcion)

# Ejecutar el programa principal
ejecutar_programa()