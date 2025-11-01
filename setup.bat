@echo off
REM Setup-Skript für Text Anonymisierer
echo.
echo ================================
echo Text Anonymisierer - Setup
echo ================================
echo.

REM Prüfe ob Python installiert ist
python --version >nul 2>&1
if errorlevel 1 (
    echo FEHLER: Python ist nicht installiert!
    echo Bitte installiere Python von https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python gefunden:
python --version
echo.

REM Erstelle virtuelle Umgebung
echo Erstelle virtuelle Umgebung...
python -m venv venv
if errorlevel 1 (
    echo FEHLER: Konnte virtuelle Umgebung nicht erstellen!
    pause
    exit /b 1
)
echo OK
echo.

REM Aktiviere virtuelle Umgebung
echo Aktiviere virtuelle Umgebung...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo FEHLER: Konnte virtuelle Umgebung nicht aktivieren!
    pause
    exit /b 1
)
echo OK
echo.

REM Installiere Dependencies
echo Installiere Dependencies...
echo (Dies kann einige Minuten dauern...)
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo FEHLER: Konnte Dependencies nicht installieren!
    pause
    exit /b 1
)
echo.
echo OK
echo.

REM Optional: spaCy Sprachmodell
echo.
echo ================================
echo Moechten Sie das deutsche spaCy-Sprachmodell installieren?
echo (Nur noetig falls Presidio es benoetigt)
echo ================================
set /p INSTALL_SPACY="Installieren? (j/n): "
if /i "%INSTALL_SPACY%"=="j" (
    echo Installiere deutsches Sprachmodell...
    python -m spacy download de_core_news_sm
    echo OK
)
echo.

REM Fertig
echo.
echo ================================
echo Setup abgeschlossen!
echo ================================
echo.
echo Starte jetzt das Programm mit:
echo    start.bat
echo.
echo oder:
echo    venv\Scripts\activate.bat
echo    python main.py
echo.
pause
