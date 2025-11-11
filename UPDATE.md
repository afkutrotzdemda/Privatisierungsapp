# 🔄 Automatische Updates

## Methode 1: Automatisches Update-Script (Empfohlen)

### Schnell-Update:
```
update.bat
```

Das wars! Das Script:
- ✅ Prüft auf neue Updates von GitHub
- ✅ Zeigt dir was sich geändert hat
- ✅ Fragt dich ob du updaten willst
- ✅ Aktualisiert Python-Pakete falls nötig
- ✅ Startet die App neu

---

## Methode 2: Auf Updates prüfen (ohne zu installieren)

```
python check_updates.py
```

Zeigt nur ob Updates verfügbar sind, installiert sie aber nicht.

---

## Methode 3: Manuelles Update (für Fortgeschrittene)

```bash
git pull origin claude/text-anonymizer-windows-011CUh7Aet7jbkUi7Jhd9gEG
pip install -r requirements.txt --upgrade
```

---

## Was passiert beim Update?

### ✅ Das wird aktualisiert:
- Alle Code-Dateien (src/*.py)
- Batch-Scripts (start.bat, wechsel_modus.bat, etc.)
- Python-Pakete (wenn requirements.txt geändert wurde)

### ❌ Das bleibt erhalten:
- Deine config.toml Einstellungen (außer wenn config.toml selbst geändert wurde)
- Deine Whitelist
- Log-Dateien

---

## Troubleshooting

### Problem: "Du hast lokale Änderungen"
**Lösung:** Das Script fragt dich ob du sie verwerfen willst.

**Alternative:** Manuell resetten:
```bash
git reset --hard HEAD
git pull
```

### Problem: "Konnte nicht mit GitHub verbinden"
**Mögliche Ursachen:**
- Keine Internetverbindung
- GitHub ist down
- Firewall blockiert Git

**Lösung:**
1. Prüfe deine Internetverbindung
2. Versuche es später nochmal

### Problem: "requirements.txt konnte nicht aktualisiert werden"
**Lösung:** Manuell installieren:
```bash
pip install presidio-analyzer presidio-anonymizer --upgrade
```

---

## Update-Benachrichtigung beim Start (Optional)

Du kannst die App so einstellen, dass sie beim Start automatisch auf Updates prüft.

**Bearbeite `main.py`** und füge am Anfang von `start()` hinzu:
```python
from check_updates import check_for_updates

# Prüfe auf Updates (leise)
updates_available, count, _ = check_for_updates(silent=True)
if updates_available:
    print(f"✨ {count} Update(s) verfügbar! Führe 'update.bat' aus.")
```

---

## Fragen?

- Problem mit Update? Öffne ein Issue auf GitHub
- Willst du zur vorherigen Version zurück? Nutze: `git checkout <commit-hash>`
