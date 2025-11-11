# Anonymify für Windows

Ein Windows-Tool zum schnellen Anonymisieren von Texten mit **konfigurierbarem Hotkey** (Standard: Strg+Alt+A).

## ✨ Features

- **🎯 Konfigurierbarer Hotkey**: Standard Strg+Alt+A, aber änderbar in `config.toml`
- **📝 Whitelist**: Namen die NICHT anonymisiert werden sollen (z.B. "Gericht", "Richter")
- **🤖 Microsoft Presidio**: Professionelle PII-Erkennung und Anonymisierung
- **🖥️ System Tray Icon**: Läuft diskret im Hintergrund mit Farbwechsel-Status
- **🇩🇪 Deutsche Sprache**: Optimiert für deutsche Texte (Anwalts-Patterns!)
- **🔍 Erweiterte Erkennung**: Namen (mit Titeln), Adressen, Aktenzeichen, IBAN, Kontonummern, etc.
- **⚡ Automatischer Workflow**: Nur Text markieren + Hotkey → fertig!

## Workflow

1. Text markieren (blau markieren wie gewohnt)
2. **Strg+Alt+A** drücken (kopiert automatisch!)
3. Anonymisierten Text einfügen (Strg+V)
4. Fertig! Jetzt sicher an KI senden

**Noch einfacher!** Du musst nicht mehr Strg+C drücken - nur markieren und Strg+Alt+A!

## 🚀 Schnellstart Installation

### Voraussetzungen

- Windows 10/11
- Python 3.8+ ([Download](https://www.python.org/downloads/))
- Admin-Rechte (für globale Hotkeys)

### ⚡ Automatische Installation (EMPFOHLEN)

```bash
# 1. Repository klonen oder ZIP herunterladen
git clone <repository-url>
cd Privatisierungsapp

# 2. Automatisches Setup starten
install.bat
```

Das war's! `install.bat` macht automatisch:
- ✅ Python-Version prüfen
- ✅ Virtuelle Umgebung erstellen
- ✅ Alle Dependencies installieren
- ✅ Optional: Auto-Start einrichten
- ✅ App starten

### 📝 Manuelle Installation

Siehe [WINDOWS_README.md](WINDOWS_README.md) für detaillierte Anleitung.

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

## 🔍 Erkannte PII-Typen

### Standard-Daten
- `<PERSON>` - Namen von Personen (mit Titeln wie Dr., Prof.)
- `<EMAIL>` - E-Mail-Adressen
- `<TELEFON>` - Telefonnummern (deutsche Formate)
- `<ADRESSE>` - Straßenadressen (Hauptstraße, Musterweg, etc.)
- `<ORT>` - PLZ + Städte
- `<DATUM>` - Datums- und Zeitangaben
- `<KREDITKARTE>` - Kreditkartennummern
- `<IBAN>` - Bankverbindungen (IBAN)
- `<KONTO-NR>` - Kontonummern
- `<IP-ADRESSE>` - IP-Adressen
- `<URL>` - Webseiten-URLs

### Anwalts-spezifische Daten
- `<AKTENZEICHEN>` - Aktenzeichen (Az. 1 Js 123/21)
- `<STEUER-ID>` - Steuer-IDs
- `<SV-NUMMER>` - Sozialversicherungsnummern
- `<AUSWEIS-NR>` - Personalausweis-Nummern

## ⚙️ Konfiguration

Bearbeite `config.toml` um die App anzupassen:

### Hotkey ändern
```toml
[hotkey]
combination = "ctrl+alt+a"  # Ändere zu z.B. "ctrl+shift+a"
```

### Whitelist hinzufügen
```toml
[whitelist]
custom = [
    "Musterstadt GmbH",  # Wird NICHT anonymisiert
    "Rechtsanwalt Müller",
]
```

### Entities deaktivieren
```toml
[anonymization]
enable_date = false  # Datum wird NICHT anonymisiert
enable_url = false   # URLs werden NICHT anonymisiert
```

## 🔄 Auto-Start einrichten

Der `install.bat` Installer bietet 3 Optionen:

**Option 1: Startup-Ordner** (Einfach, OHNE Admin)
- ✅ Einfach einzurichten
- ❌ Hotkey funktioniert evtl. nicht ohne Admin

**Option 2: Task Scheduler** (MIT Admin-Rechten)
- ✅ Hotkey funktioniert zuverlässig
- ⚠️ Benötigt Admin-Rechte bei Einrichtung
- Führe `setup_admin_autostart.bat` als Administrator aus

**Option 3: Manuell starten**
- Rechtsklick auf `start.bat` → "Als Administrator ausführen"

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

## 📱 Cloud-Testing (ohne Windows PC)

Wenn du keinen Windows-PC hast, kannst du die Anonymisierung auf Cloud-Plattformen testen!

Siehe **[examples/docs/](examples/docs/)** für:
- `COLAB_ANLEITUNG.md` - Google Colab Setup
- `PRESIDIO_COLAB.md` - Presidio auf Colab nutzen
- `ANWALT_ANLEITUNG.md` - Anleitung für Anwälte (DSGVO)

Test-Scripts in **[examples/colab-tests/](examples/colab-tests/)**:
- `presidio_anwalt.py` - Vollständiges Beispiel mit allen Patterns
- `test_interactive.py` - Interaktiver Test mit Eingabe
- `test_simple.py` - Einfacher Regex-basierter Demo

## Support

Bei Fragen oder Problemen bitte ein Issue erstellen.