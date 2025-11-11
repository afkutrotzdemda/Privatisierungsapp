"""
Presidio Test für DEUTSCH - Funktioniert OHNE spaCy!
Nutzt nur Pattern-basierte Erkennung.
"""

from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

print("=" * 70)
print("🔒 PRESIDIO TEXT ANONYMISIERER - DEUTSCH")
print("=" * 70)
print()

# Initialisiere Presidio OHNE Sprachmodelle
print("⏳ Initialisiere Presidio (Pattern-basiert, kein spaCy nötig)...")

# Erstelle einen Dummy NLP Engine der nichts tut
class DummyNlpEngine(NlpEngine):
    def process_text(self, text, language):
        # Gibt leeres NLP result zurück - wir brauchen kein NLP!
        from presidio_analyzer.nlp_engine import NlpArtifacts
        return NlpArtifacts([], [], [], [], None, language)

    def process_batch(self, texts, language, **kwargs):
        return [self.process_text(text, language) for text in texts]

    def is_loaded(self):
        return True

    def is_loaded_from_file(self):
        return False

    def load(self):
        pass

    def get_supported_languages(self):
        return ["de", "en"]

    def get_supported_entities(self):
        return []

    def is_stopword(self, word, language):
        return False

    def is_punct(self, word, language):
        return False

# Erstelle leere Registry (OHNE predefined recognizers die spaCy brauchen!)
registry = RecognizerRegistry()
# Wir fügen manuell nur die Pattern-basierten hinzu

# Füge Pattern-Recognizer hinzu (funktioniert OHNE spaCy!)
print("⏳ Füge Erkennungsmuster hinzu...")

# E-Mail Recognizer
email_pattern = Pattern(
    name="email",
    regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    score=0.8
)
email_recognizer = PatternRecognizer(
    supported_entity="EMAIL_ADDRESS",
    patterns=[email_pattern],
    context=["email", "e-mail", "mail"],
    supported_language="en"
)
registry.add_recognizer(email_recognizer)

# Credit Card Recognizer
credit_card_pattern = Pattern(
    name="credit_card",
    regex=r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b",
    score=0.7
)
credit_card_recognizer = PatternRecognizer(
    supported_entity="CREDIT_CARD",
    patterns=[credit_card_pattern],
    context=["kreditkarte", "credit", "card", "visa", "mastercard"],
    supported_language="en"
)
registry.add_recognizer(credit_card_recognizer)

# IP Address Recognizer
ip_pattern = Pattern(
    name="ip_address",
    regex=r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    score=0.7
)
ip_recognizer = PatternRecognizer(
    supported_entity="IP_ADDRESS",
    patterns=[ip_pattern],
    context=["ip", "adresse", "address"],
    supported_language="en"
)
registry.add_recognizer(ip_recognizer)

# URL Recognizer
url_patterns = [
    Pattern(name="url_http", regex=r"https?://[^\s]+", score=0.8),
    Pattern(name="url_www", regex=r"www\.[^\s]+", score=0.7),
]
url_recognizer = PatternRecognizer(
    supported_entity="URL",
    patterns=url_patterns,
    context=["url", "website", "webseite", "link"],
    supported_language="en"
)
registry.add_recognizer(url_recognizer)

# Deutscher Telefon-Recognizer
phone_patterns = [
    Pattern(name="phone_de_mobile", regex=r"0\d{3,4}[\s\-/]?\d{3,4}[\s\-/]?\d{3,4}", score=0.7),
    Pattern(name="phone_de_intl", regex=r"\+49[\s\-/]?\d{2,4}[\s\-/]?\d{3,9}", score=0.7),
    Pattern(name="phone_de_landline", regex=r"0\d{2,5}[\s\-/]?\d{5,9}", score=0.6),
]
phone_recognizer = PatternRecognizer(
    supported_entity="PHONE_NUMBER",
    patterns=phone_patterns,
    context=["tel", "telefon", "phone", "mobile", "handy", "fon"],
    supported_language="en"
)
registry.add_recognizer(phone_recognizer)

# Deutscher IBAN-Recognizer
iban_pattern = Pattern(
    name="iban_de",
    regex=r"\bDE\d{2}[\s]?\d{4}[\s]?\d{4}[\s]?\d{4}[\s]?\d{4}[\s]?\d{2}\b",
    score=0.9
)
iban_recognizer = PatternRecognizer(
    supported_entity="IBAN_CODE",
    patterns=[iban_pattern],
    context=["iban", "konto", "bankverbindung"],
    supported_language="en"
)
registry.add_recognizer(iban_recognizer)

