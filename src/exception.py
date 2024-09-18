import sys  # Importa la biblioteca sys, que proporciona funciones relacionadas con el sistema y la ejecución del programa.
from src.logger import logging  # Importa el módulo de registro (logging) desde un archivo 'logger' dentro del paquete 'src'.

# Esta función crea un mensaje de error detallado que incluye el nombre del archivo, la línea donde ocurrió el error y el mensaje del error.
def error_message_detail(error, error_detail: sys):
    # Obtiene información sobre la excepción actual (error) usando sys.exc_info().
    _, _, exc_tb = error_detail.exc_info()  
    #Tipo de la excepción (primer valor): El tipo de la excepción que ocurrió, como TypeError, ValueError, etc.
    #Valor de la excepción (segundo valor): La instancia de la excepción, es decir, el objeto real de la excepción que contiene el mensaje y otros detalles.
    #Traceback (tercer valor): El objeto traceback, que contiene información detallada sobre dónde ocurrió la excepción en el código, incluyendo el archivo, la línea, y la función.
    file_name = exc_tb.tb_frame.f_code.co_filename  # Obtiene el nombre del archivo donde ocurrió el error.
    # Construye un mensaje de error con el nombre del archivo, el número de línea y el mensaje del error.
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message[{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )

    return error_message  # Devuelve el mensaje de error detallado.


# Esta clase personalizada de excepción permite generar mensajes de error más detallados usando la función anterior.
class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)  # Llama al constructor de la clase base Exception con el mensaje de error. Se hace un inheritance de la clase 
        # Guarda el mensaje de error detallado usando la función 'error_message_detail'.
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    # Sobrescribe el método __str__ para devolver el mensaje de error detallado cuando se intente convertir la excepción a una cadena.
    def __str__(self):
        return self.error_message

    