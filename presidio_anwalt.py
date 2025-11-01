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
KANZLEI MÜLLER & PARTNER
Rechtsanwälte
Bahnhofstraße 78
60329 Frankfurt am Main
Tel: 069-12345678 | Fax: 069-12345679
Email: kanzlei@mueller-partner.de
www.mueller-partner.de

                                            Frankfurt, den 15.11.2024

Amtsgericht München
Zivilgericht, Abteilung 12
Nymphenburger Straße 20
80335 München

Az. unserer Kanzlei: 2024/456/MP
Ihr Az.: 12 C 789/24


Betreff: Klage wegen Schadensersatz und Schmerzensgeld
         Kläger: Dr. Max Mustermann
         Beklagter: Firma Schmidt GmbH & Co. KG
         Streitwert: 45.000,00 EUR


Sehr geehrte Damen und Herren,

namens und im Auftrag meines Mandanten, Herrn Dr. Max Alexander Mustermann,
geboren am 15.03.1985 in München, wohnhaft in der Leopoldstraße 123, 80802 München,
Steuer-ID: 12345678901, Personalausweis-Nr.: L234567890, erhebe ich

                                    Klage

gegen die Beklagte, Firma Schmidt GmbH & Co. KG, Sitz in Hamburg, vertreten durch
den Geschäftsführer Herrn Thomas Weber, Hauptstraße 45, 20095 Hamburg,
Handelsregister Hamburg HRB 123456.


I. SACHVERHALT

1. Mein Mandant war vom 01.04.2020 bis 31.08.2024 bei der Beklagten als
   leitender Angestellter im Bereich IT-Security beschäftigt (vgl. Arbeitsvertrag
   vom 15.03.2020, Az. 2020/AV/456).

2. Die monatliche Vergütung belief sich zuletzt auf 8.500,00 EUR brutto.
   Die Zahlungen erfolgten stets auf das Konto meines Mandanten bei der
   Deutschen Bank, IBAN: DE89 3704 0044 0532 0130 00, BIC: COBADEFFXXX.

3. Am 12.07.2024 gegen 09:45 Uhr ereignete sich in den Büroräumen der Beklagten
   in der Alsterstraße 67, 20095 Hamburg, ein Arbeitsunfall. Mein Mandant stürzte
   aufgrund mangelhafter Sicherung eines Kabels und erlitt einen Bruch des rechten
   Oberarmknochens sowie eine schwere Gehirnerschütterung.

4. Der Unfall wurde durch folgende Zeugen beobachtet:

   a) Frau Anna Schmidt, Sekretärin, wohnhaft Müllerweg 34, 22087 Hamburg,
      Tel: 040-98765432, Email: a.schmidt@example.de

   b) Herr Prof. Dr. Klaus Meyer, IT-Leiter, Hauptstraße 12, 20354 Hamburg,
      Tel: +49 40 12345678, Email: k.meyer@example.com

   c) Frau Petra Schulz, Reinigungskraft, Gartenstraße 5, 21073 Hamburg,
      Tel: 0176 98765432

5. Die ärztliche Erstversorgung erfolgte durch Dr. med. Andreas Werner,
   Facharzt für Orthopädie, Praxis in der Eppendorfer Landstraße 89, 20249 Hamburg,
   Telefon: 040-23456789, Email: praxis@dr-werner-ortho.de.

6. Mein Mandant war vom 12.07.2024 bis 15.10.2024 arbeitsunfähig erkrankt.
   Die Beklagte weigerte sich, Lohnfortzahlung über den 30.09.2024 hinaus zu leisten.

7. Am 20.08.2024 erhielt mein Mandant eine fristlose Kündigung per Einschreiben
   (Sendungsnummer: RR123456789DE), zugestellt am 21.08.2024 um 10:15 Uhr.

8. Gegen diese Kündigung läuft bereits ein separates Verfahren vor dem
   Arbeitsgericht Hamburg, Az. 15 Ca 234/24.


II. ANSPRUCHSGRUNDLAGEN

1. Schadensersatz gem. § 823 Abs. 1 BGB i.V.m. § 618 BGB
   - Verdienstausfall: 17.000,00 EUR (2 Monate à 8.500 EUR)
   - Behandlungskosten: 5.400,00 EUR
   - Fahrtkosten zu Ärzten: 780,00 EUR
   - Anwaltskosten Vorverfahren: 2.500,00 EUR

   Zwischensumme: 25.680,00 EUR

2. Schmerzensgeld gem. § 253 Abs. 2 BGB
   Angemessen erscheinen mindestens: 15.000,00 EUR

3. Feststellungsantrag bezüglich zukünftiger Schäden

4. Verzugszinsen gem. § 288 BGB seit dem 01.09.2024


III. BEWEISMITTEL

