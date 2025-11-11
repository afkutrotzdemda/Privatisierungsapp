# 🚀 Anleitung für Google Colab / Replit

## So nutzt du den Text Anonymisierer auf deinem Tablet:

---

## Option 1: Google Colab (EMPFOHLEN)

### Schritt 1: Öffne Google Colab
Gehe zu: https://colab.research.google.com

### Schritt 2: Erstelle ein neues Notebook
- Klick auf "Neues Notebook" oder "File → New Notebook"

### Schritt 3: Kopiere diesen Code in die erste Zelle:

```python
# Projekt herunterladen
!git clone https://github.com/DEIN-USERNAME/Privatisierungsapp
%cd Privatisierungsapp

# Test mit Beispielen ausführen
!python test_simple.py
```

### Schritt 4: Für eigenen Text - Neue Zelle mit:

```python
# Interaktive Version
!python test_interactive.py
```

### Schritt 5: Oder direkt im Notebook verwenden:

```python
import re

def anonymize(text):
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '<EMAIL>', text)
    text = re.sub(r'\+?\d{1,4}[\s\-]?\(?\d{1,4}\)?[\s\-]?\d{1,4}[\s\-]?\d{1,9}', '<TELEFON>', text)
    text = re.sub(r'\b[A-Z]{2}\d{2}\s?(\d{4}\s?){4}\d{2}\b', '<IBAN>', text)
    text = re.sub(r'\b\d{1,2}\.\d{1,2}\.\d{4}\b', '<DATUM>', text)
    text = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '<IP-ADRESSE>', text)
    text = re.sub(r'https?://[^\s]+', '<URL>', text)
    text = re.sub(r'www\.[^\s]+', '<URL>', text)
    text = re.sub(r'\b(Herr|Frau)\s+(Dr\.\s+)?[A-Z][a-z]+\s+[A-Z][a-z]+\b', r'\1 <PERSON>', text)
    text = re.sub(r'\b[A-ZÄÖÜ][a-zäöüß]+straße\s+\d+[a-z]?\b', '<ADRESSE>', text)
    return text

# DEINEN TEXT HIER EINFÜGEN:
mein_text = """
Max Mustermann
Email: max@example.com
Tel: 0176 12345678
"""

print("ORIGINAL:")
print(mein_text)
print("\nANONYMISIERT:")
print(anonymize(mein_text))
```

---

## Option 2: Replit

### Schritt 1: Gehe zu Replit
https://replit.com

### Schritt 2: Registrieren (kostenlos)
- Mit Email oder GitHub Account

### Schritt 3: Import von GitHub
- Klick "Create Repl"
- Wähle "Import from GitHub"
- Gib deine Repository-URL ein: `https://github.com/DEIN-USERNAME/Privatisierungsapp`

### Schritt 4: Programm ausführen
In der Shell (Console):
```bash
python test_simple.py
```

Oder für interaktive Nutzung:
```bash
python test_interactive.py
```

### Schritt 5: Eigene Texte testen
- Einfach in der Console eigenen Text eingeben wenn `test_interactive.py` läuft
- Oder: Erstelle eine neue Datei `mein_test.py` und nutze die anonymize-Funktion

---

## Was du sehen wirst:

### Output von `test_simple.py`:
```
======================================================================
TEST 1
======================================================================

ORIGINAL:
----------------------------------------------------------------------
Hallo, ich bin Max Mustermann und wohne in der Hauptstraße 123
Meine E-Mail ist max.mustermann@example.com

ANONYMISIERT:
----------------------------------------------------------------------
Hallo, ich bin Max Mustermann und wohne in der <ADRESSE>
Meine E-Mail ist <EMAIL>
```

### Output von `test_interactive.py`:
```
🔒 TEXT ANONYMISIERER - Interaktive Version

Gib deinen Text ein:
> Max Mustermann, Tel: 0176 123456

ANONYMISIERT:
Max Mustermann, Tel: <TELEFON>
```

---

## Tipps:

✅ **Google Colab**: Am besten für einmalige Tests
✅ **Replit**: Am besten wenn du es öfter nutzen willst (bleibt gespeichert)
✅ Du kannst die Ausgabe kopieren und direkt an eine KI senden!

## Erkannte Daten-Typen:

- 📧 **E-Mail**: user@example.com → `<EMAIL>`
- 📞 **Telefon**: +49 123 456789 → `<TELEFON>`
- 🏠 **Adresse**: Hauptstraße 123 → `<ADRESSE>`
- 👤 **Person**: Herr Max Mustermann → Herr `<PERSON>`
- 📅 **Datum**: 15.03.2024 → `<DATUM>`
- 💳 **IBAN**: DE89... → `<IBAN>`
- 🌐 **IP**: 192.168.1.1 → `<IP-ADRESSE>`
- 🌐 **URL**: www.example.com → `<URL>`

---

## Probleme?

**Fehler beim git clone?**
- Prüfe ob die Repository-URL richtig ist
- Stelle sicher dass das Repo öffentlich ist

**Python nicht gefunden?**
- Auf Colab: Sollte immer funktionieren
- Auf Replit: Python als Template auswählen

**Eingabe funktioniert nicht?**
- Nutze die Notebook-Version mit festem Text (siehe oben)
- Oder ändere den Text direkt in `test_simple.py`
