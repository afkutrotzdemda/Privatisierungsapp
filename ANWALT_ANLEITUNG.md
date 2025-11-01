# ⚖️ Text-Anonymisierer für Anwälte

## DSGVO-konforme Anonymisierung vor KI-Nutzung

Als Anwalt müssen Sie personenbezogene Daten Ihrer Mandanten schützen. Dieses Tool anonymisiert juristische Texte **automatisch**, bevor Sie sie an KI-Systeme (ChatGPT, Claude, etc.) senden.

---

## 🚀 Schnellstart (Google Colab)

### Schritt 1: Repository laden

```python
!git clone https://github.com/afkutrotzdemda/Privatisierungsapp
%cd Privatisierungsapp
!pip install -q presidio-analyzer presidio-anonymizer
```

### Schritt 2: Anwalts-Version ausführen

```python
!python presidio_anwalt.py
```

**Fertig!** Sie sehen Beispiele mit anonymisierten juristischen Texten.

---

## ✏️ Eigenen Mandantentext anonymisieren

### Methode 1: Text direkt im Script ändern

1. Öffne `presidio_anwalt.py` in deinem Repository
2. Suche nach `DEIN_TEXT =`
3. Ersetze den Beispieltext mit deinem eigenen Text
4. Führe in Colab aus: `!python presidio_anwalt.py`

### Methode 2: In Colab-Zelle (EMPFOHLEN)

```python
# Script einmal laden (nur beim ersten Mal)
exec(open('presidio_anwalt.py').read())

# DEINEN TEXT HIER EINFÜGEN:
mein_mandantentext = """
Betreff: Mandant Dr. Max Mustermann

Sehr geehrte Damen und Herren,

im Verfahren Az. 1 Js 456/23 gegen meinen Mandanten Dr. Max Mustermann,
wohnhaft in der Hauptstraße 123, 10115 Berlin, geboren am 15.03.1980,
möchte ich folgende Unterlagen einreichen.

Kontaktdaten:
Email: max.mustermann@email.de
Tel: 0176 12345678
IBAN: DE89 3704 0044 0532 0130 00

Mit freundlichen Grüßen
"""

# Anonymisieren
anonymisiert = anonymize_text(mein_mandantentext, 'en')

print("=" * 70)
print("ANONYMISIERTER TEXT (sicher für KI):")
print("=" * 70)
print(anonymisiert)
```

---

## 🔒 Was wird erkannt und anonymisiert?

### Personenbezogene Daten

| Datentyp | Beispiel | Wird zu |
|----------|----------|---------|
| **Namen** | Max Mustermann, Dr. Schmidt, Herr Meyer | `<PERSON>` |
| **E-Mail** | anwalt@kanzlei.de | `<EMAIL>` |
| **Telefon** | 0176 12345678, +49 30 123456 | `<TELEFON>` |
| **Straßenadresse** | Hauptstraße 45 | `<ADRESSE>` |
| **PLZ/Stadt** | 10115 Berlin | `<ORT>` |
| **Geburtsdatum** | 15.03.1985 | `<DATUM>` |

### Juristische Daten

| Datentyp | Beispiel | Wird zu |
|----------|----------|---------|
| **Aktenzeichen** | Az. 1 Js 123/21, 2 C 456/20 | `<AKTENZEICHEN>` |

### Identifikationsnummern

| Datentyp | Beispiel | Wird zu |
|----------|----------|---------|
| **IBAN** | DE89 3704 0044 0532 0130 00 | `<IBAN>` |
| **Steuer-ID** | 12345678901 | `<STEUER-ID>` |
| **Sozialversicherungsnummer** | 12 345678 A 123 | `<SV-NUMMER>` |
| **Personalausweisnummer** | L123456789 | `<AUSWEIS-NR>` |
| **Kreditkarte** | 4111 1111 1111 1111 | `<KREDITKARTE>` |

### Technische Daten

| Datentyp | Beispiel | Wird zu |
|----------|----------|---------|
| **IP-Adresse** | 192.168.1.1 | `<IP-ADRESSE>` |
| **URL** | www.kanzlei.de | `<URL>` |

---

## 📋 Anwendungsbeispiele für Anwälte

### Beispiel 1: Schriftsatz anonymisieren

**Vorher:**
```
Im Verfahren Az. 1 Js 123/21 gegen Herrn Klaus Meyer,
wohnhaft Hauptstraße 45, 80331 München, geboren am 15.03.1985,
Telefon: 0176 98765432, Email: meyer@email.de
```

**Nachher:**
```
Im Verfahren <AKTENZEICHEN> gegen <PERSON>,
wohnhaft <ADRESSE>, <ORT>, geboren am <DATUM>,
Telefon: <TELEFON>, Email: <EMAIL>
```

**Dann an ChatGPT:**
```
"Kannst du diesen Text für mich rechtlich prüfen und verbessern:

Im Verfahren <AKTENZEICHEN> gegen <PERSON>,
wohnhaft <ADRESSE>, <ORT>, geboren am <DATUM>..."
```

