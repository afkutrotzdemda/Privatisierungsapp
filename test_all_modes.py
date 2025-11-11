"""
TEST: Alle 3 Modi (Fast, Balanced, Accurate) mit Zeit-Messung
"""

import sys, time
sys.path.insert(0, 'src')
from anonymizer import TextAnonymizer
import logging

def test_mode(mode_name, text):
    """Testet einen Modus mit Zeit-Messung"""
    print("="*70)
    print(f"🧪 TEST: {mode_name.upper()} MODUS")
    print("="*70)
    print()

    # Setze Modus
    import os
    with open('config.toml', 'r') as f:
        config = f.read()

    config = config.replace('recognition_mode = "fast"', f'recognition_mode = "{mode_name}"')
    config = config.replace('recognition_mode = "balanced"', f'recognition_mode = "{mode_name}"')
    config = config.replace('recognition_mode = "accurate"', f'recognition_mode = "{mode_name}"')

    with open('config.toml', 'w') as f:
        f.write(config)

    # Erstelle neuen Anonymizer (damit Modus neu geladen wird)
    anonymizer = TextAnonymizer()
    anonymizer.initialize()

    # Anonymisiere
    start = time.time()
    result = anonymizer.anonymize(text)
    total_time = time.time() - start

    # Speichere
    with open(f'test_notarschreiben_{mode_name}.txt', 'w', encoding='utf-8') as f:
        f.write(result)

    # Check Namen
    checks = [
        ("Herr Maximilian Josef Müller-Hoffmann", "Herr M."),
        ("Frau Dr. med. Anna-Maria Müller-Hoffmann", "Frau Dr. med. M."),
        ("Herr Prof. Dr. Klaus-Dieter Schneider", "Herr Prof. Dr. S."),
        ("Dr. Heinrich Weber", "Dr. W."),
        ("Herr Thomas Wagner", "Herr W."),
    ]

    print("📊 NAMEN-CHECK:")
    anonymized_count = 0
    for original, expected in checks:
        if original in text:
            if original not in result and expected in result:
                print(f"  ✅ {original[:35]:35} → {expected}")
                anonymized_count += 1
            elif original not in result:
                print(f"  ⚠️  {original[:35]:35} → (erkannt, aber Muster nicht gefunden)")
                anonymized_count += 1
            else:
                print(f"  ❌ {original[:35]:35} → NICHT anonymisiert!")

    print()
    print(f"⏱️  ZEIT: {total_time:.3f}s")
    print(f"📈 NAMEN: {anonymized_count}/{len([c for c in checks if c[0] in text])} anonymisiert")
    print()

    return {
        'mode': mode_name,
        'time': total_time,
        'anonymized': anonymized_count,
        'result_length': len(result),
    }

def main():
    logging.basicConfig(level=logging.WARNING)

    print("="*70)
    print("🎯 VERGLEICH: ALLE MODI MIT ZEIT-MESSUNG")
    print("="*70)
    print()

    # Lade Test-Text
    with open('test_notarschreiben.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    print(f"📄 Notarschreiben: {len(text)} Zeichen")
    print()

    # Teste alle Modi
    results = []
    modes_to_test = ['fast']  # Standard: nur fast

    # Prüfe ob spaCy verfügbar ist
    try:
        import spacy
        try:
            spacy.load('de_core_news_sm')
            modes_to_test.append('balanced')
            print("[✓] spaCy small model gefunden - BALANCED wird getestet")
        except:
            print("[!] spaCy small model nicht gefunden - BALANCED wird übersprungen")
            print("    Installiere mit: python -m spacy download de_core_news_sm")

        try:
            spacy.load('de_core_news_lg')
            modes_to_test.append('accurate')
            print("[✓] spaCy large model gefunden - ACCURATE wird getestet")
        except:
            print("[!] spaCy large model nicht gefunden - ACCURATE wird übersprungen")
            print("    Installiere mit: python -m spacy download de_core_news_lg")
    except ImportError:
        print("[!] spaCy nicht installiert - nur FAST wird getestet")
        print("    Installiere mit: pip install spacy")

    print()

    for mode in modes_to_test:
        result = test_mode(mode, text)
        results.append(result)

    # Vergleich
    print("="*70)
    print("📊 VERGLEICH")
    print("="*70)
    print()
    print(f"{'Modus':<12} {'Zeit':>10} {'Namen':>10} {'Länge':>10}")
    print("-"*70)
    for r in results:
        print(f"{r['mode']:<12} {r['time']:>9.3f}s {r['anonymized']:>10} {r['result_length']:>10}")

    print()
    print("✅ TEST ABGESCHLOSSEN!")
    print()

if __name__ == '__main__':
    main()
