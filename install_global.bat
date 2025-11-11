@echo off
SETLOCAL EnableDelayedExpansion
TITLE Anonymify - Installation (GLOBAL, ohne venv)

REM ============================================================================
REM GLOBALE INSTALLATION (OHNE VIRTUELLE UMGEBUNG)
REM ============================================================================
REM
REM Dieses Script installiert Anonymify GLOBAL (nicht in venv)
REM Nutze dies nur wenn install.bat fehlschlägt!
REM
REM WARNUNG: Installiert Packages global auf deinem System
REM
REM ============================================================================

echo.
echo ====================================================================
echo     ANONYMIFY - GLOBALE INSTALLATION
echo ====================================================================
echo.
echo WARNUNG: Dieses Script installiert Packages GLOBAL!
echo          Nutze dies nur wenn install.bat nicht funktioniert.
echo.
echo ====================================================================
echo.

pause

REM ============================================================================
REM SCHRITT 1: PYTHON PRUEFEN
REM ============================================================================

echo [1/4] Pruefe Python-Installation...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [FEHLER] Python ist nicht installiert!
    echo.
    echo Bitte installiere Python von: https://www.python.org/downloads/
    echo.
    echo WICHTIG: Bei der Installation "Add Python to PATH" ankreuzen!
    echo.
    pause
    exit /b 1
)

echo [OK] Python gefunden:
python --version
echo.

REM ============================================================================
REM SCHRITT 2: PIP PRUEFEN UND UPGRADEN
REM ============================================================================

echo [2/4] Pruefe pip...
echo.

python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [FEHLER] pip ist nicht installiert!
    echo.
    echo LOESUNG:
    echo   1. Python neu installieren von python.org
    echo   2. Bei Installation "Install pip" sicherstellen
    echo.
    echo ODER manuell pip installieren:
    echo   curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    echo   python get-pip.py
    echo.
    pause
    exit /b 1
)

echo [OK] pip gefunden
echo.
echo Upgrade pip...
python -m pip install --upgrade pip -q
echo [OK] pip aktualisiert
echo.

REM ============================================================================
REM SCHRITT 3: DEPENDENCIES INSTALLIEREN (GLOBAL)
REM ============================================================================

echo [3/4] Installiere Dependencies (GLOBAL)...
echo     (Dies kann einige Minuten dauern...)
echo.

REM Installiere Standard-Dependencies
echo     - Installiere pyperclip (Zwischenablage)...
pip install pyperclip --user

echo     - Installiere keyboard (Hotkey)...
pip install keyboard --user

echo     - Installiere pystray (System Tray Icon)...
pip install pystray --user

echo     - Installiere Pillow (Bilder)...
pip install Pillow --user

REM Installiere Presidio (Microsoft PII-Erkennung)
echo     - Installiere Presidio Analyzer...
pip install presidio-analyzer --user

echo     - Installiere Presidio Anonymizer...
pip install presidio-anonymizer --user

echo.
echo [OK] Alle Dependencies installiert!
echo.

REM ============================================================================
REM SCHRITT 4: START-SCRIPT ERSTELLEN
REM ============================================================================

echo [4/4] Erstelle Start-Script...
echo.

REM Erstelle start_global.bat
(
echo @echo off
echo REM Anonymify Starter ^(Global Installation^)
echo echo.
echo echo ====================================================================
echo echo     ANONYMIFY - STARTER
echo echo ====================================================================
echo echo.
echo echo WICHTIG: Als Administrator ausfuehren fuer Hotkey!
echo echo.
echo python main.py
echo if errorlevel 1 pause
) > start_global.bat

echo [OK] start_global.bat erstellt
echo.

REM ============================================================================
REM SCHRITT 5: ABSCHLUSS
REM ============================================================================

echo ====================================================================
echo     INSTALLATION ERFOLGREICH!
echo ====================================================================
echo.
echo Die App ist jetzt installiert (GLOBAL, ohne venv).
echo.
echo VERWENDUNG:
echo     1. Rechtsklick auf: start_global.bat
echo     2. Waehle: "Als Administrator ausfuehren"
echo     3. Das "A"-Icon erscheint in der Taskleiste
echo.
echo HINWEIS:
echo     - Dependencies wurden GLOBAL installiert (--user)
echo     - Nutze start_global.bat statt start.bat
echo     - Bei Problemen: Siehe QUICKSTART.md
echo.
echo ====================================================================
echo.

set /p START_NOW="App jetzt starten? (j/n): "

if /i "%START_NOW%"=="j" (
    echo.
    echo Starte Anonymify...
    echo.
    echo HINWEIS: Druecke Strg+C zum Beenden
    echo.
    python main.py
) else (
    echo.
    echo Starte die App spaeter mit:
    echo   Rechtsklick start_global.bat -^> "Als Administrator ausfuehren"
    echo.
)

echo.
pause

ENDLOCAL
