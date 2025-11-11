@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

cls
echo.
echo ================================================================
echo                    ANONYMIFY - AUTO UPDATE
echo ================================================================
echo.

:: Prüfe ob Git installiert ist
git --version >nul 2>&1
if errorlevel 1 (
    echo [FEHLER] Git ist nicht installiert!
    echo.
    echo Bitte installiere Git von: https://git-scm.com/download/win
    pause
    exit /b 1
)

:: Prüfe aktuellen Branch
for /f "tokens=*" %%i in ('git branch --show-current') do set CURRENT_BRANCH=%%i
echo Aktueller Branch: %CURRENT_BRANCH%
echo.

:: Zeige aktuelle Version
echo Aktuelle Version:
git log -1 --oneline
echo.

:: Prüfe auf uncommitted changes
git diff-index --quiet HEAD --
if errorlevel 1 (
    echo [WARNUNG] Du hast lokale Aenderungen die nicht committed sind!
    echo.
    git status --short
    echo.
    choice /c JN /m "Moechtest du trotzdem updaten? (Aenderungen gehen verloren)"
    if errorlevel 2 (
        echo Update abgebrochen!
        pause
        exit /b 0
    )
    echo.
    echo [*] Setze lokale Aenderungen zurueck...
    git reset --hard HEAD
)

:: Fetch updates von GitHub
echo [*] Pruefe auf Updates von GitHub...
git fetch origin %CURRENT_BRANCH% 2>nul
if errorlevel 1 (
    echo.
    echo [FEHLER] Konnte nicht mit GitHub verbinden!
    echo Moegliche Ursachen:
    echo - Keine Internetverbindung
    echo - GitHub ist nicht erreichbar
    echo - Repository wurde geloescht
    echo.
    pause
    exit /b 1
)

:: Prüfe ob Updates verfügbar sind
git rev-list HEAD...origin/%CURRENT_BRANCH% --count > update_count.tmp
set /p UPDATE_COUNT=<update_count.tmp
del update_count.tmp

if "%UPDATE_COUNT%"=="0" (
    echo.
    echo [OK] Du hast bereits die neueste Version!
    echo Keine Updates verfuegbar.
    echo.
    pause
    exit /b 0
)

:: Zeige was sich geändert hat
echo.
echo ----------------------------------------------------------------
echo %UPDATE_COUNT% neue(s) Update(s) verfuegbar!
echo ----------------------------------------------------------------
echo.
echo Aenderungen:
git log HEAD..origin/%CURRENT_BRANCH% --oneline --decorate --color=never
echo.
echo ----------------------------------------------------------------
echo.

choice /c JN /m "Moechtest du jetzt updaten"
if errorlevel 2 (
    echo.
    echo Update abgebrochen!
    pause
    exit /b 0
)

echo.
echo [*] Lade Updates herunter...

:: Mache git pull
git pull origin %CURRENT_BRANCH%
if errorlevel 1 (
    echo.
    echo [FEHLER] Update fehlgeschlagen!
    echo.
    echo Versuche manuelle Loesung:
    echo   git reset --hard origin/%CURRENT_BRANCH%
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Update erfolgreich!
echo.

:: Zeige neue Version
echo Neue Version:
git log -1 --oneline
echo.

:: Prüfe ob requirements.txt sich geändert hat
git diff HEAD@{1} HEAD --name-only | findstr "requirements.txt" >nul
if not errorlevel 1 (
    echo [!] requirements.txt wurde aktualisiert!
    echo [*] Aktualisiere Python-Pakete...
    echo.

    if exist venv\Scripts\activate.bat (
        call venv\Scripts\activate.bat
    )

    pip install -r requirements.txt --upgrade
    if errorlevel 1 (
        echo.
        echo [WARNUNG] Einige Pakete konnten nicht aktualisiert werden!
        echo Die App funktioniert moeglicherweise trotzdem.
        echo.
    ) else (
        echo.
        echo [OK] Pakete erfolgreich aktualisiert!
        echo.
    )
)

:: Prüfe ob config.toml sich geändert hat
git diff HEAD@{1} HEAD --name-only | findstr "config.toml" >nul
if not errorlevel 1 (
    echo.
    echo [WARNUNG] config.toml wurde aktualisiert!
    echo Deine lokalen Einstellungen wurden moeglicherweise ueberschrieben.
    echo Bitte pruefe deine Einstellungen in config.toml
    echo.
)

echo ----------------------------------------------------------------
echo.

choice /c JN /m "Moechtest du die App jetzt neu starten"
if errorlevel 2 (
    echo.
    echo Fertig! Starte die App manuell mit start.bat
    echo.
    pause
    exit /b 0
)

echo.
echo [*] Starte App neu...
start "" start.bat
exit /b 0