# Deutscher Datums-Recognizer
date_patterns = [
    Pattern(name="date_de_dot", regex=r"\b\d{1,2}\.\d{1,2}\.\d{4}\b", score=0.6),
    Pattern(name="date_de_slash", regex=r"\b\d{1,2}/\d{1,2}/\d{4}\b", score=0.6),
]
date_recognizer = PatternRecognizer(
    supported_entity="DATE_TIME",
    patterns=date_patterns,
    context=["datum", "geboren", "geburtsdatum", "date"],
    supported_language="en"
)
registry.add_recognizer(date_recognizer)

# Erstelle Analyzer mit Dummy NLP Engine und unserer Registry
dummy_nlp = DummyNlpEngine()
analyzer = AnalyzerEngine(
    registry=registry,
    nlp_engine=dummy_nlp,
    supported_languages=["en"]  # Muss konsistent mit Registry sein
)
anonymizer = AnonymizerEngine()

print("✅ Presidio bereit!")
print()


def anonymize_text(text, language="de"):
    """Anonymisiert Text mit Presidio"""

    # Analysiere Text
    results = analyzer.analyze(
        text=text,
        language=language,
        entities=None  # Alle Entities erkennen
    )

    if not results:
        print("⚠️  Warnung: Keine persönlichen Daten erkannt")

    # Anonymisiere
    anonymized = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        operators={
            "DEFAULT": OperatorConfig("replace", {"new_value": "<ANONYMISIERT>"}),
            "PERSON": OperatorConfig("replace", {"new_value": "<PERSON>"}),
            "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "<EMAIL>"}),
            "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "<TELEFON>"}),
            "LOCATION": OperatorConfig("replace", {"new_value": "<ORT>"}),
            "DATE_TIME": OperatorConfig("replace", {"new_value": "<DATUM>"}),
            "CREDIT_CARD": OperatorConfig("replace", {"new_value": "<KREDITKARTE>"}),
            "IBAN_CODE": OperatorConfig("replace", {"new_value": "<IBAN>"}),
            "IP_ADDRESS": OperatorConfig("replace", {"new_value": "<IP-ADRESSE>"}),
            "URL": OperatorConfig("replace", {"new_value": "<URL>"}),
            "US_SSN": OperatorConfig("replace", {"new_value": "<SSN>"}),
        }
    )

    return anonymized.text


# ============================================================================
# 👉 HIER DEINEN TEXT EINFÜGEN:
# ============================================================================

DEIN_TEXT = """
Max Mustermann
Email: max.mustermann@example.com
Tel: 0176 12345678
Tel2: +49 30 98765432
Geburtsdatum: 15.03.1990
IBAN: DE89 3704 0044 0532 0130 00
Website: https://www.example.com
IP: 192.168.1.100
Kreditkarte: 4111 1111 1111 1111
"""

# ↑↑↑ Ändere den Text oben mit deinem eigenen Text! ↑↑↑

# ============================================================================
# TEST AUSFÜHREN
# ============================================================================

print("=" * 70)
print("📝 ORIGINAL TEXT:")
print("=" * 70)
print(DEIN_TEXT)
print()

print("=" * 70)
print("🔒 ANONYMISIERT:")
print("=" * 70)
anonymized_text = anonymize_text(DEIN_TEXT, language="en")  # "en" weil Registry auf "en" ist
print(anonymized_text)
print()

print("=" * 70)
print("✅ FERTIG!")
print("=" * 70)
print("👉 Kopiere den anonymisierten Text oben und sende ihn an deine KI!")
print()

# ============================================================================
# WEITERE BEISPIELE
# ============================================================================

print("\n" + "=" * 70)
print("📚 WEITERE BEISPIELE:")
print("=" * 70)
print()

beispiele = [
    "Kontakt: anna.schmidt@gmail.com, Tel: 0176 98765432",
    "IBAN: DE89 3704 0044 0532 0130 00, geboren am 15.03.1990",
    "Telefon: +49 30 12345678, www.example.com",
    "Kreditkarte: 5500 0000 0000 0004, IP: 192.168.1.1",
]

for i, text in enumerate(beispiele, 1):
    anonymized = anonymize_text(text, 'en')
    print(f"Beispiel {i}:")
    print(f"  Vorher:  {text}")
    print(f"  Nachher: {anonymized}")
    print()

print("=" * 70)
print("ℹ️  Erkannte Daten-Typen:")
print("  • E-Mail → <EMAIL>")
print("  • Telefon → <TELEFON>")
print("  • IBAN → <IBAN>")
print("  • Datum → <DATUM>")
print("  • Kreditkarte → <KREDITKARTE>")
print("  • IP-Adresse → <IP-ADRESSE>")
print("  • URL → <URL>")
print("=" * 70)
