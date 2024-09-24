import sys  # Importa el módulo 'sys' para trabajar con el sistema, útil para manejar excepciones y rutas.
from dataclasses import dataclass  # Importa 'dataclass' para definir clases con poco código y mejorar la legibilidad.

import numpy as np  # Importa 'numpy', que es útil para manejar arrays numéricos.
import pandas as pd  # Importa 'pandas', que es útil para manipular y analizar datos estructurados (como dataframes).
from sklearn.compose import ColumnTransformer  # Importa 'ColumnTransformer' para aplicar transformaciones diferentes a columnas distintas en un dataframe.
from sklearn.impute import SimpleImputer  # Importa 'SimpleImputer' para manejar valores faltantes en los datos.
from sklearn.pipeline import Pipeline  # Importa 'Pipeline' para encadenar varios pasos de transformación en un proceso.
from sklearn.preprocessing import OneHotEncoder, StandardScaler  # Importa 'OneHotEncoder' para transformar variables categóricas en numéricas y 'StandardScaler' para normalizar datos.

from src.exception import CustomException  # Importa una clase personalizada para manejar excepciones, definida en otro archivo.
from src.logger import logging  # Importa una herramienta de 'logging' para registrar mensajes y errores.
import os  # Importa el módulo 'os' para manejar rutas de archivos y directorios.

from src.utils import save_object  # Importa una función personalizada para guardar objetos, posiblemente serializándolos.

# Crea una configuración para la transformación de datos utilizando 'dataclass', donde se define la ruta del archivo preprocesado.
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"preprocessor.pkl")  # Define la ruta donde se guardará el objeto de preprocesamiento.

# Clase que maneja la transformación de los datos.
class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()  # Inicializa la configuración de transformación de datos.

    # Función que devuelve un objeto transformador para preprocesar los datos.
    def get_data_transformer_object(self):
        '''
        Esta función es responsable de la transformación de los datos.
        '''
        try:
            # Define las columnas numéricas y categóricas del dataframe.
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            # Define una pipeline para las columnas numéricas:
            num_pipeline= Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="median")),  # Rellena valores faltantes con la mediana.
                ("scaler",StandardScaler())  # Normaliza los valores.
                ]
            )

            # Define una pipeline para las columnas categóricas:
            cat_pipeline=Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),  # Rellena valores faltantes con el valor más frecuente.
                ("one_hot_encoder",OneHotEncoder()),  # Convierte variables categóricas en numéricas mediante codificación One-Hot.
                ("scaler",StandardScaler(with_mean=False))  # Normaliza, pero sin centrar en cero (por compatibilidad con One-Hot).
                ]
            )

            # Registra columnas categóricas y numéricas para ayudar en la depuración.
            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            # Combina las pipelines en un transformador por columnas.
            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns),  # Aplica la pipeline numérica a las columnas numéricas.
                ("cat_pipelines",cat_pipeline,categorical_columns)  # Aplica la pipeline categórica a las columnas categóricas.
                ]
            )

            return preprocessor  # Devuelve el preprocesador completo.
        
        except Exception as e:
            raise CustomException(e,sys)  # Si ocurre una excepción, lanza una excepción personalizada.

    # Función para iniciar la transformación de los datos.
    def initiate_data_transformation(self,train_path,test_path):
        try:
            # Lee los datos de entrenamiento y prueba desde los archivos CSV.
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Lectura de los datos de entrenamiento y prueba completada.")

            logging.info("Obteniendo objeto de preprocesamiento.")

            # Obtiene el objeto de preprocesamiento definido anteriormente.
            preprocessing_obj=self.get_data_transformer_object()

            # Define la columna objetivo (lo que se va a predecir).
            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]

            # Separa las características (input) y la columna objetivo (output) en los datos de entrenamiento.
            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            # Separa las características (input) y la columna objetivo (output) en los datos de prueba.
            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info("Aplicando objeto de preprocesamiento en los dataframes de entrenamiento y prueba.")

            # Aplica el preprocesador a los datos de entrenamiento.
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            # Aplica el preprocesador a los datos de prueba.
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            # Combina las características preprocesadas con la columna objetivo en un solo array para el entrenamiento.
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            # Combina las características preprocesadas con la columna objetivo en un solo array para la prueba.
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info("Guardando objeto de preprocesamiento.")

            # Guarda el preprocesador en un archivo .pkl.
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,  # Define la ruta donde se guardará.
                obj=preprocessing_obj  # Objeto a guardar.
            )

            # Devuelve los arrays de entrenamiento, prueba, y la ruta del archivo preprocesador.
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)  # Si ocurre una excepción, lanza una excepción personalizada.
