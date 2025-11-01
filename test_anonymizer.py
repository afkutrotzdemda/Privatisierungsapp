"""
Test-Script für die Anonymisierungs-Funktion
Kann ohne Windows-spezifische Features ausgeführt werden
"""

from src.anonymizer import TextAnonymizer

# Test-Texte
test_texts = [
    """Hallo, ich bin Max Mustermann und wohne in der Hauptstraße 123, 10115 Berlin.
Meine E-Mail ist max.mustermann@example.com und meine Telefonnummer ist +49 30 12345678.
Meine IBAN ist DE89370400440532013000.""",

    """Kontaktdaten:
- Name: Anna Schmidt
- Adresse: Müllerstraße 45, München
- Email: anna.schmidt@gmail.com
- Tel: 0176 98765432
- Geburtsdatum: 15.03.1990""",

    """Sehr geehrte Frau Dr. Weber,

ich möchte Sie über folgenden Vorfall informieren. Am 24.10.2024 um 14:30 Uhr
hat Herr Thomas Becker unter der Telefonnummer 069-12345678 angerufen.
Seine IP-Adresse war 192.168.1.100 und er hat die Webseite www.example.com besucht."""
]

def main():
    print("=" * 70)
    print("TEXT ANONYMISIERUNGS-TEST")
    print("=" * 70)
    print()

    # Erstelle Anonymizer
    print("Initialisiere Text Anonymizer...")
    anonymizer = TextAnonymizer(language="de")

    print("Lade Presidio (kann beim ersten Mal etwas dauern)...")
    if not anonymizer.initialize():
        print("FEHLER: Konnte Presidio nicht initialisieren!")
        return

    print("✓ Presidio erfolgreich geladen!")
    print()

    # Teste jeden Text
    for i, text in enumerate(test_texts, 1):
        print("=" * 70)
        print(f"TEST {i}")
        print("=" * 70)
        print()
        print("ORIGINAL:")
        print("-" * 70)
        print(text)
        print()

        print("ANONYMISIERT:")
        print("-" * 70)
        anonymized = anonymizer.anonymize(text)
        print(anonymized)
        print()

    print("=" * 70)
    print("TESTS ABGESCHLOSSEN!")
    print("=" * 70)

if __name__ == "__main__":
    main()
