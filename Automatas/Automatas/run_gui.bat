@echo off
chcp 65001 >nul
cd /d "%~dp0src"
title BeBot - Interfaz Gráfica
echo Iniciando BeBot GUI...
python chatbot_gui.py
if errorlevel 1 (
    echo.
    echo Hubo un error al iniciar la interfaz gráfica.
    echo Prueba ejecutando run_console.bat en su lugar.
    pause
)
