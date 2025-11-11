@echo off
SETLOCAL EnableDelayedExpansion
TITLE Anonymify - Admin Auto-Start Setup (Task Scheduler)

REM ============================================================================
REM ADMIN AUTO-START SETUP
REM ============================================================================
REM
REM Dieses Script richtet Auto-Start via Windows Task Scheduler ein.
REM VORTEIL: Die App läuft mit Admin-Rechten → Hotkey funktioniert!
REM
REM WICHTIG: Dieses Script MUSS als Administrator ausgeführt werden!
REM          Rechtsklick → "Als Administrator ausführen"
REM
REM ============================================================================

echo.
echo ====================================================================
echo     ANONYMIFY - ADMIN AUTO-START SETUP
echo ====================================================================
echo.
echo Dieses Script richtet Auto-Start via Task Scheduler ein.
echo Die App startet dann automatisch MIT Admin-Rechten.
echo.
echo WICHTIG: Du musst dieses Script ALS ADMINISTRATOR ausfuehren!
echo.
echo ====================================================================
echo.

REM ============================================================================
REM SCHRITT 1: ADMIN-RECHTE PRUEFEN
REM ============================================================================

echo [1/3] Pruefe Admin-Rechte...
echo.

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [FEHLER] Dieses Script braucht Administrator-Rechte!
    echo.
    echo LOESUNG:
    echo     1. Beende dieses Fenster
    echo     2. Rechtsklick auf setup_admin_autostart.bat
    echo     3. Waehle "Als Administrator ausfuehren"
    echo.
    pause
    exit /b 1
)

echo [OK] Script laeuft als Administrator
echo.

REM ============================================================================
REM SCHRITT 2: TASK ERSTELLEN
REM ============================================================================

echo [2/3] Erstelle Task Scheduler Eintrag...
echo.

REM Aktuelles Verzeichnis
set APP_DIR=%CD%
set SCRIPT_PATH=%APP_DIR%\start.bat

echo     - Task Name: Anonymify_Autostart
echo     - Script: %SCRIPT_PATH%
echo     - Trigger: Bei Anmeldung (mit Admin-Rechten)
echo.

REM Erstelle Task via schtasks
schtasks /create /tn "Anonymify_Autostart" /tr "\"%SCRIPT_PATH%\"" /sc onlogon /rl highest /f >nul 2>&1

if errorlevel 1 (
    echo [FEHLER] Konnte Task nicht erstellen!
    echo.
    echo Moeliche Gruende:
    echo     - Keine Admin-Rechte
    echo     - Task Scheduler Dienst laeuft nicht
    echo.
    pause
    exit /b 1
)

echo [OK] Task erfolgreich erstellt!
echo.

REM ============================================================================
REM SCHRITT 3: BESTAETIGUNG
REM ============================================================================

echo [3/3] Setup abgeschlossen!
echo.
echo ====================================================================
echo     AUTO-START AKTIVIERT!
echo ====================================================================
echo.
echo Die App startet jetzt automatisch beim Anmelden.
echo.
echo DETAILS:
echo     - Task Name: Anonymify_Autostart
echo     - Rechte: Administrator (Hotkey funktioniert!)
echo     - Trigger: Bei jedem Login
echo.
echo TASK VERWALTEN:
echo     - Anzeigen: taskschd.msc (Task Scheduler oeffnen)
echo     - Loeschen: schtasks /delete /tn "Anonymify_Autostart" /f
echo.
echo NAECHSTE SCHRITTE:
echo     - Teste die App mit: start.bat (Rechtsklick -^> Als Admin)
echo     - Oder: Melde dich ab und wieder an (Auto-Start)
echo.
echo ====================================================================
echo.

pause

ENDLOCAL
