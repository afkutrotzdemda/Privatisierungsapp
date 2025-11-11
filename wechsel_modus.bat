@echo off
:: ==================================================================
:: ANONYMIFY - MODUS WECHSELN
:: ==================================================================
:: Wechselt zwischen Fast, Balanced und Accurate Modus
:: ==================================================================

chcp 65001 >nul
color 0A
cd /d "%~dp0"

echo.
echo ================================================================
echo                    ANONYMIFY - MODUS WECHSELN
echo ================================================================
echo.
echo Aktueller Modus:
echo.

:: Zeige aktuellen Modus
if exist config.toml (
    findstr "recognition_mode" config.toml
) else (
    echo FEHLER: config.toml nicht gefunden!
    timeout /t 3
    exit /b 1
)

echo.
echo ----------------------------------------------------------------
echo VERFÜGBARE MODI:
echo ----------------------------------------------------------------
echo.
echo [1] FAST - Schnell (~0.1s)
echo     - Nur Pattern-Matching (kein Machine Learning)
echo     - Perfekt für Echtzeit-Nutzung
echo     - Empfohlen für die meisten Nutzer
echo.
echo [2] BALANCED - Ausgewogen (~1s)
echo     - Pattern + Machine Learning (spaCy klein)
echo     - Bessere Erkennung von Namen ohne Titel
echo     - Benoetigt: pip install spacy + Modell
echo.
echo [3] ACCURATE - Maximal (~2-5s)
echo     - Pattern + grosses ML-Modell
echo     - Beste Genauigkeit
echo     - Benoetigt: grosses spaCy-Modell
echo.
echo ----------------------------------------------------------------

set /p CHOICE="Wähle Modus (1/2/3) oder [Q] für Abbrechen: "

if /i "%CHOICE%"=="q" (
    echo.
    echo Abgebrochen!
    timeout /t 2 >nul
    exit /b 0
)

if "%CHOICE%"=="1" (
    echo.
    echo [*] Wechsle zu FAST Modus...
    powershell -ExecutionPolicy Bypass -Command "(Get-Content config.toml) -replace 'recognition_mode = \\\".*\\\"', 'recognition_mode = \\\"fast\\\"' | Set-Content config.toml"
    if errorlevel 1 (
        echo FEHLER: Konnte config.toml nicht aktualisieren!
        timeout /t 3
        exit /b 1
    )
    echo [OK] Modus auf FAST gesetzt!
    echo.
    echo HINWEIS: Die App muss neu gestartet werden!
    goto :end
)

if "%CHOICE%"=="2" (
    echo.
    echo [*] Wechsle zu BALANCED Modus...

    :: Prüfe ob spaCy installiert ist
    python -c "import spacy" 2>nul
    if errorlevel 1 (
        echo.
        echo [!] spaCy ist nicht installiert!
        echo [*] Installiere spaCy und deutsches Modell...
        echo.

        if exist venv\Scripts\activate.bat (
            call venv\Scripts\activate.bat
        )

        pip install spacy -q
        if errorlevel 1 (
            echo [FEHLER] Konnte spaCy nicht installieren!
            timeout /t 5
            exit /b 1
        )

        python -m spacy download de_core_news_sm
        if errorlevel 1 (
            echo [FEHLER] Konnte Modell nicht downloaden!
            timeout /t 5
            exit /b 1
        )

        echo [OK] spaCy und Modell erfolgreich installiert!
    )

    powershell -ExecutionPolicy Bypass -Command "(Get-Content config.toml) -replace 'recognition_mode = \\\".*\\\"', 'recognition_mode = \\\"balanced\\\"' | Set-Content config.toml"
    if errorlevel 1 (
        echo FEHLER: Konnte config.toml nicht aktualisieren!
        timeout /t 3
        exit /b 1
    )
    echo [OK] Modus auf BALANCED gesetzt!
    echo.
    echo HINWEIS: Die App muss neu gestartet werden!
    goto :end
)

if "%CHOICE%"=="3" (
    echo.
    echo [*] Wechsle zu ACCURATE Modus...

    :: Prüfe ob spaCy installiert ist
    python -c "import spacy" 2>nul
    if errorlevel 1 (
        echo.
        echo [!] spaCy ist nicht installiert!
        echo [*] Installiere spaCy...
        echo.

        if exist venv\Scripts\activate.bat (
            call venv\Scripts\activate.bat
        )

        pip install spacy -q
    )

    :: Prüfe ob großes Modell installiert ist
    python -c "import spacy; spacy.load('de_core_news_lg')" 2>nul
    if errorlevel 1 (
        echo.
        echo [!] Großes spaCy-Modell nicht gefunden!
        echo [*] Lade großes Modell (ca. 100 MB)...
        echo.

        python -m spacy download de_core_news_lg
        if errorlevel 1 (
            echo [FEHLER] Konnte Modell nicht downloaden!
            echo.
            echo HINWEIS: Wechsle auf BALANCED Modus (nutzt kleines Modell)
            powershell -ExecutionPolicy Bypass -Command "(Get-Content config.toml) -replace 'recognition_mode = \\\".*\\\"', 'recognition_mode = \\\"balanced\\\"' | Set-Content config.toml"
            timeout /t 5
            exit /b 1
        )

        echo [OK] Modell erfolgreich installiert!
    )

    powershell -ExecutionPolicy Bypass -Command "(Get-Content config.toml) -replace 'recognition_mode = \\\".*\\\"', 'recognition_mode = \\\"accurate\\\"' | Set-Content config.toml"
    if errorlevel 1 (
        echo FEHLER: Konnte config.toml nicht aktualisieren!
        timeout /t 3
        exit /b 1
    )
    echo [OK] Modus auf ACCURATE gesetzt!
    echo.
    echo HINWEIS: Die App muss neu gestartet werden!
    goto :end
)

echo.
echo [FEHLER] Ungueltige Auswahl!
timeout /t 2
exit /b 1

:end
echo.
echo ----------------------------------------------------------------
echo.
echo Möchtest du die App jetzt neu starten? [J/N]
set /p RESTART="Eingabe: "

if /i "%RESTART%"=="j" (
    echo.
    echo [*] Starte App neu...
    start "" start.bat
    exit
)

echo.
echo Fertig! Starte die App manuell neu mit start.bat
echo.
timeout /t 3
