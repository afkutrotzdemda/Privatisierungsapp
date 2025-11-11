@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

cls
echo.
echo ================================================================
echo                    ANONYMIFY - MODUS WECHSELN
echo ================================================================
echo.

if not exist config.toml (
    echo FEHLER: config.toml nicht gefunden!
    pause
    exit /b 1
)

echo Aktueller Modus:
findstr "recognition_mode" config.toml
echo.
echo ----------------------------------------------------------------
echo VERFUEGBARE MODI:
echo ----------------------------------------------------------------
echo.
echo [1] FAST - Schnell (~0.1s)
echo     Nur Pattern-Matching
echo     Empfohlen fuer die meisten Nutzer
echo.
echo [2] BALANCED - Ausgewogen (~1s)
echo     Pattern + Machine Learning
echo     Bessere Erkennung von Namen ohne Titel
echo.
echo [3] ACCURATE - Maximal (~2-5s)
echo     Pattern + grosses ML-Modell
echo     Beste Genauigkeit
echo.
echo ----------------------------------------------------------------
echo.

set /p CHOICE="Waehle Modus (1/2/3) oder [Q] fuer Abbrechen: "

if /i "%CHOICE%"=="q" (
    echo.
    echo Abgebrochen!
    timeout /t 2 >nul
    exit /b 0
)

:: =================================================================
:: OPTION 1: FAST
:: =================================================================
if "%CHOICE%"=="1" (
    echo.
    echo [*] Wechsle zu FAST Modus...

    :: Erstelle temporäre Python-Script für config update
    echo import re > update_config.py
    echo with open('config.toml', 'r', encoding='utf-8') as f: >> update_config.py
    echo     content = f.read() >> update_config.py
    echo content = re.sub(r'recognition_mode = ".*"', 'recognition_mode = "fast"', content) >> update_config.py
    echo with open('config.toml', 'w', encoding='utf-8') as f: >> update_config.py
    echo     f.write(content) >> update_config.py

    python update_config.py
    if errorlevel 1 (
        echo FEHLER: Konnte config.toml nicht aktualisieren!
        del update_config.py 2>nul
        pause
        exit /b 1
    )

    del update_config.py 2>nul
    echo [OK] Modus auf FAST gesetzt!
    echo.
    echo HINWEIS: Die App muss neu gestartet werden!
    goto end
)

:: =================================================================
:: OPTION 2: BALANCED
:: =================================================================
if "%CHOICE%"=="2" (
    echo.
    echo [*] Wechsle zu BALANCED Modus...
    echo.

    :: Prüfe ob spaCy installiert ist
    python -c "import spacy" 2>nul
    if errorlevel 1 (
        echo [!] spaCy ist nicht installiert!
        echo [*] Installiere spaCy und deutsches Modell...
        echo     Bitte warten, das kann 1-2 Minuten dauern...
        echo.

        if exist venv\Scripts\activate.bat (
            call venv\Scripts\activate.bat
        )

        pip install spacy
        if errorlevel 1 (
            echo [FEHLER] Konnte spaCy nicht installieren!
            pause
            exit /b 1
        )

        python -m spacy download de_core_news_sm
        if errorlevel 1 (
            echo [FEHLER] Konnte Modell nicht downloaden!
            echo Versuche manuelle Installation mit:
            echo   pip install https://github.com/explosion/spacy-models/releases/download/de_core_news_sm-3.7.0/de_core_news_sm-3.7.0-py3-none-any.whl
            pause
            exit /b 1
        )

        echo [OK] spaCy und Modell erfolgreich installiert!
        echo.
    )

    :: Update config.toml
    echo import re > update_config.py
    echo with open('config.toml', 'r', encoding='utf-8') as f: >> update_config.py
    echo     content = f.read() >> update_config.py
    echo content = re.sub(r'recognition_mode = ".*"', 'recognition_mode = "balanced"', content) >> update_config.py
    echo with open('config.toml', 'w', encoding='utf-8') as f: >> update_config.py
    echo     f.write(content) >> update_config.py

    python update_config.py
    if errorlevel 1 (
        echo FEHLER: Konnte config.toml nicht aktualisieren!
        del update_config.py 2>nul
        pause
        exit /b 1
    )

    del update_config.py 2>nul
    echo [OK] Modus auf BALANCED gesetzt!
    echo.
    echo HINWEIS: Die App muss neu gestartet werden!
    goto end
)

