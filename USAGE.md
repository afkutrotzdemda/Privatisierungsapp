# 📖 ANONYMIFY - NUTZUNGSANLEITUNG

## 🚀 Schnellstart

1. **Installation:** `install.bat` ausführen
2. **App starten:** `start.bat` (als Administrator!)
3. **Text anonymisieren:**
   - Text markieren
   - `Strg+Alt+A` drücken
   - Fertig! Text ist in Zwischenablage

## 🎯 Use-Case: Text vor AI-Nutzung anonymisieren

### Workflow:

```
1. Anwaltsschreiben in Word/PDF öffnen
2. Text markieren (Strg+A)
3. Strg+Alt+A drücken
4. In ChatGPT/Claude einfügen (Strg+V)
5. AI schreibt anonymisierten Entwurf
6. Entwurf mit echten Namen korrigieren
```

### Beispiel:

**Vorher:**
```
Dr. Markus Schmidt (m.schmidt@kanzlei.de)
Hauptstraße 123, 10115 Berlin
Tel: 030 12345678
IBAN: DE89 3704 0044 0532 0130 00
```

**Nachher (für AI):**
```
Dr. S. (***@***.de)
H.straße 123, XXXXX B.
Tel: 030 XXXXXX
IBAN: DE** ****
```

**✅ DSGVO-konform!** Keine echten Personendaten an AI-Dienste!

---

## 🎚️ MODI WECHSELN

### Verfügbare Modi:

| Modus | Geschwindigkeit | Genauigkeit | Empfohlen für |
|-------|----------------|-------------|---------------|
| **FAST** | ~0.1s | Gut | Die meisten Nutzer |
| **BALANCED** | ~1s | Sehr gut | Mehr Genauigkeit |
| **ACCURATE** | ~2-5s | Maximal | Höchste Genauigkeit |

### Modi wechseln:

```cmd
wechsel_modus.bat
```

**Oder manuell:** `config.toml` öffnen und ändern:
```toml
[anonymization]
recognition_mode = "fast"    # oder "balanced" / "accurate"
```

---

## 🔧 KONFIGURATION

### Whitelist anpassen

In `config.toml` kannst du Begriffe hinzufügen die NICHT anonymisiert werden:

```toml
[whitelist]
# Eigene Begriffe
custom = [
    "Meine Kanzlei GmbH",
    "Spezifischer Firmenname",
]
```

### Hotkey ändern

```toml
[hotkey]
combination = "ctrl+alt+a"   # z.B. "ctrl+shift+a"
```

---

## 🔄 AUTOSTART

### Autostart aktivieren:
```cmd
setup_admin_autostart.bat
```

### Autostart deaktivieren:
```cmd
autostart_aus.bat
```

---

## 🧪 TESTEN

### Vollständiger Test mit Anwaltsschreiben:
```cmd
python test_anonymisierung.py
```

### Edge-Case Tests:
```cmd
python test_edge_cases.py
```

### Test-Dateien:
- `test_anwaltsschreiben.txt` - Realistisches Anwaltsschreiben
- `test_anonymisiert.txt` - Beispiel-Output

---

## 📊 WAS WIRD ANONYMISIERT?

| Daten-Typ | Beispiel | Anonymisiert zu |
|-----------|----------|-----------------|
| **Namen** | Herr Dr. Müller | Herr Dr. M. |
| **Straßen** | Hauptstraße 123 | H.straße 123 |
| **Orte** | 10115 Berlin | XXXXX B. |
| **E-Mail** | max@firma.de | \*\*\*@\*\*\*.de |
| **Telefon** | 030 12345678 | 030 XXXXXX |
| **IBAN** | DE89 3704... | DE\*\* \*\*\*\* |
| **Datum** | 15.03.2024 | XX.03.2024 |
| **Aktenzeichen** | 123 C 456/2024 | \*\*\* C \*\*\*/2024 |

---

## ⚠️ WICHTIGE HINWEISE

### ✅ Perfekt für:
- ChatGPT/Claude für Textentwürfe
- AI für Formulierungsvorschläge
- AI für Rechtsprüfungen (ohne echte Namen)

### ⚠️ NICHT geeignet für:
- Maximale Anonymität (Gerichtsurteile veröffentlichen)
- Wissenschaftliche Anonymisierung
- Wenn Kontext komplett entfernt werden muss

### ⚠️ Beachte:
- Kontext bleibt teilweise erhalten ("XXXXX B." = Berlin)
- Bei mehreren Personen mit gleichem Anfangsbuchstaben kann Verwirrung entstehen
- Whitelist muss gepflegt werden (z.B. "Richter" könnte auch ein Name sein)

---

## 🐛 PROBLEME LÖSEN

### App startet nicht:
1. Als Administrator ausführen (Rechtsklick → "Als Administrator")
2. `install.bat` nochmal ausführen
3. Python-Installation prüfen (`python --version`)

### Hotkey funktioniert nicht:
- **Ursache:** Keine Admin-Rechte
- **Lösung:** `start.bat` als Administrator ausführen

### Zu viele Wörter werden anonymisiert:
- **Lösung:** Whitelist erweitern in `config.toml`
- Oder: Modus auf "fast" setzen (restriktiver)

### Zu wenig Wörter werden anonymisiert:
- **Lösung:** Modus auf "balanced" oder "accurate" wechseln
- `wechsel_modus.bat` ausführen

---

## 📞 SUPPORT

- **Issues:** https://github.com/afkutrotzdemda/Privatisierungsapp/issues
- **Dokumentation:** Siehe README.md und QUICKSTART.md

---

## 📝 BEISPIEL-WORKFLOW

### Schritt-für-Schritt: Anwaltsschreiben mit ChatGPT überarbeiten

1. **Anwaltsschreiben öffnen** (Word/PDF)
2. **Text markieren** (Strg+A)
3. **Anonymisieren** (Strg+Alt+A)
   - ✅ Text ist jetzt in Zwischenablage
4. **ChatGPT öffnen**
5. **Prompt schreiben:**
   ```
   Überarbeite dieses Anwaltsschreiben und mache es
   professioneller. Behalte die Struktur bei.

   [Anonymisierten Text einfügen - Strg+V]
   ```
6. **ChatGPT-Antwort kopieren**
7. **In Word einfügen**
8. **Echte Namen wieder einsetzen** (Suchen & Ersetzen)
   - "Herr M." → "Herr Müller"
   - "Dr. S." → "Dr. Schmidt"
   - "XXXXX B." → "10115 Berlin"
9. **Fertig!** ✅

**DSGVO-konform:** ChatGPT hat keine echten Personendaten erhalten!

---

## 🎓 BEST PRACTICES

### 1. Whitelist pflegen
- Füge häufige Firmen/Organisationen hinzu
- Prüfe regelmäßig ob Begriffe fälschlich anonymisiert werden

### 2. Modus wählen
- **FAST:** Für tägliche Nutzung (empfohlen)
- **BALANCED:** Wenn Namen ohne Titel vorkommen
- **ACCURATE:** Für komplexe Texte

### 3. Vor großen Texten testen
- Teste mit `test_anonymisierung.py`
- Prüfe Output in `test_anonymisiert.txt`

### 4. Autostart nur wenn täglich genutzt
- Sonst: Manuell mit `start.bat` starten
- Deaktivieren mit `autostart_aus.bat`

---

Viel Erfolg mit Anonymify! 🎉
