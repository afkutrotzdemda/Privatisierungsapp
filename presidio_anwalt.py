"""
PRESIDIO TEXT ANONYMISIERER - FÜR ANWÄLTE
==========================================

Speziell entwickelt für juristische Texte mit erweiterter Erkennung:
- Namen (deutsche Vor- und Nachnamen)
- Adressen (Straßen, PLZ, Städte)
- Aktenzeichen
- Ausweisnummern
- Steuer-IDs
- Sozialversicherungsnummern
- Und vieles mehr...

DSGVO-konform anonymisieren vor dem Senden an KI-Systeme!
"""

from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

print("=" * 70)
print("⚖️  PRESIDIO ANONYMISIERER FÜR ANWÄLTE")
print("=" * 70)
print()
print("DSGVO-konforme Anonymisierung für juristische Texte")
print()

# Initialisiere Presidio OHNE Sprachmodelle
print("⏳ Initialisiere Presidio...")

# Dummy NLP Engine (braucht kein spaCy!)
class DummyNlpEngine(NlpEngine):
    def process_text(self, text, language):
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

# Erstelle Registry
registry = RecognizerRegistry()

print("⏳ Lade Erkennungsmuster für juristische Texte...")

# ============================================================================
# 1. PERSÖNLICHE DATEN
# ============================================================================

# E-Mail
email_pattern = Pattern(
    name="email",
    regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    score=0.9
)
email_recognizer = PatternRecognizer(
    supported_entity="EMAIL_ADDRESS",
    patterns=[email_pattern],
    supported_language="en"
)
registry.add_recognizer(email_recognizer)

# Telefon (deutsche Formate)
phone_patterns = [
    Pattern(name="phone_mobile", regex=r"0\d{3,4}[\s\-/]?\d{3,4}[\s\-/]?\d{3,4}", score=0.8),
    Pattern(name="phone_intl", regex=r"\+49[\s\-/]?\d{2,4}[\s\-/]?\d{3,9}", score=0.8),
    Pattern(name="phone_landline", regex=r"0\d{2,5}[\s\-/]?\d{5,9}", score=0.7),
    Pattern(name="phone_brackets", regex=r"\(\d{2,5}\)[\s\-/]?\d{5,9}", score=0.7),
]
phone_recognizer = PatternRecognizer(
    supported_entity="PHONE_NUMBER",
    patterns=phone_patterns,
    supported_language="en"
)
registry.add_recognizer(phone_recognizer)

# Namen (deutsche Vor- und Nachnamen)
# Erkennt: "Max Mustermann", "Dr. Anna Schmidt", "Prof. Dr. Klaus Meyer"
name_patterns = [
    # Vollständige Namen mit Anrede
    Pattern(
        name="name_with_title",
        regex=r"\b(Herr|Frau|Hr\.|Fr\.|Herrn)\s+(Dr\.\s+)?(Prof\.\s+)?(Dr\.\s+)?[A-ZÄÖÜ][a-zäöüß]+\s+[A-ZÄÖÜ][a-zäöüß]+(-[A-ZÄÖÜ][a-zäöüß]+)?\b",
        score=0.85
    ),
    # Namen mit Titel ohne Anrede
    Pattern(
        name="name_with_dr",
        regex=r"\b(Dr\.|Prof\.|Prof\.\s+Dr\.)\s+[A-ZÄÖÜ][a-zäöüß]+\s+[A-ZÄÖÜ][a-zäöüß]+(-[A-ZÄÖÜ][a-zäöüß]+)?\b",
        score=0.8
    ),
    # Einfache Namen (Vorname Nachname)
    Pattern(
        name="simple_name",
        regex=r"\b[A-ZÄÖÜ][a-zäöüß]{2,}\s+[A-ZÄÖÜ][a-zäöüß]{2,}(-[A-ZÄÖÜ][a-zäöüß]+)?\b",
        score=0.6
    ),
]
name_recognizer = PatternRecognizer(
    supported_entity="PERSON",
    patterns=name_patterns,
    context=["name", "herr", "frau", "mandant", "kläger", "beklagte", "zeuge"],
    supported_language="en"
)
registry.add_recognizer(name_recognizer)

# ============================================================================
# 2. ADRESSEN & ORTE
# ============================================================================

