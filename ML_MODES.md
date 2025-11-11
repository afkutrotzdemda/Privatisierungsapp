# 🧠 Machine Learning Modus aktivieren

## 📋 **Übersicht**

Anonymify hat **3 Modi** für die Erkennung:

| Modus | Geschwindigkeit | Genauigkeit | Installation |
|-------|----------------|-------------|--------------|
| **fast** | ⚡ ~0.1s | ⭐⭐⭐ | Standard, keine zusätzlichen Pakete |
| **balanced** | 🏃 ~1s | ⭐⭐⭐⭐ | Benötigt spaCy (klein) |
| **accurate** | 🐌 ~2-5s | ⭐⭐⭐⭐⭐ | Benötigt spaCy (groß) |

---

## ⚡ **Modus 1: fast (Standard)**

### Was macht es?
- Nur Pattern-Matching (Regex)
- Kein Machine Learning
- Super schnell (~0.1 Sekunden)
- Gut für Echtzeit-Nutzung

### Nachteile:
- ❌ Mehr False Positives
- ❌ "Der Richter" könnte als Name erkannt werden

### Aktivieren:
```toml
# config.toml
[anonymization]
recognition_mode = "fast"  # Standard
```

---

## 🏃 **Modus 2: balanced (Empfohlen für mehr Genauigkeit)**

### Was macht es?
- Pattern-Matching + leichtes ML (spaCy small)
- Named Entity Recognition (NER)
- Mittlere Geschwindigkeit (~1 Sekunde)
- Viel weniger False Positives

### Vorteile:
- ✅ Erkennt "Max Müller" als Person
- ✅ Ignoriert "Der Richter" (Beruf, kein Name)
- ✅ Noch brauchbar für Echtzeit

### Installation:
```bash
# 1. spaCy installieren
pip install spacy

# 2. Kleines deutsches Modell laden
python -m spacy download de_core_news_sm
```

### Aktivieren:
```toml
# config.toml
[anonymization]
recognition_mode = "balanced"
```

---

## 🧠 **Modus 3: accurate (Maximum Precision)**

### Was macht es?
- Pattern-Matching + großes ML-Modell
- Bestes Named Entity Recognition
- Langsam (~2-5 Sekunden)
- Fast keine False Positives

### Vorteile:
- ✅✅✅ Sehr präzise Erkennung
- ✅✅✅ Minimale False Positives
- ✅✅✅ Versteht Kontext

### Nachteile:
- ❌ Langsam (2-5 Sekunden)
- ❌ Größeres Modell (~100 MB)

### Installation:
```bash
# 1. spaCy installieren
pip install spacy

# 2. GROßES deutsches Modell laden
python -m spacy download de_core_news_lg
```

### Aktivieren:
```toml
# config.toml
[anonymization]
recognition_mode = "accurate"
```

---

## 🎯 **Welchen Modus soll ich nutzen?**

### **Du hast viele False Positives** (6000 → 2000 Zeichen)
```
→ Nutze "balanced" oder "accurate"
→ Installiere spaCy
→ Teste mit balanced zuerst
```

### **Du willst Echtzeit-Feedback**
```
→ Bleibe bei "fast"
→ Erhöhe Score-Thresholds stattdessen:

[anonymization]
recognition_mode = "fast"
person_score_threshold = 0.8  # Strenger
```

### **Du hast Zeit und willst perfekte Ergebnisse**
```
→ Nutze "accurate"
→ Warte 2-5 Sekunden pro Text
→ Fast keine False Positives mehr
```

---

## 📊 **Beispiel-Vergleich**

### Test-Text:
```
"Der Richter Dr. Max Mustermann sprach das Urteil.
Die Staatsanwaltschaft Hamburg klagt an."
```

### **Modus: fast**
```
Ergebnis:
"<PERSON> <PERSON> <PERSON> sprach das Urteil.
<PERSON> Hamburg klagt an."

False Positives: 3 ("Der Richter", "Die Staatsanwaltschaft")
Zeit: 0.1s
```

### **Modus: balanced**
```
Ergebnis:
"Der Richter <PERSON> sprach das Urteil.
Die Staatsanwaltschaft Hamburg klagt an."

False Positives: 0
Zeit: 1.2s
```

### **Modus: accurate**
```
Ergebnis:
"Der Richter <PERSON> sprach das Urteil.
Die Staatsanwaltschaft Hamburg klagt an."

False Positives: 0
Zeit: 3.5s
```

---

## 💡 **Kombination: Beste Einstellungen**

### **Für Anwälte (Dokumente prüfen)**
```toml
[anonymization]
recognition_mode = "accurate"        # Beste Genauigkeit
person_score_threshold = 0.7         # Standard OK
```

### **Für Echtzeit (schnell tippen)**
```toml
[anonymization]
recognition_mode = "fast"            # Schnell
person_score_threshold = 0.8         # Strenger Threshold
```

### **Für Balance (beste Balance)**
```toml
[anonymization]
recognition_mode = "balanced"        # Mittelweg
person_score_threshold = 0.7         # Standard
```

---

## 🚀 **Installation & Test**

### **Schritt 1: spaCy installieren**
```bash
# In Projekt-Ordner:
call venv\Scripts\activate.bat

# Installiere spaCy
pip install spacy

# Lade deutsches Modell
python -m spacy download de_core_news_sm

# Optional: Großes Modell für "accurate"
python -m spacy download de_core_news_lg
```

### **Schritt 2: config.toml bearbeiten**
```toml
[anonymization]
recognition_mode = "balanced"  # Ändere hier!
```

### **Schritt 3: App neu starten**
```bash
# App beenden
Rechtsklick Icon → Beenden

# Neu starten
Rechtsklick start.bat → "Als Administrator ausführen"
```

### **Schritt 4: Im Log prüfen**
```
Schaue in anonymizer.log:

[INFO] Erkennungs-Modus: balanced
[INFO] Versuche spaCy zu laden für Modus 'balanced'...
[INFO] spaCy NLP Engine geladen: de_core_news_sm
```

---

## ❓ **Troubleshooting**

### **"Konnte spaCy nicht laden"**
```
Problem: spaCy nicht installiert
Lösung:
  pip install spacy
  python -m spacy download de_core_news_sm
```

### **"Großes Modell nicht gefunden"**
```
Problem: de_core_news_lg fehlt für "accurate"
Lösung:
  python -m spacy download de_core_news_lg
Oder:
  Nutze "balanced" statt "accurate"
```

### **"Dauert zu lange"**
```
Problem: Modus zu langsam
Lösung:
  1. Wechsel von "accurate" → "balanced"
  2. Oder von "balanced" → "fast"
  3. Erhöhe stattdessen person_score_threshold auf 0.8
```

---

## 📝 **Zusammenfassung**

**Problem:** Zu viele False Positives (6000 → 2000 Zeichen)

**Lösungen:**
1. ⚡ **Schnell:** Bleibe bei "fast", erhöhe Threshold auf 0.8
2. 🏃 **Mittel:** Nutze "balanced" mit spaCy (EMPFOHLEN!)
3. 🧠 **Langsam:** Nutze "accurate" mit großem Modell

**Installation:**
```bash
pip install spacy
python -m spacy download de_core_news_sm
```

**Aktivieren:**
```toml
# config.toml
[anonymization]
recognition_mode = "balanced"
```

---

**Viel Erfolg!** 🚀
