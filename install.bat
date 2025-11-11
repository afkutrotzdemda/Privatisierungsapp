@echo off
SETLOCAL EnableDelayedExpansion
TITLE Anonymify - Installation

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
echo     ANONYMIFY - INSTALLATION
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
        echo.
        echo ====================================================================
        echo [FEHLER] Konnte virtuelle Umgebung nicht erstellen!
        echo ====================================================================
        echo.
        echo HAEUFIGE URSACHEN:
        echo   - Python vom Windows Store installiert
        echo   - pip fehlt in Python-Installation
        echo   - Alte Python-Version
        echo   - Berechtigungsprobleme
        echo.
        echo LOESUNG 1 - Python neu installieren ^(EMPFOHLEN^):
        echo   1. Python deinstallieren ^(Windows Einstellungen -^> Apps^)
        echo   2. Von python.org neu installieren: https://www.python.org/downloads/
        echo   3. Version 3.10 oder 3.11 waehlen ^(NICHT Windows Store!^)
        echo   4. Bei Installation "Add Python to PATH" anhaken
        echo   5. install.bat erneut ausfuehren
        echo.
        echo LOESUNG 2 - Ohne virtuelle Umgebung installieren:
        echo   1. Schliesse dieses Fenster
        echo   2. Fuehre install_global.bat aus
        echo   3. Dependencies werden global installiert
        echo.
        echo LOESUNG 3 - pip manuell installieren:
        echo   curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        echo   python get-pip.py
        echo   Dann install.bat erneut ausfuehren
        echo.
        echo ====================================================================
        echo.
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
echo.
echo WICHTIG: Der globale Hotkey braucht Administrator-Rechte!
echo.
echo OPTION 1: Startup-Ordner (OHNE Admin-Rechte)
echo     + Einfach einzurichten
echo     - Hotkey funktioniert evtl. NICHT ohne Admin
echo.
echo OPTION 2: Task Scheduler (MIT Admin-Rechten)
echo     + Hotkey funktioniert zuverlaessig
echo     - Benoetigt Admin-Rechte bei der Einrichtung
echo     - Fuer Fortgeschrittene Benutzer
echo.
echo OPTION 3: Manuell starten
echo     - Keine Auto-Start, einfach 'start.bat' ausfuehren
echo.

set /p AUTOSTART_CHOICE="Waehle Option (1/2/3): "

if "%AUTOSTART_CHOICE%"=="1" (
    echo.
    echo     - Richte Auto-Start via Startup-Ordner ein...

    REM Erstelle Verknuepfung im Autostart-Ordner
    set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
    set SCRIPT_PATH=%CD%\start.bat

    REM Verwende PowerShell um Verknuepfung zu erstellen
    powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('!STARTUP_FOLDER!\Anonymify.lnk'); $Shortcut.TargetPath = '!SCRIPT_PATH!'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.WindowStyle = 7; $Shortcut.Save()"

    if errorlevel 1 (
        echo [WARNUNG] Konnte Auto-Start nicht einrichten
        echo            Bitte manuell eine Verknuepfung erstellen
    ) else (
        echo [OK] Auto-Start eingerichtet (Startup-Ordner)!
        echo.
        echo WICHTIG: Die App laeuft OHNE Admin-Rechte!
        echo          Rechtsklick auf start.bat -^> "Als Administrator ausfuehren"
        echo          um den Hotkey zum Laufen zu bringen.
    )
) else if "%AUTOSTART_CHOICE%"=="2" (
    echo.
    echo     - Starte setup_admin_autostart.bat fuer Task Scheduler...
    echo.
    echo WICHTIG: Du musst setup_admin_autostart.bat ALS ADMINISTRATOR ausfuehren!
    echo          Rechtsklick -^> "Als Administrator ausfuehren"
    echo.
    call setup_admin_autostart.bat
) else (
    echo [INFO] Auto-Start uebersprungen
    echo       Du kannst die App manuell mit 'start.bat' starten
    echo       TIPP: Rechtsklick -^> "Als Administrator ausfuehren"
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
echo     1. Starte die App: Rechtsklick start.bat -^> "Als Administrator"
echo     2. Das "A"-Icon erscheint in der Taskleiste
echo     3. Markiere Text in beliebiger App
echo     4. Druecke Strg+Alt+A (automatisch kopiert + anonymisiert!)
echo     5. Fuege anonymisierten Text ein (Strg+V)
echo.
echo ICON-FARBEN:
echo     GRUEN  = Bereit
echo     GELB   = Anonymisiert gerade...
echo     ROT    = Fehler
echo.
echo KONFIGURATION:
echo     - Hotkey aendern: config.toml bearbeiten
echo     - Whitelist: Namen in config.toml hinzufuegen
echo.
echo TIPPS:
echo     - Die App laeuft im Hintergrund
echo     - Klick auf Icon zeigt aktuellen Hotkey
echo     - Zum Beenden: Rechtsklick Icon -^> Beenden
echo.
echo ====================================================================
echo.

set /p START_NOW="App jetzt starten? (j/n): "

if /i "%START_NOW%"=="j" (
    echo.
    echo Starte Anonymify...
    echo.
    REM Starte in neuem Fenster
    start "Anonymify" /MIN cmd /c "cd /d %CD% && call start.bat"
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
