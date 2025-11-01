"""
Einfacher Test der zeigt wie die Anonymisierung funktionieren würde
(Ohne tatsächlich Presidio zu laden - für Demo-Zwecke)
"""

import re

def simple_anonymize(text):
    """
    Einfache Regex-basierte Anonymisierung zu Demonstrationszwecken
    (Die echte Presidio-Version ist viel genauer!)
    """

    # E-Mail Adressen
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '<EMAIL>', text)

    # Telefonnummern (verschiedene Formate)
    text = re.sub(r'\+?\d{1,4}[\s\-]?\(?\d{1,4}\)?[\s\-]?\d{1,4}[\s\-]?\d{1,9}', '<TELEFON>', text)

    # IBAN
    text = re.sub(r'\b[A-Z]{2}\d{2}\s?(\d{4}\s?){4}\d{2}\b', '<IBAN>', text)

    # Datum (verschiedene Formate)
    text = re.sub(r'\b\d{1,2}\.\d{1,2}\.\d{4}\b', '<DATUM>', text)
    text = re.sub(r'\b\d{4}-\d{2}-\d{2}\b', '<DATUM>', text)

    # IP-Adressen
    text = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '<IP-ADRESSE>', text)

    # URLs
    text = re.sub(r'https?://[^\s]+', '<URL>', text)
    text = re.sub(r'www\.[^\s]+', '<URL>', text)

    # Einfache Namen (Herr/Frau + Titel + Name)
    text = re.sub(r'\b(Herr|Frau)\s+(Dr\.\s+)?[A-Z][a-z]+\s+[A-Z][a-z]+\b', r'\1 <PERSON>', text)

    # Adressen (Straße + Nummer)
    text = re.sub(r'\b[A-ZÄÖÜ][a-zäöüß]+straße\s+\d+[a-z]?\b', '<ADRESSE>', text)

    return text


# Test-Texte
test_texts = [
    """Hallo, ich bin Max Mustermann und wohne in der Hauptstraße 123, 10115 Berlin.
Meine E-Mail ist max.mustermann@example.com und meine Telefonnummer ist +49 30 12345678.
Meine IBAN ist DE89 3704 0044 0532 0130 00.""",

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
    print("ANONYMISIERUNGS-DEMO (Vereinfachte Version)")
    print("=" * 70)
    print()
    print("⚠️  HINWEIS: Dies ist eine vereinfachte Demo mit Regex.")
    print("   Die echte Windows-App nutzt Microsoft Presidio und ist")
    print("   deutlich genauer!")
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
        anonymized = simple_anonymize(text)
        print(anonymized)
        print()

    print("=" * 70)
    print("✓ DEMO ABGESCHLOSSEN!")
    print("=" * 70)
    print()
    print("Die Windows-App funktioniert genauso, nur mit besserer KI-Erkennung!")

if __name__ == "__main__":
    main()