:: =================================================================
:: OPTION 3: ACCURATE
:: =================================================================
if "%CHOICE%"=="3" (
    echo.
    echo [*] Wechsle zu ACCURATE Modus...
    echo.

    :: Prüfe ob spaCy installiert ist
    python -c "import spacy" 2>nul
    if errorlevel 1 (
        echo [!] spaCy ist nicht installiert!
        echo [*] Installiere spaCy zuerst...
        echo.

        if exist venv\Scripts\activate.bat (
            call venv\Scripts\activate.bat
        )

        pip install spacy
        if errorlevel 1 (
            echo [FEHLER] Konnte spaCy nicht installieren!
            pause
            exit /b 1
        )
    )

    :: Prüfe ob großes Modell installiert ist
    python -c "import spacy; spacy.load('de_core_news_lg')" 2>nul
    if errorlevel 1 (
        echo [!] Grosses spaCy-Modell nicht gefunden!
        echo [*] Lade grosses Modell herunter...
        echo     ACHTUNG: Das Modell ist ca. 500 MB gross!
        echo     Download kann 5-10 Minuten dauern...
        echo.

        choice /c JN /m "Moechtest du fortfahren"
        if errorlevel 2 (
            echo Abgebrochen!
            pause
            exit /b 0
        )

        echo.
        echo Starte Download...
        python -m spacy download de_core_news_lg
        if errorlevel 1 (
            echo.
            echo [FEHLER] Konnte Modell nicht downloaden!
            echo.
            echo Moegliche Loesungen:
            echo 1. Versuche es spaeter nochmal (GitHub Rate Limit)
            echo 2. Nutze BALANCED Modus stattdessen
            echo.
            echo Soll ich auf BALANCED Modus wechseln? (kleines Modell)

            choice /c JN /m "Auf BALANCED wechseln"
            if errorlevel 2 (
                echo Abgebrochen!
                pause
                exit /b 1
            )

            :: Wechsle zu BALANCED
            echo.
            echo [*] Wechsle zu BALANCED Modus...

            python -m spacy download de_core_news_sm
            if errorlevel 1 (
                echo [FEHLER] Auch kleines Modell konnte nicht geladen werden!
                pause
                exit /b 1
            )

            :: Update config zu balanced
            echo import re > update_config.py
            echo with open('config.toml', 'r', encoding='utf-8') as f: >> update_config.py
            echo     content = f.read() >> update_config.py
            echo content = re.sub(r'recognition_mode = ".*"', 'recognition_mode = "balanced"', content) >> update_config.py
            echo with open('config.toml', 'w', encoding='utf-8') as f: >> update_config.py
            echo     f.write(content) >> update_config.py

            python update_config.py
            del update_config.py 2>nul

            echo [OK] Modus auf BALANCED gesetzt!
            echo.
            goto end
        )

        echo.
        echo [OK] Grosses Modell erfolgreich installiert!
        echo.
    )

    :: Update config.toml zu accurate
    echo import re > update_config.py
    echo with open('config.toml', 'r', encoding='utf-8') as f: >> update_config.py
    echo     content = f.read() >> update_config.py
    echo content = re.sub(r'recognition_mode = ".*"', 'recognition_mode = "accurate"', content) >> update_config.py
    echo with open('config.toml', 'w', encoding='utf-8') as f: >> update_config.py
    echo     f.write(content) >> update_config.py

    python update_config.py
    if errorlevel 1 (
        echo FEHLER: Konnte config.toml nicht aktualisieren!
        del update_config.py 2>nul
        pause
        exit /b 1
    )

    del update_config.py 2>nul
    echo [OK] Modus auf ACCURATE gesetzt!
    echo.
    echo HINWEIS: Die App muss neu gestartet werden!
    goto end
)

echo.
echo [FEHLER] Ungueltige Auswahl!
pause
exit /b 1

:end
echo.
echo ----------------------------------------------------------------
echo.
set /p RESTART="Moechtest du die App jetzt neu starten? [J/N]: "

if /i "%RESTART%"=="j" (
    echo.
    echo [*] Starte App neu...
    start "" start.bat
    exit
)

echo.
echo Fertig! Starte die App manuell neu mit start.bat
echo.
pause
