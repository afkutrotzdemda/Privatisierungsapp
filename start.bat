@echo off
SETLOCAL
REM Anonymify Starter
echo.
echo ====================================================================
echo     ANONYMIFY - STARTER
echo ====================================================================
echo.

REM ============================================================================
REM SCHRITT 1: PRUEFE OB INSTALLATION AUSGEFUEHRT WURDE
REM ============================================================================

if not exist venv\Scripts\activate.bat (
    echo [FEHLER] Virtuelle Umgebung nicht gefunden!
    echo.
    echo ====================================================================
    echo     INSTALLATION FEHLT!
    echo ====================================================================
    echo.
    echo Du musst ZUERST install.bat ausfuehren!
    echo.
    echo LOESUNG:
    echo     1. Schliesse dieses Fenster
    echo     2. Doppelklick auf install.bat
    echo     3. Warte bis Installation abgeschlossen
    echo     4. Dann erneut start.bat ausfuehren
    echo.
    echo ODER falls install.bat nicht existiert:
    echo     python -m venv venv
    echo     call venv\Scripts\activate.bat
    echo     pip install -r requirements.txt
    echo.
    echo ====================================================================
    echo.
    pause
    exit /b 1
)

REM ============================================================================
REM SCHRITT 2: AKTIVIERE VIRTUELLE UMGEBUNG
REM ============================================================================

echo [1/2] Aktiviere virtuelle Umgebung...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo [FEHLER] Konnte virtuelle Umgebung nicht aktivieren!
    echo.
    echo Fuehre install.bat erneut aus.
    echo.
    pause
    exit /b 1
)
echo [OK] Virtuelle Umgebung aktiv
echo.

REM ============================================================================
REM SCHRITT 3: PRUEFE OB PRESIDIO INSTALLIERT IST
REM ============================================================================

echo [2/2] Pruefe Dependencies...
python -c "import presidio_analyzer" 2>nul

if errorlevel 1 (
    echo [FEHLER] Presidio ist nicht installiert!
    echo.
    echo ====================================================================
    echo     DEPENDENCIES FEHLEN!
    echo ====================================================================
    echo.
    echo LOESUNG:
    echo     1. Schliesse dieses Fenster
    echo     2. Fuehre install.bat erneut aus
    echo.
    echo ODER manuell installieren:
    echo     call venv\Scripts\activate.bat
    echo     pip install -r requirements.txt
    echo.
    echo ====================================================================
    echo.
    pause
    exit /b 1
)
echo [OK] Dependencies vorhanden
echo.

REM ============================================================================
REM SCHRITT 4: STARTE PROGRAMM
REM ============================================================================

echo ====================================================================
echo Starte Anonymify...
echo ====================================================================
echo.
echo WICHTIG: Programm als Administrator starten fuer Hotkey!
echo          Rechtsklick start.bat -^> "Als Administrator ausfuehren"
echo.
echo ====================================================================
echo.

python main.py

REM Falls Fehler auftreten, Fenster offen lassen
if errorlevel 1 (
    echo.
    echo ====================================================================
    echo     FEHLER beim Starten!
    echo ====================================================================
    echo.
    echo MOEGLICHE LOESUNGEN:
    echo     1. Fuehre install.bat erneut aus
    echo     2. Rechtsklick start.bat -^> "Als Administrator ausfuehren"
    echo     3. Pruefe anonymizer.log fuer Details
    echo.
    echo ====================================================================
    echo.
    pause
)

ENDLOCAL
