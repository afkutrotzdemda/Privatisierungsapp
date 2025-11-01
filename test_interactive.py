"""
Interaktive Test-Version für Google Colab / Replit
Du kannst eigenen Text eingeben und sofort das anonymisierte Ergebnis sehen!
"""

import re

def anonymize_text(text):
    """
    Anonymisiert Text mit Regex-Patterns
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

    # Namen (Herr/Frau + evtl. Titel + Name)
    text = re.sub(r'\b(Herr|Frau)\s+(Dr\.\s+)?[A-Z][a-z]+\s+[A-Z][a-z]+\b', r'\1 <PERSON>', text)

    # Adressen (Straße + Nummer)
    text = re.sub(r'\b[A-ZÄÖÜ][a-zäöüß]+straße\s+\d+[a-z]?\b', '<ADRESSE>', text)

    return text


def main():
    print("=" * 70)
    print("🔒 TEXT ANONYMISIERER - Interaktive Version")
    print("=" * 70)
    print()
    print("Füge deinen Text ein und drücke Enter.")
    print("Zum Beenden: leere Zeile oder 'exit' eingeben")
    print()
    print("Erkannte Typen:")
    print("  📧 E-Mail → <EMAIL>")
    print("  📞 Telefon → <TELEFON>")
    print("  🏠 Adresse → <ADRESSE>")
    print("  👤 Person → <PERSON>")
    print("  📅 Datum → <DATUM>")
    print("  💳 IBAN → <IBAN>")
    print("  🌐 IP/URL → <IP-ADRESSE>, <URL>")
    print()
    print("=" * 70)
    print()

    # Zeige erst ein Beispiel
    example = """Max Mustermann, max@example.com, +49 123 456789
Hauptstraße 123, Berlin"""

    print("📝 BEISPIEL:")
    print("-" * 70)
    print("Original:")
    print(example)
    print()
    print("Anonymisiert:")
    print(anonymize_text(example))
    print()
    print("=" * 70)
    print()

    # Interaktive Schleife
    while True:
        print("Gib deinen Text ein (oder 'exit' zum Beenden):")
        print()

        # Mehrzeilige Eingabe sammeln
        lines = []
        print("(Drücke zweimal Enter wenn fertig)")
        empty_count = 0

        while True:
            try:
                line = input()
                if line.lower() == 'exit':
                    print("\n👋 Auf Wiedersehen!")
                    return

                if not line.strip():
                    empty_count += 1
                    if empty_count >= 1:  # Nach einer leeren Zeile aufhören
                        break
                else:
                    empty_count = 0
                    lines.append(line)

            except EOFError:
                break

        if not lines:
            print("\n👋 Auf Wiedersehen!")
            break

        user_text = "\n".join(lines)

        print()
        print("=" * 70)
        print("🔒 ANONYMISIERT:")
        print("=" * 70)
        anonymized = anonymize_text(user_text)
        print(anonymized)
        print()
        print("=" * 70)
        print()


if __name__ == "__main__":
    main()