---

### Beispiel 2: Mandantengespräch zusammenfassen

**Vorher:**
```
Mandant: Dr. Thomas Weber, Tel: +49 30 12345678
Beratung am 24.10.2023:
Thema: Kündigungsschutzklage, Az. 2 Ca 456/23
Arbeitgeber: Firma Schmidt GmbH, München
```

**Nachher:**
```
Mandant: <PERSON>, Tel: <TELEFON>
Beratung am <DATUM>:
Thema: Kündigungsschutzklage, <AKTENZEICHEN>
Arbeitgeber: Firma Schmidt GmbH, München
```

---

### Beispiel 3: Vertrag zur Prüfung an KI

**Vorher:**
```
Mietvertrag zwischen Max Mustermann (Mieter),
Hauptstraße 123, 10115 Berlin,
und Anna Schmidt (Vermieterin)
IBAN: DE89 3704 0044 0532 0130 00
```

**Nachher:**
```
Mietvertrag zwischen <PERSON> (Mieter),
<ADRESSE>, <ORT>,
und <PERSON> (Vermieterin)
IBAN: <IBAN>
```

---

## ⚠️ Wichtige Hinweise für Anwälte

### ✅ Was Sie tun sollten:

1. **Immer anonymisieren** vor KI-Nutzung
2. **Prüfen Sie den Output** - kontrollieren Sie ob alle sensiblen Daten ersetzt wurden
3. **Dokumentieren Sie** in der Akte, dass Sie Anonymisierung genutzt haben
4. **Informieren Sie ggf. Mandanten** über KI-Nutzung (auch anonymisiert)

### ❌ Was dieses Tool NICHT ersetzt:

- Ihre anwaltliche Sorgfaltspflicht
- Prüfung, ob KI-Nutzung im Einzelfall zulässig ist
- Verschlüsselung bei Übertragung
- Mandanteneinwilligung (wo erforderlich)

### 🔍 Nachkontrolle empfohlen:

Das Tool erkennt die meisten Standard-Daten. **Überprüfen Sie trotzdem:**
- Ungewöhnliche Namen (z.B. "de Silva", "van der Berg")
- Spezielle Aktenzeichen-Formate
- Firmennamen, die wie Personen klingen
- Kontext-spezifische sensible Informationen

---

## 📱 Auch auf dem Tablet nutzbar

Als Anwalt unterwegs? Google Colab funktioniert auch auf Tablets (Android/iOS)!

1. Öffne https://colab.research.google.com im Browser
2. Führe die Commands oben aus
3. Kopiere den anonymisierten Text
4. Fertig!

---

## 🔧 Für Windows (Kanzlei-PC)

Das vollständige Windows-Tool mit Hotkey (Strg+Alt+A) ist in Entwicklung.
Dann: Text kopieren → Strg+Alt+A drücken → Anonymisiert in Zwischenablage!

Siehe `README.md` für Details.

---

## 📜 Rechtsgrundlagen

Relevant für DSGVO-Compliance:
- Art. 5 DSGVO (Datenminimierung)
- Art. 25 DSGVO (Privacy by Design)
- § 203 StGB (Verschwiegenheitspflicht)
- § 43a BRAO (Verschwiegenheitspflicht Rechtsanwälte)

**Hinweis:** Dies ist keine Rechtsberatung. Konsultieren Sie bei Bedarf einen Datenschutzbeauftragten.

---

## 💡 Tipps für die Praxis

### Workflow-Integration:

```
1. Mandantentext in Word/Email schreiben
2. Text kopieren (Strg+C)
3. In Google Colab einfügen und anonymisieren
4. Anonymisierten Text an ChatGPT/Claude senden
5. KI-Antwort prüfen und in eigene Worte fassen
6. Original-Namen wieder einsetzen
```

### Zeitersparnis:

- ✅ Schriftsätze vorformulieren lassen
- ✅ Rechtliche Argumente recherchieren
- ✅ Vertragsentwürfe prüfen lassen
- ✅ Zusammenfassungen erstellen

**Aber:** Niemals KI-Output 1:1 übernehmen! Immer fachlich prüfen.

---

## 🆘 Support

Bei Fragen oder wenn bestimmte Datentypen nicht erkannt werden:
- Öffne ein Issue im GitHub Repository
- Beschreibe welche Daten nicht erkannt wurden
- Ich erweitere die Patterns entsprechend

---

## ⚖️ Haftungsausschluss

Dieses Tool dient als Hilfsmittel. Die Verantwortung für DSGVO-Compliance
und Einhaltung der anwaltlichen Verschwiegenheitspflicht liegt beim Nutzer.

Keine Gewährleistung für vollständige Anonymisierung aller Daten.
**Immer den Output manuell prüfen!**

---

**Viel Erfolg bei der DSGVO-konformen Nutzung von KI in Ihrer Kanzlei!** ⚖️
