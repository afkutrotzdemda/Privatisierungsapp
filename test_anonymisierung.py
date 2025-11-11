"""
Test-Script: Anonymisierung von Anwaltsschreiben

Testet alle Custom Operators mit realem Anwaltsschreiben
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from anonymizer import TextAnonymizer
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    print("=" * 80)
    print("🧪 TEST: Anonymisierung von Anwaltsschreiben")
    print("=" * 80)
    print()

    # Lade Test-Text
    print("📄 Lade Test-Datei...")
    with open('test_anwaltsschreiben.txt', 'r', encoding='utf-8') as f:
        original_text = f.read()

    print(f"   Länge: {len(original_text)} Zeichen")
    print()

    # Erstelle Anonymizer
    print("🔧 Initialisiere Anonymizer...")
    anonymizer = TextAnonymizer(language="de")

    if not anonymizer.initialize():
        print("❌ Fehler beim Initialisieren!")
        return

    print("✅ Anonymizer bereit")
    print()

    # Anonymisiere
    print("🔒 Anonymisiere Text...")
    anonymized_text = anonymizer.anonymize(original_text)

    print(f"   Länge nach Anonymisierung: {len(anonymized_text)} Zeichen")
    print()

    # Speichere Ergebnis
    output_file = 'test_anonymisiert.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(anonymized_text)

    print(f"✅ Anonymisierter Text gespeichert: {output_file}")
    print()

    # Zeige Vorher/Nachher Beispiele
    print("=" * 80)
    print("📊 BEISPIELE (Vorher → Nachher)")
    print("=" * 80)
    print()

    examples = [
        ("Dr. Markus Schmidt", "Namen mit Titel"),
        ("Hauptstraße 123", "Straßenadressen"),
        ("10115 Berlin", "PLZ + Stadt"),
        ("Tel: 030 12345678", "Telefonnummern"),
        ("m.schmidt@kanzlei-schmidt.de", "E-Mail Adressen"),
        ("Az.: 123 C 456/2024", "Aktenzeichen"),
        ("15. März 2024", "Datum"),
        ("DE89 3704 0044 0532 0130 00", "IBAN"),
        ("Herr\nMax Mustermann", "Empfänger"),
        ("Frau Dr. Anna Weber", "Mandantin"),
    ]

    for search_text, description in examples:
        if search_text in original_text:
            # Finde Position im Original
            start = original_text.find(search_text)
            end = start + len(search_text)

            # Finde ungefähre Position im anonymisierten Text
            # (kann durch Längenänderungen verschoben sein)
            context_before = original_text[max(0, start-20):start]
            context_start = anonymized_text.find(context_before)

            if context_start != -1:
                # Suche nach dem nächsten Wort nach dem Kontext
                anon_start = context_start + len(context_before)
                # Nimm die nächsten 30 Zeichen
                anon_snippet = anonymized_text[anon_start:anon_start+50].split('\n')[0].strip()

                print(f"📌 {description}:")
                print(f"   Vorher:  '{search_text}'")
                print(f"   Nachher: '{anon_snippet}'")
                print()

    print("=" * 80)
    print("✅ TEST ABGESCHLOSSEN!")
    print("=" * 80)
    print()
    print(f"Vollständiger anonymisierter Text: {output_file}")
    print()

if __name__ == '__main__':
    main()