# Straßenadressen
street_patterns = [
    # Straßenname + Hausnummer
    Pattern(
        name="street_strasse",
        regex=r"\b[A-ZÄÖÜ][a-zäöüß]+straße\s+\d+[a-zA-Z]?",
        score=0.85
    ),
    Pattern(
        name="street_str",
        regex=r"\b[A-ZÄÖÜ][a-zäöüß]+str\.\s+\d+[a-zA-Z]?",
        score=0.85
    ),
    Pattern(
        name="street_weg",
        regex=r"\b[A-ZÄÖÜ][a-zäöüß]+weg\s+\d+[a-zA-Z]?",
        score=0.85
    ),
    Pattern(
        name="street_platz",
        regex=r"\b[A-ZÄÖÜ][a-zäöüß]+platz\s+\d+[a-zA-Z]?",
        score=0.85
    ),
    Pattern(
        name="street_allee",
        regex=r"\b[A-ZÄÖÜ][a-zäöüß]+allee\s+\d+[a-zA-Z]?",
        score=0.85
    ),
]
street_recognizer = PatternRecognizer(
    supported_entity="STREET_ADDRESS",
    patterns=street_patterns,
    context=["adresse", "wohnhaft", "ansässig", "straße"],
    supported_language="en"
)
registry.add_recognizer(street_recognizer)

# Postleitzahl + Stadt
postal_patterns = [
    Pattern(
        name="plz_stadt",
        regex=r"\b\d{5}\s+[A-ZÄÖÜ][a-zäöüß]+(?:\s+[a-zäöüß]+)?\b",
        score=0.8
    ),
    Pattern(
        name="plz",
        regex=r"\bPLZ:?\s*\d{5}\b",
        score=0.9
    ),
]
postal_recognizer = PatternRecognizer(
    supported_entity="LOCATION",
    patterns=postal_patterns,
    context=["plz", "postleitzahl", "wohnort", "ort"],
    supported_language="en"
)
registry.add_recognizer(postal_recognizer)

# ============================================================================
# 3. JURISTISCHE DATEN
# ============================================================================

# Aktenzeichen
case_patterns = [
    # Format: 1 Js 123/21, 2 C 456/20, etc.
    Pattern(
        name="aktenzeichen",
        regex=r"\b\d+\s+[A-Z]{1,3}\s+\d+/\d{2,4}\b",
        score=0.9
    ),
    # Format: Az.: 1 Js 123/21
    Pattern(
        name="aktenzeichen_az",
        regex=r"\bAz\.?:?\s*\d+\s+[A-Z]{1,3}\s+\d+/\d{2,4}\b",
        score=0.95
    ),
]
case_recognizer = PatternRecognizer(
    supported_entity="CASE_NUMBER",
    patterns=case_patterns,
    context=["aktenzeichen", "az", "verfahren"],
    supported_language="en"
)
registry.add_recognizer(case_recognizer)

# ============================================================================
# 4. IDENTIFIKATIONSNUMMERN
# ============================================================================

# IBAN
iban_pattern = Pattern(
    name="iban_de",
    regex=r"\bDE\d{2}[\s]?\d{4}[\s]?\d{4}[\s]?\d{4}[\s]?\d{4}[\s]?\d{2}\b",
    score=0.95
)
iban_recognizer = PatternRecognizer(
    supported_entity="IBAN_CODE",
    patterns=[iban_pattern],
    supported_language="en"
)
registry.add_recognizer(iban_recognizer)

# Steuer-ID
tax_patterns = [
    Pattern(
        name="steuer_id",
        regex=r"\b\d{11}\b",
        score=0.6
    ),
    Pattern(
        name="steuer_id_labeled",
        regex=r"\b(Steuer-ID|Steueridentifikationsnummer|St\.-Nr\.|Steuernummer):?\s*\d{10,13}\b",
        score=0.95
    ),
]
tax_recognizer = PatternRecognizer(
    supported_entity="TAX_ID",
    patterns=tax_patterns,
    context=["steuer", "finanzamt", "steuernummer"],
    supported_language="en"
)
registry.add_recognizer(tax_recognizer)

