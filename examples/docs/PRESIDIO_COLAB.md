# 🚀 Presidio auf Deutsch in Google Colab testen

## Schritt-für-Schritt Anleitung

---

### ✅ ZELLE 1: Repository laden & Presidio installieren

Kopiere das und drücke Run:

```python
!git clone https://github.com/afkutrotzdemda/Privatisierungsapp
%cd Privatisierungsapp
!pip install -q presidio-analyzer presidio-anonymizer
```

---

### ✅ ZELLE 2: Test ausführen

```python
!python presidio_test_deutsch.py
```

**Das war's!** Du siehst jetzt die Beispiele.

---

### ✅ ZELLE 3: Deinen eigenen Text testen

```python
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# Setup (nur einmal ausführen)
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# Deutsche Pattern hinzufügen
phone_patterns = [
    Pattern(name="phone_de", regex=r"\+49[\s\-]?\d{2,4}[\s\-]?\d{3,9}", score=0.7),
    Pattern(name="phone_mobile", regex=r"0\d{3,4}[\s\-]?\d{6,8}", score=0.7),
]
phone_recognizer = PatternRecognizer(
    supported_entity="PHONE_NUMBER",
    patterns=phone_patterns
)
analyzer.registry.add_recognizer(phone_recognizer)

iban_pattern = Pattern(
    name="iban_de",
    regex=r"\bDE\d{2}[\s]?\d{4}[\s]?\d{4}[\s]?\d{4}[\s]?\d{4}[\s]?\d{2}\b",
    score=0.9
)
iban_recognizer = PatternRecognizer(
    supported_entity="IBAN_CODE",
    patterns=[iban_pattern]
)
analyzer.registry.add_recognizer(iban_recognizer)

# 👉 HIER DEINEN TEXT EINFÜGEN:
mein_text = """
Max Mustermann
Email: max@example.com
Tel: 0176 123456789
IBAN: DE89 3704 0044 0532 0130 00
"""

# Anonymisieren
results = analyzer.analyze(text=mein_text, language="de")
anonymized = anonymizer.anonymize(
    text=mein_text,
    analyzer_results=results,
    operators={
        "DEFAULT": OperatorConfig("replace", {"new_value": "<ANONYMISIERT>"}),
        "PERSON": OperatorConfig("replace", {"new_value": "<PERSON>"}),
        "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "<EMAIL>"}),
        "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "<TELEFON>"}),
        "IBAN_CODE": OperatorConfig("replace", {"new_value": "<IBAN>"}),
    }
)

print("ORIGINAL:")
print(mein_text)
print("\nANONYMISIERT:")
print(anonymized.text)
```

---

## 🎯 KOMPLETT IN EINER ZELLE

Wenn du alles in einer Zelle haben willst:

```python
!git clone https://github.com/afkutrotzdemda/Privatisierungsapp
%cd Privatisierungsapp
!pip install -q presidio-analyzer presidio-anonymizer
!python presidio_test_deutsch.py
```

---

## 📝 Was erkannt wird:

- ✅ **E-Mail**: max@example.com → `<EMAIL>`
- ✅ **Telefon**: 0176 123456, +49 30 123456 → `<TELEFON>`
- ✅ **IBAN**: DE89 3704... → `<IBAN>`
- ✅ **Datum**: 15.03.2024 → `<DATUM>`
- ✅ **IP**: 192.168.1.1 → `<IP-ADRESSE>`
- ✅ **URL**: www.example.com → `<URL>`
- ✅ **Kreditkarte**: 4111 1111 1111 1111 → `<KREDITKARTE>`

---

## ❓ Fehler?

**"No module named 'presidio_analyzer'"**
→ Führe Zelle 1 nochmal aus (Presidio installieren)

**"No matching recognizers"**
→ Nutze `presidio_test_deutsch.py` (hat deutsche Pattern integriert!)

**Text wird nicht anonymisiert**
→ Probiere mit englischem Text und `language="en"`

---

## 💡 Tipp

Die Datei **`presidio_test_deutsch.py`** kannst du auch direkt bearbeiten:
1. Im Repository auf GitHub öffnen
2. Text bei `DEIN_TEXT =` ändern
3. In Colab neu ausführen
