@echo off
REM Text Anonymisierer Starter
echo.
echo ================================
echo Text Anonymisierer wird gestartet...
echo ================================
echo.

REM Aktiviere virtuelle Umgebung falls vorhanden
if exist venv\Scripts\activate.bat (
    echo Aktiviere virtuelle Umgebung...
    call venv\Scripts\activate.bat
)

REM Starte Programm
echo Starte Anonymisierer...
echo.
python main.py

REM Falls Fehler auftreten, Fenster offen lassen
if errorlevel 1 (
    echo.
    echo ================================
    echo FEHLER beim Starten!
    echo ================================
    echo.
    pause
)
