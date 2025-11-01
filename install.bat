@echo off
SETLOCAL EnableDelayedExpansion
TITLE Text Anonymisierer - Installation

REM ============================================================================
REM AUTOMATISCHES INSTALLATIONS-SCRIPT
REM ============================================================================
REM
REM Dieses Script:
REM - Überprüft Python-Installation
REM - Installiert alle Dependencies (inkl. Presidio)
REM - Richtet optional Auto-Start ein
REM - Startet die Anwendung
REM
REM ============================================================================

echo.
echo ====================================================================
echo     TEXT ANONYMISIERER - INSTALLATION
echo ====================================================================
echo.
echo     Automatische Installation fuer Windows
echo     (c) 2024 - DSGVO-konforme Text-Anonymisierung
echo.
echo ====================================================================
echo.

REM ============================================================================
REM SCHRITT 1: PYTHON PRUEFEN
REM ============================================================================

echo [1/5] Pruefe Python-Installation...
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
REM SCHRITT 2: VIRTUELLE UMGEBUNG ERSTELLEN
REM ============================================================================

echo [2/5] Erstelle virtuelle Umgebung...
echo.

if exist venv (
    echo [INFO] Virtuelle Umgebung existiert bereits
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [FEHLER] Konnte virtuelle Umgebung nicht erstellen!
        pause
        exit /b 1
    )
    echo [OK] Virtuelle Umgebung erstellt
)
echo.

REM ============================================================================
REM SCHRITT 3: DEPENDENCIES INSTALLIEREN
REM ============================================================================

echo [3/5] Installiere Dependencies...
echo     (Dies kann einige Minuten dauern...)
echo.

REM Aktiviere virtuelle Umgebung
call venv\Scripts\activate.bat

REM Upgrade pip
echo     - Aktualisiere pip...
python -m pip install --upgrade pip -q

REM Installiere Standard-Dependencies
echo     - Installiere pyperclip (Zwischenablage)...
pip install pyperclip -q

echo     - Installiere keyboard (Hotkey)...
pip install keyboard -q

echo     - Installiere pystray (System Tray Icon)...
pip install pystray -q

echo     - Installiere Pillow (Bilder)...
pip install Pillow -q

REM Installiere Presidio (Microsoft PII-Erkennung)
echo     - Installiere Presidio Analyzer...
pip install presidio-analyzer -q

echo     - Installiere Presidio Anonymizer...
pip install presidio-anonymizer -q

echo.
echo [OK] Alle Dependencies installiert!
echo.

REM ============================================================================
REM SCHRITT 4: AUTO-START EINRICHTEN (OPTIONAL)
REM ============================================================================

echo [4/5] Auto-Start einrichten...
echo.
echo Soll die App automatisch mit Windows starten?
echo     (Empfohlen fuer die beste Benutzererfahrung)
echo.

set /p AUTOSTART="Auto-Start aktivieren? (j/n): "

if /i "%AUTOSTART%"=="j" (
    echo.
    echo     - Richte Auto-Start ein...

    REM Erstelle Verknuepfung im Autostart-Ordner
    set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
    set SCRIPT_PATH=%CD%\start.bat

    REM Verwende PowerShell um Verknuepfung zu erstellen
    powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('!STARTUP_FOLDER!\Text Anonymisierer.lnk'); $Shortcut.TargetPath = '!SCRIPT_PATH!'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.WindowStyle = 7; $Shortcut.Save()"

    if errorlevel 1 (
        echo [WARNUNG] Konnte Auto-Start nicht einrichten
        echo            Bitte manuell eine Verknuepfung erstellen
    ) else (
        echo [OK] Auto-Start eingerichtet!
        echo      Die App startet jetzt automatisch mit Windows.
    )
) else (
    echo [INFO] Auto-Start uebersprungen
    echo       Du kannst die App manuell mit 'start.bat' starten
)
echo.

REM ============================================================================
REM SCHRITT 5: ABSCHLUSS
REM ============================================================================

echo [5/5] Installation abgeschlossen!
echo.
echo ====================================================================
echo     INSTALLATION ERFOLGREICH!
echo ====================================================================
echo.
echo Die App ist jetzt installiert und einsatzbereit.
echo.
echo VERWENDUNG:
echo     1. Starte die App mit: start.bat
echo     2. Das "A"-Icon erscheint in der Taskleiste
echo     3. Kopiere Text (Strg+C)
echo     4. Druecke Strg+Alt+A zum Anonymisieren
echo     5. Fuege anonymisierten Text ein (Strg+V)
echo.
echo ICON-FARBEN:
echo     GRUEN  = Bereit
echo     GELB   = Anonymisiert gerade...
echo     ROT    = Fehler (3 Sek, dann zurueck zu Gruen)
echo.
echo TIPPS:
echo     - Die App laeuft im Hintergrund
echo     - Klick auf das Icon zeigt das Menue
echo     - Zum Beenden: Rechtsklick Icon -^> Beenden
echo.
echo ====================================================================
echo.

set /p START_NOW="App jetzt starten? (j/n): "

if /i "%START_NOW%"=="j" (
    echo.
    echo Starte Text Anonymisierer...
    echo.
    REM Starte in neuem Fenster
    start "Text Anonymisierer" /MIN cmd /c "cd /d %CD% && call start.bat"
    echo.
    echo [OK] App gestartet!
    echo      Schaue in die Taskleiste fuer das Icon.
    echo.
) else (
    echo.
    echo Starte die App spaeter mit: start.bat
    echo.
)

echo Druecke eine Taste zum Beenden...
pause >nul

ENDLOCAL
