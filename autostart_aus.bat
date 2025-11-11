@echo off
:: ==================================================================
:: ANONYMIFY - AUTOSTART DEAKTIVIEREN
:: ==================================================================
:: Entfernt Anonymify aus dem Windows-Autostart
:: ==================================================================

chcp 65001 >nul
color 0C

echo.
echo ════════════════════════════════════════════════════════════════
echo              ANONYMIFY - AUTOSTART DEAKTIVIEREN
echo ════════════════════════════════════════════════════════════════
echo.

:: Prüfe Admin-Rechte
net session >nul 2>&1
if errorlevel 1 (
    echo ⚠️  WARNUNG: Admin-Rechte benötigt!
    echo.
    echo Autostart mit Task Scheduler erfordert Admin-Rechte.
    echo.
    echo Rechtsklick auf diese Datei → "Als Administrator ausführen"
    echo.
    pause
    exit /b 1
)

echo [*] Suche nach Autostart-Einträgen...
echo.

:: 1. Task Scheduler (empfohlene Methode)
schtasks /Query /TN "Anonymify" >nul 2>&1
if %errorlevel% equ 0 (
    echo [✓] Anonymify-Task gefunden in Task Scheduler
    echo [*] Lösche Task...

    schtasks /Delete /TN "Anonymify" /F >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Task Scheduler: Autostart deaktiviert!
        set FOUND_TASK=1
    ) else (
        echo ❌ Fehler beim Löschen des Tasks!
    )
) else (
    echo [ℹ] Kein Task Scheduler Eintrag gefunden
)

echo.

:: 2. Registry Autostart (Run)
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "Anonymify" >nul 2>&1
if %errorlevel% equ 0 (
    echo [✓] Anonymify gefunden in Registry (HKCU\Run)
    echo [*] Lösche Registry-Eintrag...

    reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "Anonymify" /f >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Registry: Autostart deaktiviert!
        set FOUND_REG=1
    ) else (
        echo ❌ Fehler beim Löschen des Registry-Eintrags!
    )
) else (
    echo [ℹ] Kein Registry Eintrag gefunden (HKCU)
)

echo.

:: 3. Registry Autostart (Run) - HKLM (für alle Nutzer)
reg query "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v "Anonymify" >nul 2>&1
if %errorlevel% equ 0 (
    echo [✓] Anonymify gefunden in Registry (HKLM\Run)
    echo [*] Lösche Registry-Eintrag...

    reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v "Anonymify" /f >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Registry (HKLM): Autostart deaktiviert!
        set FOUND_REG_HKLM=1
    ) else (
        echo ❌ Fehler beim Löschen des Registry-Eintrags!
    )
) else (
    echo [ℹ] Kein Registry Eintrag gefunden (HKLM)
)

echo.

:: 4. Startup-Ordner
set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
if exist "%STARTUP_FOLDER%\Anonymify.lnk" (
    echo [✓] Anonymify gefunden im Startup-Ordner
    echo [*] Lösche Verknüpfung...

    del "%STARTUP_FOLDER%\Anonymify.lnk" >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Startup-Ordner: Autostart deaktiviert!
        set FOUND_STARTUP=1
    ) else (
        echo ❌ Fehler beim Löschen der Verknüpfung!
    )
) else (
    echo [ℹ] Keine Verknüpfung im Startup-Ordner gefunden
)

echo.
echo ════════════════════════════════════════════════════════════════

if defined FOUND_TASK (
    echo.
    echo ✅ ERFOLG: Autostart wurde deaktiviert!
    echo.
    echo Anonymify startet NICHT mehr automatisch beim Windows-Start.
    echo.
) else if defined FOUND_REG (
    echo.
    echo ✅ ERFOLG: Autostart wurde deaktiviert!
    echo.
) else if defined FOUND_REG_HKLM (
    echo.
    echo ✅ ERFOLG: Autostart wurde deaktiviert!
    echo.
) else if defined FOUND_STARTUP (
    echo.
    echo ✅ ERFOLG: Autostart wurde deaktiviert!
    echo.
) else (
    echo.
    echo ℹ️  Kein Autostart-Eintrag gefunden!
    echo.
    echo Anonymify war NICHT im Autostart konfiguriert.
    echo.
)

echo ────────────────────────────────────────────────────────────────
echo.
echo Möchtest du Anonymify komplett beenden? [J/N]
set /p KILL_APP="Eingabe: "

if /i "%KILL_APP%"=="j" (
    echo.
    echo [*] Beende Anonymify-Prozesse...
    taskkill /F /IM pythonw.exe /FI "WINDOWTITLE eq Anonymify*" >nul 2>&1
    taskkill /F /IM python.exe /FI "WINDOWTITLE eq Anonymify*" >nul 2>&1
    echo ✅ Anonymify beendet!
)

echo.
echo Fertig!
echo.
echo HINWEIS: Du kannst Autostart jederzeit wieder aktivieren mit:
echo          • setup_admin_autostart.bat (empfohlen)
echo          • Option beim install.bat
echo.
timeout /t 5