# Sozialversicherungsnummer
sv_pattern = Pattern(
    name="sozialversicherungsnummer",
    regex=r"\b\d{2}\s?\d{6}\s?[A-Z]\s?\d{3}\b",
    score=0.8
)
sv_recognizer = PatternRecognizer(
    supported_entity="SOCIAL_SECURITY_NUMBER",
    patterns=[sv_pattern],
    context=["sozialversicherung", "rentenversicherung", "sv-nummer"],
    supported_language="en"
)
registry.add_recognizer(sv_recognizer)

# Personalausweisnummer
id_patterns = [
    Pattern(
        name="perso_nummer",
        regex=r"\b[A-Z]\d{9}\b",
        score=0.7
    ),
    Pattern(
        name="perso_labeled",
        regex=r"\b(Personalausweis|Ausweis-Nr\.|PA):?\s*[A-Z0-9]{9,10}\b",
        score=0.9
    ),
]
id_recognizer = PatternRecognizer(
    supported_entity="ID_NUMBER",
    patterns=id_patterns,
    context=["personalausweis", "ausweis", "identifikation"],
    supported_language="en"
)
registry.add_recognizer(id_recognizer)

# ============================================================================
# 5. WEITERE STANDARD-DATEN
# ============================================================================

# Datum
date_patterns = [
    Pattern(name="date_de_dot", regex=r"\b\d{1,2}\.\d{1,2}\.\d{4}\b", score=0.7),
    Pattern(name="date_de_slash", regex=r"\b\d{1,2}/\d{1,2}/\d{4}\b", score=0.7),
    Pattern(name="date_iso", regex=r"\b\d{4}-\d{2}-\d{2}\b", score=0.7),
]
date_recognizer = PatternRecognizer(
    supported_entity="DATE_TIME",
    patterns=date_patterns,
    supported_language="en"
)
registry.add_recognizer(date_recognizer)

# Kreditkarte
credit_card_pattern = Pattern(
    name="credit_card",
    regex=r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b",
    score=0.8
)
credit_card_recognizer = PatternRecognizer(
    supported_entity="CREDIT_CARD",
    patterns=[credit_card_pattern],
    supported_language="en"
)
registry.add_recognizer(credit_card_recognizer)

# IP-Adresse
ip_pattern = Pattern(
    name="ip_address",
    regex=r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    score=0.8
)
ip_recognizer = PatternRecognizer(
    supported_entity="IP_ADDRESS",
    patterns=[ip_pattern],
    supported_language="en"
)
registry.add_recognizer(ip_recognizer)

# URL
url_patterns = [
    Pattern(name="url_http", regex=r"https?://[^\s]+", score=0.9),
    Pattern(name="url_www", regex=r"www\.[^\s]+", score=0.8),
]
url_recognizer = PatternRecognizer(
    supported_entity="URL",
    patterns=url_patterns,
    supported_language="en"
)
registry.add_recognizer(url_recognizer)

# ============================================================================
# ANALYZER ERSTELLEN
# ============================================================================

dummy_nlp = DummyNlpEngine()
analyzer = AnalyzerEngine(
    registry=registry,
    nlp_engine=dummy_nlp,
    supported_languages=["en"]
)
anonymizer = AnonymizerEngine()

print("✅ Presidio bereit mit erweiterten Erkennungsmustern!")
print()


def anonymize_text(text, language="en"):
    """Anonymisiert juristischen Text mit Presidio"""

    results = analyzer.analyze(
        text=text,
        language=language,
        entities=None
    )

    if not results:
        print("⚠️  Warnung: Keine personenbezogenen Daten erkannt")

    anonymized = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        operators={
            "DEFAULT": OperatorConfig("replace", {"new_value": "<ANONYMISIERT>"}),
            "PERSON": OperatorConfig("replace", {"new_value": "<PERSON>"}),
            "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "<EMAIL>"}),
            "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "<TELEFON>"}),
            "STREET_ADDRESS": OperatorConfig("replace", {"new_value": "<ADRESSE>"}),
            "LOCATION": OperatorConfig("replace", {"new_value": "<ORT>"}),
            "DATE_TIME": OperatorConfig("replace", {"new_value": "<DATUM>"}),
            "CREDIT_CARD": OperatorConfig("replace", {"new_value": "<KREDITKARTE>"}),
            "IBAN_CODE": OperatorConfig("replace", {"new_value": "<IBAN>"}),
            "IP_ADDRESS": OperatorConfig("replace", {"new_value": "<IP-ADRESSE>"}),
            "URL": OperatorConfig("replace", {"new_value": "<URL>"}),
            "CASE_NUMBER": OperatorConfig("replace", {"new_value": "<AKTENZEICHEN>"}),
            "TAX_ID": OperatorConfig("replace", {"new_value": "<STEUER-ID>"}),
            "SOCIAL_SECURITY_NUMBER": OperatorConfig("replace", {"new_value": "<SV-NUMMER>"}),
            "ID_NUMBER": OperatorConfig("replace", {"new_value": "<AUSWEIS-NR>"}),
        }
    )

    return anonymized.text


