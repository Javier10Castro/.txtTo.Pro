@echo off
title Convertir canciones TXT a ProPresenter PRO

python "%~dp0convertir_txt_a_pro.py"

if errorlevel 1 (
    echo.
    echo Ocurrio un error.
)

pause
