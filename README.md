# Text Anonymisierer für Windows

Ein Windows-Tool zum schnellen Anonymisieren von Texten mit **Strg+Alt+A**.

## Features

- **Globaler Hotkey**: Strg+Alt+A anonymisiert automatisch Text aus der Zwischenablage
- **Microsoft Presidio**: Professionelle PII-Erkennung und Anonymisierung
- **System Tray Icon**: Läuft diskret im Hintergrund
- **Deutsche Sprache**: Optimiert für deutsche Texte
- **Automatische Erkennung**: Namen, E-Mails, Telefonnummern, Adressen, Daten, etc.

## Workflow

1. Text kopieren (Strg+C)
2. **Strg+Alt+A** drücken
3. Anonymisierten Text einfügen (Strg+V)
4. Fertig! Jetzt sicher an KI senden

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

## Support

Bei Fragen oder Problemen bitte ein Issue erstellen.