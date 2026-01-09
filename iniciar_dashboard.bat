@echo off
title Lanzador de Dashboard Quintiles
setlocal
cd /d "%~dp0"

:: --- CONFIGURACIÓN ---
set PUERTO=8501
set ANACONDA_PATH=C:\ProgramData\anaconda3
set URL=http://localhost:%PUERTO%

:: 1. VERIFICAR SI YA ESTÁ ABIERTO (Regla de no hacer nada si ya existe)
netstat -ano | findstr :%PUERTO% | findstr LISTENING >nul
if %ERRORLEVEL% equ 0 (
    start %URL%
    exit
)

:: 2. ACTIVAR ENTORNO
if exist %ANACONDA_PATH%\Scripts\activate.bat (
    call %ANACONDA_PATH%\Scripts\activate.bat %ANACONDA_PATH%
)

:: 3. LANZAR STREAMLIT
:: --theme.base light: Fuerza el modo claro
:: --server.address localhost: Oculta la External URL y errores de red
:: --browser.gatherUsageStats false: Elimina telemetría innecesaria
start %URL%

python -m streamlit run dashboard.py --server.port %PUERTO% --server.address localhost --server.headless true --theme.base light --browser.gatherUsageStats false

if %ERRORLEVEL% NEQ 0 (
    streamlit run dashboard.py --server.port %PUERTO% --server.address localhost --theme.base light
)

pause