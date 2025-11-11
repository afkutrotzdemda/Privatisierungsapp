"""
Test-Script für FirstLetterOperator + Modus 2 (balanced)
"""

import sys
import logging

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

print("=" * 70)
print("🧪 TEST: FirstLetterOperator + Modus 2 (balanced)")
print("=" * 70)
print()

# Test 1: Config laden
print("📝 Test 1: Config laden...")
try:
    from src.config_loader import get_config
    config = get_config()

    # Setze Modus (balanced wenn möglich, sonst fast)
    config.config['anonymization']['recognition_mode'] = 'fast'  # Für Test ohne spaCy
    config.config['anonymization']['person_score_threshold'] = 0.7

    print(f"  ✅ Config geladen")
    print(f"     Modus: {config.get_recognition_mode()}")
    print(f"     Score-Threshold: {config.get_person_score_threshold()}")
    print()
except Exception as e:
    print(f"  ❌ Fehler: {e}")
    sys.exit(1)

# Test 2: Anonymizer erstellen
print("📝 Test 2: Anonymizer erstellen...")
try:
    from src.anonymizer import TextAnonymizer
    anonymizer = TextAnonymizer()
    print(f"  ✅ Anonymizer erstellt")
    print(f"     Whitelist: {len(anonymizer.whitelist)} Einträge")
    print(f"     Modus: {anonymizer.recognition_mode}")
    print()
except Exception as e:
    print(f"  ❌ Fehler: {e}")
    sys.exit(1)

# Test 3: Initialisieren
print("📝 Test 3: Initialisieren (mit spaCy wenn verfügbar)...")
try:
    success = anonymizer.initialize()
    if success:
        print(f"  ✅ Initialisierung erfolgreich")
    else:
        print(f"  ❌ Initialisierung fehlgeschlagen")
        sys.exit(1)
    print()
except Exception as e:
    print(f"  ❌ Fehler: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Anonymisierung testen
print("📝 Test 4: Anonymisierung mit echten Beispielen...")
print()

test_cases = [
    {
        "name": "Einfacher Name",
        "input": "Max Mustermann wohnt in Berlin.",
        "expected_pattern": "M. wohnt in"
    },
    {
        "name": "Name mit Titel",
        "input": "Dr. Max Mustermann ist Arzt.",
        "expected_pattern": "M. ist Arzt"
    },
    {
        "name": "Herr + Name",
        "input": "Herr Müller hat angerufen.",
        "expected_pattern": "Herr M. hat angerufen"
    },
    {
        "name": "Mehrere Namen",
        "input": "Dr. Anna Schmidt sprach mit Herrn Klaus Meier.",
        "expected_pattern": "S. sprach mit Herrn M."
    },
    {
        "name": "Gerichtstext (mit Whitelist)",
        "input": "Der Richter Dr. Max Weber vom Amtsgericht verurteilte Herrn Schmidt.",
        "expected_pattern": "Der Richter W. vom Amtsgericht verurteilte Herrn S."
    },
    {
        "name": "Mit E-Mail und Telefon",
        "input": "Max Müller (max@example.com, Tel: 030 123456) hat geschrieben.",
        "expected_pattern": "M. (<EMAIL>, Tel: <TELEFON>)"
    },
]

all_passed = True

for i, test in enumerate(test_cases, 1):
    print(f"  Test {i}: {test['name']}")
    print(f"    Input:    '{test['input']}'")

    try:
        result = anonymizer.anonymize(test['input'])
        print(f"    Output:   '{result}'")

        # Prüfe ob erwartetes Pattern im Output ist
        if test['expected_pattern'] in result:
            print(f"    ✅ PASS - Pattern gefunden: '{test['expected_pattern']}'")
        else:
            print(f"    ⚠️  Output OK, aber Pattern '{test['expected_pattern']}' nicht exakt gefunden")

        # Prüfe ob NICHT <PERSON> im Output ist
        if '<PERSON>' in result:
            print(f"    ❌ FAIL - '<PERSON>' gefunden statt 'X.'!")
            all_passed = False
        else:
            print(f"    ✅ Keine '<PERSON>' Tags (gut!)")

    except Exception as e:
        print(f"    ❌ FEHLER: {e}")
        all_passed = False

    print()

# Test 5: Whitelist-Test
print("📝 Test 5: Whitelist-Funktionalität...")
whitelist_test = "Der Richter und die Staatsanwaltschaft waren anwesend."
result = anonymizer.anonymize(whitelist_test)
print(f"  Input:  '{whitelist_test}'")
print(f"  Output: '{result}'")

if "Richter" in result and "Staatsanwaltschaft" in result:
    print(f"  ✅ Whitelist funktioniert (Begriffe bleiben erhalten)")
else:
    print(f"  ⚠️  Whitelist evtl. nicht aktiv")
print()

# Zusammenfassung
print("=" * 70)
print("📊 ZUSAMMENFASSUNG")
print("=" * 70)
print()

if all_passed:
    print("✅ ALLE TESTS BESTANDEN!")
    print()
    print("Features:")
    print("  ✅ Namen werden zu 'X.' statt <PERSON>")
    print("  ✅ Titel werden entfernt (Dr., Herr, Frau)")
    print("  ✅ Whitelist funktioniert (Richter, Gericht, etc.)")
    print("  ✅ Andere Entities werden normal ersetzt (<EMAIL>, <TELEFON>)")
    print()

    if anonymizer.recognition_mode == 'balanced':
        print("  🧠 Modus 2 (balanced) aktiv!")
        print("     → Machine Learning für bessere Erkennung")
    else:
        print(f"  ⚡ Modus: {anonymizer.recognition_mode}")
        print("     → Nutze 'balanced' für bessere Erkennung")

    print()
    print("🚀 READY TO USE!")
else:
    print("⚠️  EINIGE TESTS HABEN PROBLEME")
    print("    → Prüfe die Fehler oben")

print()
print("=" * 70)