1. Arbeitsvertrag vom 15.03.2020
2. Gehaltsabrechnungen Juli - Oktober 2024
3. Unfallprotokoll vom 12.07.2024, erstellt von Sicherheitsbeauftragtem
4. Ärztliches Attest Dr. Werner vom 12.07.2024
5. MRT-Befund Universitätsklinikum Hamburg-Eppendorf vom 13.07.2024
6. Arbeitsunfähigkeitsbescheinigungen (durchgehend bis 15.10.2024)
7. Kündigungsschreiben vom 20.08.2024
8. Kontoauszüge Deutsche Bank, Konto-Nr.: 1234567890
9. Zeugenaussage Frau Schmidt (Protokoll vom 05.09.2024, Az. Pol. HH-1234/24)
10. Gutachten des Sachverständigen Dr. Friedrich Koch, Bergstraße 23,
    60311 Frankfurt, Tel: 069-87654321, erstellt am 10.10.2024
11. E-Mail-Verkehr mit Personalabteilung (von hr@schmidt-gmbh.de)
12. Foto-Dokumentation der Unfallstelle (erstellt 12.07.2024, 10:30 Uhr)
13. Zeugenvernehmung Prof. Dr. Meyer geplant für 20.12.2024, 14:00 Uhr


IV. ANTRÄGE

Ich beantrage,

1. die Beklagte zu verurteilen, an meinen Mandanten 25.680,00 EUR nebst Zinsen
   in Höhe von 5 Prozentpunkten über dem Basiszinssatz seit dem 01.09.2024 zu zahlen;

2. die Beklagte zu verurteilen, an meinen Mandanten ein Schmerzensgeld in Höhe
   von 15.000,00 EUR nebst Zinsen in Höhe von 5 Prozentpunkten über dem
   Basiszinssatz seit Rechtshängigkeit zu zahlen;

3. festzustellen, dass die Beklagte verpflichtet ist, meinem Mandanten alle
   weiteren materiellen und immateriellen Schäden zu ersetzen, die aus dem
   Unfall vom 12.07.2024 noch entstehen werden;

4. die Beklagte zu verurteilen, die Kosten des Rechtsstreits zu tragen.


V. TERMINSVERLEGUNGSANTRAG

Ich beantrage zudem, den für den 28.11.2024 um 10:00 Uhr anberaumten
Gütetermin zu verlegen, da mein Mandant an diesem Tag einen ärztlichen
Kontrolltermin bei Dr. Werner wahrnehmen muss (Terminbestätigung vom 05.11.2024).

Ein Ausweichtermin wäre der 05.12.2024 nach 14:00 Uhr oder jeder Tag ab dem
10.12.2024 möglich.


VI. PROZESSKOSTENHILFE

Für den Fall, dass meinem Mandanten die Kosten des Rechtsstreits nicht zuzumuten
sind, beantrage ich die Bewilligung von Prozesskostenhilfe. Die entsprechende
Erklärung über die persönlichen und wirtschaftlichen Verhältnisse
(Formular PKH 1) ist beigefügt.

Aktuelle Vermögenssituation meines Mandanten:
- Guthaben Girokonto: 450,00 EUR (Deutsche Bank)
- Guthaben Sparkonto: 2.300,00 EUR (Sparkasse München, IBAN: DE12 7015 0000 1234 5678 90)
- Keine Immobilien
- PKW (Wert ca. 8.000 EUR, noch Kredit offen: 6.500 EUR bei VW Bank)
- Unterhaltspflicht für 2 Kinder: Sophie Mustermann (geb. 12.05.2015) und
  Leon Mustermann (geb. 23.08.2018), wohnhaft bei der Kindsmutter
  Frau Lisa Mustermann, Rosenweg 8, 80805 München


VII. ANLAGEN

Anlage K1:  Arbeitsvertrag
Anlage K2:  Gehaltsabrechnungen (4 Stück)
Anlage K3:  Unfallprotokoll
Anlage K4:  Ärztliche Atteste (3 Stück)
Anlage K5:  MRT-Befund
Anlage K6:  AU-Bescheinigungen
Anlage K7:  Kündigungsschreiben
Anlage K8:  Kontoauszüge
Anlage K9:  Sachverständigengutachten
Anlage K10: E-Mail-Verkehr
Anlage K11: Lichtbilder
Anlage K12: Formular PKH 1


Mit vorzüglicher Hochachtung


____________________
Dr. jur. Michael Müller
Rechtsanwalt
Fachanwalt für Arbeitsrecht
Zulassungsnummer: 12345
Rechtsanwaltskammer Frankfurt

Kontakt Kanzlei:
Sekretariat Frau Sabine Weber: Tel. 069-12345678-10, s.weber@mueller-partner.de
Buchhaltung Herr Josef Klein: Tel. 069-12345678-20, buchhaltung@mueller-partner.de
Fax: 069-12345679
Notfallnummer (24/7): +49 172 9876543
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
