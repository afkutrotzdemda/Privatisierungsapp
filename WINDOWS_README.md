# 🪟 Anonymify für Windows

**DSGVO-konforme Text-Anonymisierung mit einem Tastendruck!**

Speziell entwickelt für **Anwälte** und alle die sensible Daten vor dem Senden an KI-Systeme (ChatGPT, Claude, etc.) schützen müssen.

---

## 🚀 Schnellinstallation

### 1. Python installieren (falls noch nicht vorhanden)

**Download**: https://www.python.org/downloads/

⚠️ **WICHTIG**: Bei der Installation **"Add Python to PATH"** aktivieren!

### 2. Repository herunterladen

```bash
git clone https://github.com/IHR-USERNAME/Privatisierungsapp
cd Privatisierungsapp
```

Oder: Als ZIP herunterladen und entpacken

### 3. Installation starten

**Doppelklick auf**: `install.bat`

Das Script installiert **automatisch**:
- ✅ Alle Python-Packages
- ✅ Microsoft Presidio (PII-Erkennung)
- ✅ Hotkey-System
- ✅ System Tray Icon
- ✅ Optional: Auto-Start mit Windows

**Installation dauert ca. 2-3 Minuten** (beim ersten Mal)

---

## 💡 Verwendung

### Start

**Doppelklick auf**: `start.bat`

→ Ein **Icon mit "A"** erscheint in der Taskleiste

### Workflow (noch einfacher!)

1. **Text markieren** (blau markieren wie gewohnt)
   - Z.B. Mandantenbrief, Schriftsatz, E-Mail

2. **Strg+Alt+A drücken**
   - Programm kopiert automatisch (Strg+C wird simuliert)
   - Icon wird **GELB** während anonymisiert wird

3. **Text einfügen** (Strg+V)
   - Jetzt ist der Text anonymisiert!
   - Icon ist wieder **GRÜN**

4. **An KI senden**
   - DSGVO-konform ✓

**Du musst NICHT mehr Strg+C drücken!** Nur markieren und Strg+Alt+A! ✨

---

## 🎨 Icon-Farben

Das Tray Icon zeigt den aktuellen Status:

| Farbe | Status | Bedeutung |
|-------|--------|-----------|
| 🟢 **GRÜN** | Bereit | App läuft, wartet auf Strg+Alt+A |
| 🟡 **GELB** | Arbeitet | Anonymisiert gerade Text... |
| 🔴 **ROT** | Fehler | Etwas ist schiefgelaufen (nach 3 Sek wieder grün) |

---

## 🔒 Was wird anonymisiert?

### Persönliche Daten

- **Namen**: Max Mustermann → `<PERSON>`
- **E-Mail**: max@example.com → `<EMAIL>`
- **Telefon**: 0176 123456, +49 30 123456 → `<TELEFON>`
- **Adressen**: Hauptstraße 45 → `<ADRESSE>`
- **PLZ/Stadt**: 10115 Berlin → `<ORT>`
- **Geburtsdatum**: 15.03.1990 → `<DATUM>`

### Juristische Daten (für Anwälte)

- **Aktenzeichen**: Az. 1 Js 123/21 → `<AKTENZEICHEN>`

### Identifikationsnummern

- **IBAN**: DE89 3704... → `<IBAN>`
- **Kontonummer**: Konto-Nr. 1234567890 → `<KONTO-NR>`
- **Steuer-ID**: 12345678901 → `<STEUER-ID>`
- **Personalausweis**: L123456789 → `<AUSWEIS-NR>`
- **Sozialversicherung**: 12 123456 A 123 → `<SV-NUMMER>`
- **Kreditkarte**: 4111 1111 1111 1111 → `<KREDITKARTE>`

### Technische Daten

- **IP-Adresse**: 192.168.1.1 → `<IP-ADRESSE>`
- **URL**: www.example.com → `<URL>`

---

## 📋 Beispiel für Anwälte

### Vorher:

```
Betreff: Mandant Dr. Max Mustermann

Sehr geehrte Damen und Herren,

im Verfahren Az. 1 Js 123/21 gegen meinen Mandanten
Dr. Max Mustermann, wohnhaft Hauptstraße 45, 10115 Berlin,
geboren am 15.03.1985, Tel: 0176 12345678,
Email: mustermann@email.de, IBAN: DE89 3704 0044 0532 0130 00,
möchte ich folgende Unterlagen einreichen...
```

### **Strg+Alt+A drücken...**

### Nachher:

```
Betreff: Mandant <PERSON>

Sehr geehrte Damen und Herren,

im Verfahren <AKTENZEICHEN> gegen meinen Mandanten
<PERSON>, wohnhaft <ADRESSE>, <ORT>,
geboren am <DATUM>, Tel: <TELEFON>,
Email: <EMAIL>, IBAN: <IBAN>,
möchte ich folgende Unterlagen einreichen...
```

→ **Jetzt sicher an ChatGPT/Claude senden!** ✅

---

## ⚙️ Auto-Start

### Aktivieren während Installation

Beim `install.bat` wird gefragt:
```
Auto-Start aktivieren? (j/n): j
```

### Manuell aktivieren

1. Erstelle Verknüpfung zu `start.bat`
2. Kopiere nach: `C:\Users\DEIN-NAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`

### Deaktivieren

Lösche Verknüpfung aus dem Autostart-Ordner

---

## 🛠 Fehlerbehebung

### "Python nicht gefunden"

**Lösung**:
1. Python installieren: https://www.python.org/downloads/
2. Bei Installation **"Add Python to PATH"** aktivieren
3. Windows neu starten
4. `install.bat` erneut ausführen

