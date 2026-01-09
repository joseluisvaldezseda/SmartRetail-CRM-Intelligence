@echo off
title Ejecutando Pipeline de Inteligencia de Clientes
echo Iniciando proceso... Por favor no cierres esta ventana.
echo.

"C:\Users\jose.valdez\airflow\airflow_env\Scripts\python.exe" "\\compartido.lamarina.mx\Inteligencia de Clientes\ICCM\Proyectos de Inteligencia\P001.- VFR\run_pipeline.py"

echo.
echo ----------------------------------------------------------
echo Proceso terminado.
echo Puedes revisar el log en tu carpeta de Descargas.
echo ----------------------------------------------------------
pause