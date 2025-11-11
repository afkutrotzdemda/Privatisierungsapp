"""
🔒 STANDALONE TEXT ANONYMISIERER
================================

Einfach diesen GESAMTEN Code kopieren und in Google Colab / Replit einfügen!
Kein git clone nötig, kein Repository nötig!

ANLEITUNG:
1. Kopiere diesen gesamten Code (Strg+A, Strg+C)
2. Gehe zu https://colab.research.google.com
3. Erstelle neue Zelle und füge ein (Strg+V)
4. Drücke "Run" oder Strg+Enter
5. Fertig!
"""

import re

def anonymize_text(text):
    """
    Anonymisiert persönliche Daten im Text

    Erkannte Typen:
    - E-Mail: user@example.com → <EMAIL>
    - Telefon: +49 123 456789 → <TELEFON>
    - IBAN: DE89 3704... → <IBAN>
    - Datum: 15.03.2024 → <DATUM>
    - IP-Adresse: 192.168.1.1 → <IP-ADRESSE>
    - URL: www.example.com → <URL>
    - Person: Herr Max Mustermann → Herr <PERSON>
    - Adresse: Hauptstraße 123 → <ADRESSE>
    """

    # E-Mail Adressen
    text = re.sub(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        '<EMAIL>',
        text
    )

    # Telefonnummern (verschiedene Formate)
    # +49 123 456789, 0176 123456, 069-12345, etc.
    text = re.sub(
        r'\+?\d{1,4}[\s\-]?\(?\d{1,4}\)?[\s\-]?\d{1,4}[\s\-]?\d{1,9}',
        '<TELEFON>',
        text
    )

    # IBAN (z.B. DE89 3704 0044 0532 0130 00)
    text = re.sub(
        r'\b[A-Z]{2}\d{2}\s?(\d{4}\s?){4}\d{2}\b',
        '<IBAN>',
        text
    )

    # Datum (15.03.2024 oder 2024-03-15)
    text = re.sub(r'\b\d{1,2}\.\d{1,2}\.\d{4}\b', '<DATUM>', text)
    text = re.sub(r'\b\d{4}-\d{2}-\d{2}\b', '<DATUM>', text)

    # IP-Adressen (192.168.1.1)
    text = re.sub(
        r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
        '<IP-ADRESSE>',
        text
    )

    # URLs (https://example.com oder www.example.com)
    text = re.sub(r'https?://[^\s]+', '<URL>', text)
    text = re.sub(r'www\.[^\s]+', '<URL>', text)

    # Personen mit Anrede (Herr Max Mustermann, Frau Dr. Weber)
    text = re.sub(
        r'\b(Herr|Frau)\s+(Dr\.\s+)?[A-Z][a-z]+\s+[A-Z][a-z]+\b',
        r'\1 <PERSON>',
        text
    )

    # Adressen (Hauptstraße 123, Müllerstraße 45a)
    text = re.sub(
        r'\b[A-ZÄÖÜ][a-zäöüß]+straße\s+\d+[a-z]?\b',
        '<ADRESSE>',
        text
    )

    return text


# ============================================================================
# BEISPIELE - Zeigt wie es funktioniert
# ============================================================================

def show_examples():
    """Zeigt Beispiele der Anonymisierung"""

    print("=" * 70)
    print("🔒 TEXT ANONYMISIERER - DEMO")
    print("=" * 70)
    print()
    print("Erkannte Daten-Typen:")
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

    examples = [
        """Hallo, ich bin Max Mustermann und wohne in der Hauptstraße 123, Berlin.
Meine E-Mail ist max.mustermann@example.com und Telefon +49 30 12345678.""",

        """Kontaktdaten:
- Name: Anna Schmidt
- Email: anna.schmidt@gmail.com
- Tel: 0176 98765432
- IBAN: DE89 3704 0044 0532 0130 00""",

        """Sehr geehrte Frau Dr. Weber,
am 24.10.2024 hat Herr Thomas Becker (IP: 192.168.1.100)
die Website www.example.com besucht."""
    ]

    for i, example in enumerate(examples, 1):
        print(f"📝 BEISPIEL {i}:")
        print("-" * 70)
        print("ORIGINAL:")
        print(example)
        print()
        print("ANONYMISIERT:")
        print(anonymize_text(example))
        print()
        print("=" * 70)
        print()