### Hotkey funktioniert nicht

**Mögliche Ursachen**:
- App läuft nicht als Administrator
- Andere App verwendet bereits Strg+Alt+A
- Keyboard-Package nicht richtig installiert

**Lösung**:
1. `start.bat` als Administrator ausführen (Rechtsklick → "Als Administrator ausführen")
2. Andere Apps schließen die Strg+Alt+A verwenden könnten
3. In `anonymizer.log` nach Fehlern suchen

### Icon erscheint nicht in Taskleiste

**Lösung**:
1. Prüfe ob `python.exe` in den Taskleistensymbolen versteckt ist
2. Klick auf `^` in der Taskleiste
3. Suche nach dem "A"-Icon

### "Fehler beim Anonymisieren"

Icon wird **ROT** für 3 Sekunden:

**Lösung**:
1. Prüfe ob Zwischenablage Text enthält (nicht leer)
2. Schaue in `anonymizer.log` für Details
3. Bei Problemen: Issue auf GitHub erstellen

---

## 📁 Projekt-Struktur

```
Privatisierungsapp/
├── install.bat              ← Installations-Script (START HIER!)
├── start.bat                ← App starten
├── main.py                  ← Hauptprogramm
├── requirements.txt         ← Python-Dependencies
├── src/
│   ├── anonymizer.py        ← Presidio-Integration
│   ├── hotkey_handler.py    ← Strg+Alt+A Handler
│   └── tray_icon.py         ← System Tray Icon
├── presidio_anwalt.py       ← Test-Script für Anwälte
└── anonymizer.log           ← Log-Datei (wird automatisch erstellt)
```

---

## 🔄 Updates

### Neue Version installieren

```bash
cd Privatisierungsapp
git pull
call venv\Scripts\activate.bat
pip install -r requirements.txt --upgrade
```

Oder: Neu clonen und `install.bat` erneut ausführen

---

## 📖 Logs

Alle Aktivitäten werden geloggt in: `anonymizer.log`

**Nützlich für**:
- Debugging
- Nachvollziehen was anonymisiert wurde
- Performance-Analyse

**Inhalt**:
```
2024-11-15 14:30:45 - Hotkey ctrl+alt+a gedrückt!
2024-11-15 14:30:45 - Text aus Zwischenablage gelesen (1234 Zeichen)
2024-11-15 14:30:46 - Anonymisierter Text in Zwischenablage kopiert!
```

---

## ⚖️ Für Anwälte

### DSGVO-Compliance

Dieses Tool hilft bei:
- **Art. 5 DSGVO** (Datenminimierung)
- **Art. 25 DSGVO** (Privacy by Design)
- **§ 203 StGB** (Verschwiegenheitspflicht)
- **§ 43a BRAO** (Verschwiegenheitspflicht Rechtsanwälte)

⚠️ **Hinweis**: Dies ersetzt NICHT Ihre Sorgfaltspflicht!
- Immer Output manuell prüfen
- Bei Bedarf Datenschutzbeauftragten konsultieren
- Mandanten ggf. über KI-Nutzung informieren

### Workflow-Integration Kanzlei

```
1. Schriftsatz in Word schreiben
2. Text markieren und kopieren (Strg+C)
3. Strg+Alt+A drücken
4. In ChatGPT/Claude einfügen (Strg+V)
5. "Bitte überprüfe diesen Schriftsatz rechtlich..."
6. KI-Vorschläge prüfen und übernehmen
7. Original-Namen wieder einsetzen
8. Finales Dokument speichern
```

**Zeitersparnis**: 30-50% bei Schriftsatz-Erstellung!

---

## 🚨 Wichtige Hinweise

### ✅ Was Sie tun sollten:

- Immer vor KI-Nutzung anonymisieren
- Output manuell kontrollieren
- Bei wichtigen Fällen besonders gründlich prüfen
- Logs regelmäßig überprüfen

### ❌ Was dieses Tool NICHT macht:

- 100% Garantie (manuell nachprüfen!)
- Rechtliche Beratung ersetzen
- Mandanteneinwilligung ersetzen
- Verschlüsselte Übertragung (HTTPS liegt bei KI-Anbieter)

---

## 🆘 Support

### Bei Problemen:

1. **Log-Datei prüfen**: `anonymizer.log`
2. **GitHub Issues**: https://github.com/IHR-REPO/issues
3. **Dokumentation**: Siehe `README.md` und `ANWALT_ANLEITUNG.md`

### Feature-Requests:

Öffne ein Issue auf GitHub mit:
- Beschreibung was fehlt
- Beispiel-Text der nicht erkannt wird
- Use-Case Beschreibung

---

## 📜 Lizenz

MIT License - Frei verwendbar auch kommerziell.

**Haftungsausschluss**: Keine Gewährleistung für vollständige Anonymisierung.
Nutzer trägt Verantwortung für DSGVO-Compliance.

---

## 🎯 Roadmap

### Geplante Features:

- [ ] Konfigurierbare Tastenkombination
- [ ] Mehrsprachigkeit (EN, FR, IT)
- [ ] Whitelist für bestimmte Namen/Begriffe
- [ ] Statistiken (wie viele Daten anonymisiert)
- [ ] Cloud-Sync für Einstellungen
- [ ] Portable Version (ohne Installation)

---

**Viel Erfolg beim DSGVO-konformen Arbeiten mit KI!** ⚖️🔒

Bei Fragen: GitHub Issues oder E-Mail an [IHR-KONTAKT]
