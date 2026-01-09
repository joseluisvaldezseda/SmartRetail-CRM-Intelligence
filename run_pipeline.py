import os

# CONFIGURACIÓN PARA SILENCIAR LOKY/JOBLIB (Debe ir antes de cualquier otro import) 
os.environ['PYTHONWARNINGS'] = 'ignore'

import papermill as pm
import sys
import pandas as pd
import warnings
import time
from datetime import datetime

# Silenciar warnings de Python
warnings.filterwarnings("ignore")

# Definición de rutas
RUTA_P001 = r"\\compartido.lamarina.mx\Inteligencia de Clientes\ICCM\Proyectos de Inteligencia\P001.- VFR"
RUTA_P017 = r"\\compartido.lamarina.mx\Inteligencia de Clientes\ICCM\Proyectos de Inteligencia\P017.- Churn + Lifetime Value"
RUTA_QUINTILES = r"\\compartido.lamarina.mx\Inteligencia de Clientes\Bases de datos\Quintiles.csv"
RUTA_LOGS = r"C:\Users\jose.valdez\Downloads"

def ejecutar_notebook(ruta_carpeta, nombre_notebook):
    ruta_input = os.path.join(ruta_carpeta, nombre_notebook)
    print(f"\n--- Iniciando Papermill con: {nombre_notebook} ---")
    
    try:
        os.chdir(ruta_carpeta)
        pm.execute_notebook(
            input_path=ruta_input,
            output_path=ruta_input,
            log_output=False, 
            progress_bar=True
        )
        print(f"--- Finalizado con éxito: {nombre_notebook} ---")
    except Exception as e:
        print(f"Error ejecutando {nombre_notebook}: {e}")
        sys.exit(1)

def generar_log_analisis(duracion_horas):
    print("\n--- Agregando reporte a log_quintiles.txt ---")
    try:
        size_bytes = os.path.getsize(RUTA_QUINTILES)
        size_mb = size_bytes / (1024 * 1024)
        
        df = pd.read_csv(RUTA_QUINTILES, encoding='latin1', low_memory=False)
        filas, columnas = df.shape
        lista_columnas = df.columns.tolist()
        
        fecha_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ruta_completa_log = os.path.join(RUTA_LOGS, "log_quintiles.txt")
        columnas_str = "\n".join([f"- {col}" for col in lista_columnas])
        
        # He modificado el diseño del contenido para que se vea mejor como historial
        contenido = (
            f"\n{'#'*80}\n"
            f"NUEVA EJECUCIÓN REGISTRADA: {fecha_str}\n"
            f"{'='*80}\n"
            f"RESUMEN DE TIEMPO:\n"
            f"Tiempo total de ejecución: {duracion_horas:.2f} horas\n\n"
            f"ARCHIVO ANALIZADO:\n"
            f"Nombre: Quintiles.csv\n"
            f"Ruta: {RUTA_QUINTILES}\n\n"
            f"PROPIEDADES:\n"
            f"Dimensiones: {filas:,} filas x {columnas} columnas\n"
            f"Tamaño: {size_mb:.2f} MB\n\n"
            f"LISTADO DE COLUMNAS ({columnas}):\n"
            f"{columnas_str}\n"
            f"{'='*80}\n"
            f"Status: Pipeline finalizado con éxito.\n"
            f"{'#'*80}\n"
        )
        
        # "a" (append) añade al final del archivo. Si no existe, lo crea.
        with open(ruta_completa_log, "a", encoding="utf-8") as f:
            f.write(contenido)
            
        print(f"Log actualizado correctamente en: {ruta_completa_log}")
    except Exception as e:
        print(f"Error al analizar el CSV o agregar al log: {e}")

if __name__ == "__main__":
    inicio_proceso = time.time()

    # Ejecución de los 3 notebooks
    #ejecutar_notebook(RUTA_P001, "Calculo de Segmentos LM y EB.ipynb")
    #ejecutar_notebook(RUTA_P017, "Modelo Churn LM y EB.ipynb")
    #ejecutar_notebook(RUTA_P017, "Modelo LTV LM y EB.ipynb")

    fin_proceso = time.time()
    duracion_horas = (fin_proceso - inicio_proceso) / 3600

    generar_log_analisis(duracion_horas)
    print(f"\nProceso total finalizado. Tiempo registrado: {duracion_horas:.2f} horas.")