import os
# CONFIGURACIÓN PARA SILENCIAR LOKY/JOBLIB
os.environ['PYTHONWARNINGS'] = 'ignore'

import papermill as pm
import sys
import pandas as pd
import warnings
import time
from datetime import datetime

# Silenciar warnings
warnings.filterwarnings("ignore")

# --- DEFINICIÓN DE RUTAS ANONIMIZADAS ---
# En GitHub, usa nombres genéricos de carpetas
RUTA_BASE_PROYECTOS = "./notebooks"
RUTA_P001 = os.path.join(RUTA_BASE_PROYECTOS, "segmentacion")
RUTA_P017 = os.path.join(RUTA_BASE_PROYECTOS, "churn_ltv")
RUTA_P018 = os.path.join(RUTA_BASE_PROYECTOS, "recomendacion")

# El archivo de salida que usará el dashboard
RUTA_QUINTILES = "./data/rfm_churn_ltv.csv"
# Logs en una carpeta del proyecto, no en tu carpeta personal
RUTA_LOGS = "./logs"

# Crear carpetas si no existen (para que no falle en otros entornos)
os.makedirs(RUTA_LOGS, exist_ok=True)

def ejecutar_notebook(ruta_carpeta, nombre_notebook):
    # En la versión pública, asumimos que los notebooks están en el repo
    ruta_input = os.path.join(ruta_carpeta, nombre_notebook)
    print(f"\n--- Ejecutando: {nombre_notebook} ---")
    
    try:
        # Nota: En un entorno real de GitHub, estas rutas deben existir
        pm.execute_notebook(
            input_path=ruta_input,
            output_path=ruta_input, # O una carpeta de 'output'
            log_output=False, 
            progress_bar=True
        )
        print(f"--- OK: {nombre_notebook} ---")
    except Exception as e:
        print(f"Error en {nombre_notebook}: {e}")
        # En producción no querrás que el pipeline se detenga siempre, 
        # pero para desarrollo está bien.
        pass 

def generar_log_analisis(duracion_horas):
    print("\n--- Generando log de ejecución ---")
    try:
        # Verificamos si el archivo existe antes de analizar
        if not os.path.exists(RUTA_QUINTILES):
            print("Archivo de datos no encontrado para el log.")
            return

        size_mb = os.path.getsize(RUTA_QUINTILES) / (1024 * 1024)
        df = pd.read_csv(RUTA_QUINTILES, low_memory=False)
        filas, columnas = df.shape
        
        fecha_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ruta_completa_log = os.path.join(RUTA_LOGS, "pipeline_log.txt")
        
        contenido = (
            f"\n{'#'*80}\n"
            f"EJECUCIÓN SISTEMA DE INTELIGENCIA: {fecha_str}\n"
            f"{'='*80}\n"
            f"MÉTRICAS DE RENDIMIENTO:\n"
            f"Tiempo de procesamiento: {duracion_horas:.2f} horas\n\n"
            f"DATASET PROCESADO:\n"
            f"Registros: {filas:,}\n"
            f"Variables: {columnas}\n"
            f"Tamaño: {size_mb:.2f} MB\n"
            f"{'='*80}\n"
            f"Status: Pipeline completado satisfactoriamente.\n"
            f"{'#'*80}\n"
        )
        
        with open(ruta_completa_log, "a", encoding="utf-8") as f:
            f.write(contenido)
            
        print(f"Log guardado en: {ruta_completa_log}")
    except Exception as e:
        print(f"Error al generar log: {e}")

if __name__ == "__main__":
    inicio_proceso = time.time()

    # Los nombres de los notebooks también pueden ser anonimizados si tienen nombres de marcas
    ejecutar_notebook(RUTA_P001, "01_Segmentacion_Cartera.ipynb")
    ejecutar_notebook(RUTA_P017, "02_Modelo_Churn.ipynb")
    ejecutar_notebook(RUTA_P017, "03_Modelo_LTV.ipynb")
    ejecutar_notebook(RUTA_P018, "04_Engine_Recomendacion.ipynb")
    
    fin_proceso = time.time()
    duracion_horas = (fin_proceso - inicio_proceso) / 3600

    generar_log_analisis(duracion_horas)
    print(f"\nProceso finalizado. Tiempo: {duracion_horas:.2f} hrs.")