# ============================================================================
# DEINEN EIGENEN TEXT HIER TESTEN
# ============================================================================

def test_your_text():
    """Hier kannst du deinen eigenen Text testen!"""

    print("\n" + "=" * 70)
    print("✏️  TESTE DEINEN EIGENEN TEXT:")
    print("=" * 70)
    print()

    # 👉 HIER DEINEN TEXT EINFÜGEN:
    your_text = """
Max Mustermann
Email: max@example.com
Tel: +49 176 12345678
Adresse: Hauptstraße 123, München
IBAN: DE89 3704 0044 0532 0130 00
    """
    # 👆 Ersetze den Text oben mit deinem eigenen!

    print("DEIN ORIGINAL-TEXT:")
    print("-" * 70)
    print(your_text)
    print()

    print("ANONYMISIERT:")
    print("-" * 70)
    anonymized = anonymize_text(your_text)
    print(anonymized)
    print()
    print("=" * 70)
    print()
    print("✅ Kopiere den anonymisierten Text und sende ihn sicher an KIs!")
    print()


# ============================================================================
# INTERAKTIVE VERSION (für Colab/Replit mit Input)
# ============================================================================

def interactive_mode():
    """
    Interaktive Version - Gib eigenen Text ein
    (Funktioniert am besten in Colab/Replit Terminal)
    """
    print("=" * 70)
    print("🔒 INTERAKTIVER MODUS")
    print("=" * 70)
    print("Gib deinen Text ein und drücke Enter.")
    print("Zum Beenden: leere Zeile eingeben")
    print("=" * 70)
    print()

    lines = []
    print("Dein Text (Enter drücken wenn fertig):")

    try:
        while True:
            line = input()
            if not line.strip():
                break
            lines.append(line)
    except EOFError:
        pass

    if lines:
        user_text = "\n".join(lines)
        print()
        print("=" * 70)
        print("ANONYMISIERT:")
        print("=" * 70)
        print(anonymize_text(user_text))
        print("=" * 70)
    else:
        print("\n(Kein Text eingegeben)")


# ============================================================================
# HAUPTPROGRAMM
# ============================================================================

if __name__ == "__main__":
    # 1. Zeige Beispiele
    show_examples()

    # 2. Teste deinen eigenen Text (ändere den Text in der Funktion oben!)
    test_your_text()

    # 3. Optional: Interaktiver Modus (auskommentiert, aktiviere bei Bedarf)
    # Hinweis: Funktioniert nur wenn du das Script in einem Terminal ausführst
    # interactive_mode()


# ============================================================================
# SCHNELL-FUNKTION für Notebooks
# ============================================================================

def anonymize(text):
    """
    Kurz-Version zum schnellen Aufrufen in Colab-Zellen:

    >>> anonymize("Max: max@example.com, Tel: 0176 123456")
    'Max: <EMAIL>, Tel: <TELEFON>'
    """
    return anonymize_text(text)


# ============================================================================
# FERTIG!
# ============================================================================
#
# NUTZUNG:
#
# 1. In diesem Script:
#    - Ändere den Text in der Funktion test_your_text() oben
#    - Führe das gesamte Script aus
#
# 2. In neuer Colab-Zelle:
#    result = anonymize("Max: max@test.de, Tel 0176 123")
#    print(result)
#
# 3. Für die Windows-App:
#    - Siehe README.md im Repository
#    - Nutzt Microsoft Presidio (noch genauer!)
#    - Hotkey Strg+Alt+A
#
# ============================================================================
