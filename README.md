# Text Anonymisierer für Windows

Ein Windows-Tool zum schnellen Anonymisieren von Texten mit **Strg+Alt+A**.

## Features

- **Globaler Hotkey**: Strg+Alt+A anonymisiert automatisch Text aus der Zwischenablage
- **Microsoft Presidio**: Professionelle PII-Erkennung und Anonymisierung
- **System Tray Icon**: Läuft diskret im Hintergrund
- **Deutsche Sprache**: Optimiert für deutsche Texte
- **Automatische Erkennung**: Namen, E-Mails, Telefonnummern, Adressen, Daten, etc.

## Workflow

1. Text markieren (blau markieren wie gewohnt)
2. **Strg+Alt+A** drücken (kopiert automatisch!)
3. Anonymisierten Text einfügen (Strg+V)
4. Fertig! Jetzt sicher an KI senden

**Noch einfacher!** Du musst nicht mehr Strg+C drücken - nur markieren und Strg+Alt+A!

## Installation

### Voraussetzungen

- Windows 10/11
- Python 3.8 oder höher
- Administrator-Rechte (für globale Hotkeys)

### Schritt 1: Python installieren

Falls noch nicht vorhanden:
1. Download von [python.org](https://www.python.org/downloads/)
2. Bei Installation "Add Python to PATH" aktivieren

### Schritt 2: Projekt einrichten

```bash
# Repository klonen oder herunterladen
git clone <repository-url>
cd Privatisierungsapp

# Virtuelle Umgebung erstellen (empfohlen)
python -m venv venv

# Virtuelle Umgebung aktivieren
venv\Scripts\activate

# Dependencies installieren
pip install -r requirements.txt

# Deutsches Sprachmodell für spaCy herunterladen (optional, falls benötigt)
python -m spacy download de_core_news_sm
```

### Schritt 3: Starten

```bash
# Mit aktivierter virtueller Umgebung:
python main.py
```

Das Programm läuft nun im Hintergrund mit einem Icon in der System Tray.

## Nutzung

1. **Programm starten**: `python main.py`
2. **System Tray Icon**: Ein blaues "A" erscheint in der Taskleiste
3. **Text kopieren**: Markiere und kopiere Text (Strg+C)
4. **Anonymisieren**: Drücke **Strg+Alt+A**
5. **Einfügen**: Der Text in der Zwischenablage ist jetzt anonymisiert (Strg+V)

## Beispiel

**Original:**
```
Hallo, ich bin Max Mustermann und wohne in der Hauptstraße 123, Berlin.
Meine E-Mail ist max.mustermann@example.com und meine Telefonnummer ist +49 123 456789.
```

**Nach Strg+Alt+A:**
```
Hallo, ich bin <PERSON> und wohne in der <ORT>.
Meine E-Mail ist <EMAIL> und meine Telefonnummer ist <TELEFON>.
```

## Erkannte PII-Typen

- `<PERSON>` - Namen von Personen
- `<EMAIL>` - E-Mail-Adressen
- `<TELEFON>` - Telefonnummern
- `<ORT>` - Orte und Adressen
- `<DATUM>` - Datums- und Zeitangaben
- `<KREDITKARTE>` - Kreditkartennummern
- `<IBAN>` - Bankverbindungen
- `<IP-ADRESSE>` - IP-Adressen
- `<URL>` - Webseiten-URLs

## Autostart einrichten (Optional)

### Variante 1: Verknüpfung im Autostart-Ordner

1. Erstelle eine Verknüpfung zu `main.py`
2. Kopiere sie nach: `C:\Users\[DEIN_NAME]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`

### Variante 2: Task Scheduler

1. Windows-Taskplaner öffnen
2. Neue Aufgabe erstellen
3. Bei "Trigger": Bei Anmeldung
4. Bei "Aktion": `python.exe` mit Argument `"C:\Pfad\zu\main.py"`

## Logs

Logs werden in `anonymizer.log` gespeichert und helfen bei der Fehlersuche.

## Technische Details

- **Framework**: Python 3
- **Anonymisierung**: Microsoft Presidio
- **Hotkey**: keyboard library
- **Zwischenablage**: pyperclip
- **Tray Icon**: pystray

## Troubleshooting

**Hotkey funktioniert nicht:**
- Programm als Administrator starten
- Prüfen ob andere Programme Strg+Alt+A verwenden
- Log-Datei prüfen

**Presidio lädt nicht:**
- `pip install --upgrade presidio-analyzer presidio-anonymizer`
- Internetverbindung prüfen (lädt Modelle beim ersten Start)

**System Tray Icon erscheint nicht:**
- `pip install --upgrade pystray Pillow`
- Windows-Explorer neustarten

## Lizenz

MIT License

## Cloud-Plattformen zum Testen (ohne Windows PC)

Wenn du das Projekt testen möchtest ohne Windows PC:

### 1. **Replit** (EMPFOHLEN für schnelle Tests)
🔗 https://replit.com
- Kostenlos
- Direkt im Browser (auch auf Android/Tablet)
- Python vorinstalliert
- Einfach Projekt hochladen und ausführen
- **Tipp**: Nutze `test_simple.py` für schnelle Demo

### 2. **Google Colab** (Für Jupyter Notebooks)
🔗 https://colab.research.google.com
- Kostenlos mit Google Account
- GPU verfügbar
- Gut für Presidio-Tests
- Funktioniert auf Tablets

### 3. **GitHub Codespaces**
🔗 https://github.com/codespaces
- 60 Stunden/Monat kostenlos
- VS Code im Browser
- Voller Linux-Zugriff
- Beste Option für vollständige Tests

### 4. **PythonAnywhere**
🔗 https://www.pythonanywhere.com
- Free Tier verfügbar
- Web-basierte Konsole
- Gut für längerfristige Tests

### Quick-Test auf Replit:

```bash
# 1. Auf replit.com registrieren
# 2. "Create Repl" → "Import from GitHub"
# 3. Deine Repository-URL eingeben
# 4. In der Shell ausführen:
pip install presidio-analyzer presidio-anonymizer
python test_simple.py
```

## Hinweis zur Test-Version

- `test_simple.py` - Funktioniert überall, nutzt nur Regex (Demo)
- `test_anonymizer.py` - Benötigt Presidio (genauer, braucht mehr Setup)
- Die Windows-App benötigt natürlich Windows für Hotkeys und System Tray

## Support

Bei Fragen oder Problemen bitte ein Issue erstellen.