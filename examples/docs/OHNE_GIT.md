# 🚀 Nutzung OHNE Git Clone (für private Repositories)

## Problem

Wenn dein Repository **privat** ist, funktioniert `git clone` nicht ohne Login.

## Lösung: Standalone Version

Nutze die **Standalone-Datei** die KEINEN Clone braucht!

---

## ✨ Option 1: Copy & Paste (EINFACHSTE METHODE)

### Für Google Colab:

1. **Öffne die Datei** `standalone_anonymizer.py` in GitHub
   - Gehe zu deinem Repository
   - Klick auf `standalone_anonymizer.py`
   - Klick auf "Raw" (oben rechts)

2. **Kopiere den gesamten Code** (Strg+A, Strg+C)

3. **Gehe zu Google Colab**: https://colab.research.google.com

4. **Erstelle neue Zelle** und füge den Code ein (Strg+V)

5. **Drücke Run** ▶️

6. **Fertig!** Du siehst sofort die Beispiele

### Eigenen Text testen:

Ändere in der Datei die Zeile bei `your_text =`:

```python
your_text = """
HIER DEINEN TEXT EINFÜGEN
"""
```

---

## 📱 Option 2: Direkt in Colab schreiben (NOCH KÜRZER)

Kopiere einfach diesen Code in eine Colab-Zelle:

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

# DEINEN TEXT HIER:
mein_text = """
Max Mustermann
Email: max@example.com
Tel: 0176 123 456 789
Adresse: Hauptstraße 123
"""

print("ORIGINAL:")
print(mein_text)
print("\nANONYMISIERT:")
print(anonymize(mein_text))
```

Fertig! Drücke Run und sieh das Ergebnis!

---

## 🌐 Option 3: Repository öffentlich machen (wenn möglich)

Falls du das Repository später doch öffentlich machen möchtest:

1. Gehe zu deinem GitHub Repository
2. Klick auf **Settings**
3. Ganz unten: **Change visibility**
4. Wähle **Public**

Dann funktioniert auch `git clone` ohne Login.

⚠️ **ACHTUNG**: Nur öffentlich machen wenn keine sensiblen Daten drin sind!

---

## 💾 Option 4: Replit Upload

Für Replit:

1. Gehe zu https://replit.com
2. "Create Repl" → "Python"
3. **Upload Files** (Drag & Drop)
   - Lade `standalone_anonymizer.py` hoch
4. Klick auf Run

---

## Zusammenfassung

| Methode | Vorteile | Repository |
|---------|----------|------------|
| **Copy & Paste** | Am schnellsten | Kann privat bleiben |
| **Mini-Code** | Nur 10 Zeilen | Braucht kein Repo |
| **Public machen** | git clone möglich | Muss öffentlich sein |
| **Replit Upload** | Bleibt gespeichert | Kann privat bleiben |

**Empfehlung**: Nutze **Copy & Paste** mit `standalone_anonymizer.py`!

---

## ✅ Das funktioniert garantiert:

```python
# Kopiere einfach DAS hier in Google Colab:

import re

def anonymize(text):
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '<EMAIL>', text)
    text = re.sub(r'\+?\d{1,4}[\s\-]?\(?\d{1,4}\)?[\s\-]?\d{1,4}[\s\-]?\d{1,9}', '<TELEFON>', text)
    text = re.sub(r'\b[A-ZÄÖÜ][a-zäöüß]+straße\s+\d+[a-z]?\b', '<ADRESSE>', text)
    return text

# Test:
print(anonymize("Max: max@test.de, Tel: 0176 123, Hauptstraße 45"))
```

**Output:**
```
Max: <EMAIL>, Tel: <TELEFON>, <ADRESSE>
```

🎉 **Es funktioniert sofort - kein Repository nötig!**
