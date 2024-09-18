import logging  # Importa el módulo 'logging', que es la biblioteca estándar en Python para registrar eventos e información durante la ejecución de un programa.
import os  # Importa la biblioteca 'os', que permite interactuar con el sistema operativo para trabajar con archivos, rutas, etc.
from datetime import datetime  # Importa la clase 'datetime' para manejar fechas y horas.

# Crea un nombre de archivo de log basado en la fecha y la hora actual. El formato será: mes_día_año_hora_minuto_segundo.log
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Define la ruta donde se guardará el archivo de log. 
# Combina el directorio de trabajo actual, una carpeta llamada 'logs', y el nombre del archivo de log generado.
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)

# Crea la carpeta 'logs' si no existe, para evitar errores al crearla.
os.makedirs(logs_path, exist_ok=True)

# Define la ruta completa donde se guardará el archivo de log.
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Configura el sistema de logging con las siguientes opciones:
logging.basicConfig(
    filename=LOG_FILE_PATH,  # Especifica el archivo donde se guardarán los logs.
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",  # Define el formato del mensaje de log.
    level=logging.INFO,  # Establece el nivel de severidad mínimo de los mensajes a registrar (en este caso, INFO).
)

# Formato de mensaje:
# %(asctime)s -> Incluye la fecha y la hora en que se registra el mensaje.
# %(lineno)d -> Incluye el número de línea donde ocurrió el evento.
# %(name)s -> Incluye el nombre del logger que generó el evento.
# %(levelname)s -> Incluye el nivel de severidad del mensaje (INFO, WARNING, ERROR, etc.).
# %(message)s -> El mensaje principal que se registrará.

# Nivel de severidad:
# level=logging.INFO indica que solo se registrarán mensajes de nivel INFO o superior (INFO, WARNING, ERROR, CRITICAL).

if __name__ =="__main__":
    logging.info("Logging has started")