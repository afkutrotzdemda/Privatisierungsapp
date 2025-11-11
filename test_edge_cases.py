"""
Test: Edge Cases - E-Mails, Telefonnummern ohne Label
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from anonymizer import TextAnonymizer
import logging

logging.basicConfig(level=logging.WARNING)

def test_case(name, text, expected_keywords):
    """Testet einen Fall und prüft ob erwartet Keywords im Output sind"""
    anonymizer = TextAnonymizer(language="de")
    anonymizer.initialize()

    result = anonymizer.anonymize(text)

    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")
    print(f"INPUT:  {text}")
    print(f"OUTPUT: {result}")

    # Prüfe ob Keywords vorhanden sind
    all_found = all(keyword in result for keyword in expected_keywords)

    if all_found:
        print(f"✅ PASS - Alle erwartet Keywords gefunden: {expected_keywords}")
    else:
        missing = [k for k in expected_keywords if k not in result]
        print(f"❌ FAIL - Fehlende Keywords: {missing}")

    return all_found

def main():
    print("="*60)
    print("🧪 EDGE CASE TESTS")
    print("="*60)

    tests = [
        # E-Mail OHNE Label
        ("E-Mail ohne Label",
         "Kontaktiere mich unter max.mueller@firma.de für Details.",
         ["***@***.de"]),

        # Telefon OHNE Label
        ("Telefon ohne Label",
         "Ruf mich an: 030 12345678 oder 0171 9876543",
         ["030", "0171", "XXX"]),

        # Name OHNE direkten Kontext
        ("Name mit Komma",
         "Die Klage wurde eingereicht von Herrn Klaus Müller, der als Zeuge auftrat.",
         ["Herrn", "M."]),

        # Mehrere E-Mails im Text
        ("Mehrere E-Mails",
         "Schreib an info@firma.de oder kontakt@beispiel.com für Infos.",
         ["***@***.de", "***@***.com"]),

        # IBAN im Fließtext
        ("IBAN im Fließtext",
         "Überweise auf DE89 3704 0044 0532 0130 00 bis Freitag.",
         ["DE**"]),

        # Datum verschiedene Formate
        ("Verschiedene Datumsformate",
         "Am 15.03.2024 oder am 2024-03-15 findet der Termin statt.",
         ["XX.03.2024", "2024-03-XX"]),

        # Straße OHNE Nummer
        ("Straße mit Nummer",
         "Wir treffen uns in der Hauptstraße 42 in Berlin.",
         ["H.straße 42"]),

        # Mix: Name + E-Mail + Telefon
        ("Mix verschiedener PII",
         "Dr. Anna Schmidt (a.schmidt@test.de, 030 555-1234) hat angerufen.",
         ["Dr. S.", "***@***.de", "030", "XXX"]),
    ]

    results = []
    for name, text, expected in tests:
        passed = test_case(name, text, expected)
        results.append((name, passed))

    print("\n" + "="*60)
    print("📊 ZUSAMMENFASSUNG")
    print("="*60)

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\n{passed_count}/{total_count} Tests bestanden ({passed_count*100//total_count}%)")

    if passed_count == total_count:
        print("\n🎉 ALLE TESTS BESTANDEN!")
    else:
        print(f"\n⚠️  {total_count - passed_count} Tests fehlgeschlagen!")

if __name__ == '__main__':
    main()
