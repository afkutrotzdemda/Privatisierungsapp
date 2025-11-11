# ⚡ Anonymify - Schnellstart

## 🚨 **WICHTIG: Installation zuerst!**

Bevor du `start.bat` ausführst, **musst** du die Installation durchführen!

---

## 📋 **Schritt-für-Schritt Anleitung**

### ✅ **Schritt 1: Python installieren**

Falls noch nicht vorhanden:
1. Download: https://www.python.org/downloads/
2. ⚠️ **WICHTIG:** Bei Installation **"Add Python to PATH"** anhaken!
3. Installation abschließen

### ✅ **Schritt 2: Installation durchführen**

```
📂 Ordner "Privatisierungsapp" öffnen
👉 Doppelklick auf: install.bat
⏳ Warten bis fertig (kann 2-5 Minuten dauern)
```

**Was macht install.bat?**
- Prüft Python-Installation
- Erstellt virtuelle Umgebung (venv)
- Installiert alle Dependencies (Presidio, etc.)
- Richtet optional Auto-Start ein

### ✅ **Schritt 3: Programm starten**

```
👉 Rechtsklick auf: start.bat
🔧 Wähle: "Als Administrator ausführen"
✅ Grünes "A" Icon erscheint in Taskleiste
```

**⚠️ WICHTIG:** Als Administrator ausführen!
- Der globale Hotkey (Strg+Alt+A) braucht Admin-Rechte
- Ohne Admin funktioniert der Hotkey nicht!

---

## 🎯 **Verwendung**

1. **Markiere Text** in beliebiger App (Word, Browser, etc.)
2. **Drücke Strg+Alt+A** (kopiert automatisch + anonymisiert!)
3. **Füge ein** mit Strg+V
4. ✅ **Fertig!** Text ist anonymisiert

### **Icon-Farben:**
- 🟢 **Grün** = Bereit
- 🟡 **Gelb** = Anonymisiert gerade...
- 🔴 **Rot** = Fehler

---

## 🔧 **Häufige Probleme**

### ❌ **"ModuleNotFoundError: No module named 'presidio_analyzer'"**

**Problem:** Installation wurde nicht durchgeführt oder fehlgeschlagen.

**Lösung:**
```
1. Schließe alle Fenster
2. Doppelklick install.bat
3. Warte bis "Installation abgeschlossen!"
4. Dann: Rechtsklick start.bat → "Als Administrator ausführen"
```

---

### ❌ **"Python ist nicht installiert"**

**Problem:** Python fehlt oder nicht im PATH.

**Lösung:**
```
1. Python von python.org herunterladen
2. Bei Installation "Add Python to PATH" anhaken!
3. Nach Installation: install.bat erneut ausführen
```

---

### ❌ **Hotkey funktioniert nicht**

**Problem:** Programm läuft nicht als Administrator.

**Lösung:**
```
1. Rechtsklick start.bat
2. "Als Administrator ausführen" wählen
3. Im UAC-Dialog "Ja" klicken
```

---

### ❌ **Icon erscheint nicht in Taskleiste**

**Problem:** Dependencies fehlen oder Programm hat Fehler.

**Lösung:**
```
1. Schaue in anonymizer.log (im Projektordner)
2. Führe install.bat erneut aus
3. Starte Windows-Explorer neu (Strg+Shift+Esc → Windows-Explorer neu starten)
```

---

## ⚙️ **Konfiguration**

### **Hotkey ändern:**
```
1. Öffne config.toml mit Texteditor
2. Ändere: combination = "ctrl+alt+a"
   z.B. zu: combination = "ctrl+shift+a"
3. Speichern
4. App neu starten
```

### **Whitelist hinzufügen:**
```
1. Öffne config.toml
2. Unter [whitelist] → custom hinzufügen:
   custom = ["Meine Firma", "Spezialausdruck"]
3. Speichern
4. App neu starten
```

---

## 📞 **Support**

- **Log-Datei:** `anonymizer.log` (im Projektordner)
- **GitHub Issues:** Erstelle Issue mit Log-Inhalt
- **Dokumentation:** Siehe README.md und WINDOWS_README.md

---

## 🎓 **Testing ohne Windows PC**

Du hast keinen Windows-PC zum Testen?

👉 Siehe `examples/docs/COLAB_ANLEITUNG.md` für Google Colab Setup
👉 Test-Scripts in `examples/colab-tests/`

---

## ✨ **Features**

- ✅ Konfigurierbarer Hotkey (Standard: Strg+Alt+A)
- ✅ Whitelist (Namen die nicht anonymisiert werden)
- ✅ Deutsche Patterns (Anwälte, Adressen, Aktenzeichen)
- ✅ Microsoft Presidio (professionelle PII-Erkennung)
- ✅ System Tray Icon mit Farbwechsel
- ✅ Auto-Start (optional)
- ✅ Ausführliche Logs
- ✅ DSGVO-konform

---

**Viel Erfolg!** 🚀