# ============================================================================
# 👉 HIER DEINEN TEXT EINFÜGEN:
# ============================================================================

DEIN_TEXT = """
Betreff: Mandant Max Mustermann

Sehr geehrte Frau Dr. Schmidt,

im Verfahren Az. 1 Js 123/21 gegen meinen Mandanten Herr Klaus Meyer,
wohnhaft in der Hauptstraße 45, 10115 Berlin, geboren am 15.03.1985,
möchte ich folgende Unterlagen einreichen:

Kontaktdaten:
- Email: klaus.meyer@email.de
- Telefon: 0176 98765432
- Steuer-ID: 12345678901
- IBAN: DE89 3704 0044 0532 0130 00

Der Vorfall ereignete sich am 24.10.2023 gegen 14:30 Uhr.
Zeugin war Frau Anna Schmidt, Tel: +49 30 12345678.

Mit freundlichen Grüßen
"""

# ↑↑↑ Füge DEINEN juristischen Text hier ein! ↑↑↑

# ============================================================================
# TEST AUSFÜHREN
# ============================================================================

print("=" * 70)
print("📄 ORIGINAL TEXT:")
print("=" * 70)
print(DEIN_TEXT)
print()

print("=" * 70)
print("🔒 ANONYMISIERT (DSGVO-konform):")
print("=" * 70)
anonymized_text = anonymize_text(DEIN_TEXT, language="en")
print(anonymized_text)
print()

print("=" * 70)
print("✅ FERTIG!")
print("=" * 70)
print("👉 Dieser Text kann jetzt sicher an KI-Systeme gesendet werden!")
print()

# ============================================================================
# WEITERE BEISPIELE
# ============================================================================

print("\n" + "=" * 70)
print("📚 WEITERE BEISPIELE:")
print("=" * 70)
print()

beispiele = [
    "Mandant: Dr. Thomas Weber, Hauptstraße 123, 80331 München",
    "Az.: 2 C 456/20, Kläger: Herr Schmidt, Tel: 0176 12345678",
    "Email: anwalt@kanzlei.de, IBAN: DE89 3704 0044 0532 0130 00",
    "Frau Prof. Dr. Meyer, geboren am 15.03.1990, Steuer-ID: 12345678901",
]

for i, text in enumerate(beispiele, 1):
    anonymized = anonymize_text(text, 'en')
    print(f"Beispiel {i}:")
    print(f"  Vorher:  {text}")
    print(f"  Nachher: {anonymized}")
    print()

print("=" * 70)
print("ℹ️  ERKANNTE DATEN-TYPEN:")
print("=" * 70)
print("  👤 Namen → <PERSON>")
print("  📧 E-Mail → <EMAIL>")
print("  📞 Telefon → <TELEFON>")
print("  🏠 Straße → <ADRESSE>")
print("  📍 PLZ/Stadt → <ORT>")
print("  📅 Datum → <DATUM>")
print("  💳 IBAN → <IBAN>")
print("  🆔 Ausweis-Nr → <AUSWEIS-NR>")
print("  📋 Aktenzeichen → <AKTENZEICHEN>")
print("  🔢 Steuer-ID → <STEUER-ID>")
print("  🏥 SV-Nummer → <SV-NUMMER>")
print("  💳 Kreditkarte → <KREDITKARTE>")
print("  🌐 IP/URL → <IP-ADRESSE>, <URL>")
print("=" * 70)
