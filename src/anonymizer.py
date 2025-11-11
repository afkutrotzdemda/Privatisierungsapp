"""
Text Anonymisierung mit Microsoft Presidio
ERWEITERTE VERSION mit deutschen Mustern für Anwälte + Whitelist + ML-Modi
"""

from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern, RecognizerRegistry, RecognizerResult
from presidio_analyzer.nlp_engine import NlpEngine, SpacyNlpEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from presidio_anonymizer.operators import Operator, OperatorType
from typing import List, Optional, Dict
import logging
import time
import re

logger = logging.getLogger(__name__)


# Custom Operator: Ersetzt Namen durch ersten Buchstaben + Punkt
class FirstLetterOperator(Operator):
    """Anonymisiert Namen zu 'X.' (erster Buchstabe + Punkt)"""

    def operate(self, text: str, params: Dict = None) -> str:
        """
        Ersetzt Namen durch Titel + ersten Buchstaben vom Nachnamen + Punkt

        Titel bleiben ERHALTEN für bessere Lesbarkeit:
        "Max Mustermann" → "M."
        "Dr. Anna Schmidt" → "Dr. S."
        "Herr Müller" → "Herr M."
        "Herr Dr. Klaus Meier" → "Herr Dr. M."
        """
        if not text or not text.strip():
            return text

        text = text.strip()

        # Extrahiere Titel am Anfang (können mehrere sein)
        # Pattern: Herr, Frau, Dr., Prof., Hr., Fr., Herrn
        title_match = re.match(r'^((Herr|Frau|Dr\.|Prof\.|Hr\.|Fr\.|Herrn)\s+)+', text)

        if title_match:
            # Titel gefunden
            titles = title_match.group(0).strip()  # z.B. "Herr Dr."
            rest = text[title_match.end():].strip()  # z.B. "Klaus Meier"

            # Finde letztes Wort (Nachname)
            words = rest.split()
            if words:
                last_name = words[-1]  # "Meier"
                first_letter = last_name[0].upper()
                return f"{titles} {first_letter}."
            else:
                # Kein Name nach Titel? Nimm ersten Buchstaben vom Titel
                return f"{titles[0].upper()}."

        else:
            # Kein Titel: Nimm letztes Wort (Nachname)
            words = text.split()
            if len(words) >= 2:
                # "Max Mustermann" → "M." (vom Nachnamen "Mustermann")
                last_name = words[-1]
                return f"{last_name[0].upper()}."
            else:
                # Nur ein Wort
                return f"{text[0].upper()}."

    def validate(self, params: Dict = None) -> None:
        """Validierung (nicht benötigt)"""
        pass

    def operator_name(self) -> str:
        """Name des Operators"""
        return "first_letter"

    def operator_type(self) -> OperatorType:
        """Typ des Operators"""
        return OperatorType.Anonymize


# Custom Operator: Ersetzt Straßennamen durch ersten Buchstaben + Suffix
class StreetFirstLetterOperator(Operator):
    """Anonymisiert Straßen zu 'X.straße 123'"""

    def operate(self, text: str, params: Dict = None) -> str:
        """
        Ersetzt Straßennamen durch ersten Buchstaben + Suffix + Hausnummer

        "Musterstraße 123" → "M.straße 123"
        "Hauptstr. 45a" → "H.str. 45a"
        "Berliner Allee 10" → "B. Allee 10"
        """
        if not text or not text.strip():
            return text

        text = text.strip()

        # Pattern: Wortanfang + suffix (straße/str./weg/platz/allee) + Nummer
        # z.B. "Musterstraße 123", "Hauptstr. 45"
        match = re.match(r'^([A-ZÄÖÜ][a-zäöüß]+)(straße|str\.|weg|platz|allee)(\s+\d+[a-zA-Z]?)$', text)

        if match:
            street_name = match.group(1)  # "Muster"
            suffix = match.group(2)       # "straße"
            number = match.group(3)       # " 123"

            first_letter = street_name[0].upper()
            return f"{first_letter}.{suffix}{number}"

        # Fallback: Nur ersten Buchstaben
        return f"{text[0].upper()}."

    def validate(self, params: Dict = None) -> None:
        pass

    def operator_name(self) -> str:
        return "street_first_letter"

    def operator_type(self) -> OperatorType:
        return OperatorType.Anonymize


# Custom Operator: Maskiert E-Mail (behält Domain-Typ)
class EmailMaskOperator(Operator):
    """Maskiert E-Mail aber behält Struktur"""

    def operate(self, text: str, params: Dict = None) -> str:
        """
        "max.mueller@firma.de" → "***@***.de"
        """
        if not text or '@' not in text:
            return "***@***.***"

        local, domain = text.split('@', 1)
        # Behalte nur TLD (.de, .com, etc.)
        domain_parts = domain.split('.')
        if len(domain_parts) >= 2:
            tld = domain_parts[-1]
            return f"***@***.{tld}"
        return "***@***.***"

    def validate(self, params: Dict = None) -> None:
        pass

    def operator_name(self) -> str:
        return "email_mask"

    def operator_type(self) -> OperatorType:
        return OperatorType.Anonymize


# Custom Operator: Maskiert Telefon (behält Vorwahl)
class PhoneMaskOperator(Operator):
    """Maskiert Telefon aber behält Vorwahl"""

    def operate(self, text: str, params: Dict = None) -> str:
        """
        "030 12345678" → "030 XXXXXX"
        "+49 30 123456" → "+49 30 XXXXXX"
        "030 555-1234" → "030 XXXXXX"
        """
        if not text or not text.strip():
            return "XXXXXXXXXX"

        text = text.strip()

        # Pattern: Internationale Vorwahl (optional) + Ortsvorwahl
        # z.B. "+49 30 123456", "030 12345678", "030 555-1234"

        # Versuche internationale Format: +49 30 ...
        match = re.match(r'^(\+\d{1,3})[\s\-/]?(\d{2,4})[\s\-/](.+)$', text)
        if match:
            country = match.group(1)  # "+49"
            area = match.group(2)      # "30"
            rest = match.group(3)      # Rest der Nummer

            digit_count = len([c for c in rest if c.isdigit()])
            masked = 'X' * max(digit_count, 6)
            return f"{country} {area} {masked}"

        # Nationales Format: 030 ...
        match = re.match(r'^(0\d{1,4})[\s\-/](.+)$', text)
        if match:
            prefix = match.group(1)  # "030"
            rest = match.group(2)     # "12345678" oder "555-1234"

            # Zähle Ziffern im Rest
            digit_count = len([c for c in rest if c.isdigit()])
            masked = 'X' * max(digit_count, 6)
            return f"{prefix} {masked}"

        # Fallback: Nur Ziffern ohne Vorwahl
        digit_count = len([c for c in text if c.isdigit()])
        if digit_count >= 6:
            return 'X' * digit_count

        return "XXXXXXXXXX"

    def validate(self, params: Dict = None) -> None:
        pass

    def operator_name(self) -> str:
        return "phone_mask"

    def operator_type(self) -> OperatorType:
        return OperatorType.Anonymize


# Custom Operator: Maskiert IBAN (behält Ländercode)
class IbanMaskOperator(Operator):
    """Maskiert IBAN aber behält Ländercode"""

    def operate(self, text: str, params: Dict = None) -> str:
        """
        "DE89 3704 0044 0532 0130 00" → "DE** **** ****"
        """
        if not text or not text.strip():
            return "DE** ****"

        text = text.strip()

        # Ländercode (erste 2 Zeichen)
        if len(text) >= 2:
            country = text[:2].upper()
            return f"{country}** **** ****"

        return "DE** ****"

    def validate(self, params: Dict = None) -> None:
        pass

    def operator_name(self) -> str:
        return "iban_mask"

    def operator_type(self) -> OperatorType:
        return OperatorType.Anonymize


# Custom Operator: Maskiert Datum (behält Monat/Jahr)
class DateMaskOperator(Operator):
    """Maskiert Datum aber behält Monat/Jahr"""

    def operate(self, text: str, params: Dict = None) -> str:
        """
        "15. März 2024" → "XX. März 2024"
        "15.03.2024" → "XX.03.2024"
        """
        if not text or not text.strip():
            return "XX.XX.XXXX"

        text = text.strip()

        # Pattern: "15. März 2024"
        match = re.match(r'^(\d{1,2})(\.\s*[A-Za-zä]+\s+\d{4})$', text)
        if match:
            rest = match.group(2)
            return f"XX{rest}"

        # Pattern: "15.03.2024"
        match = re.match(r'^(\d{1,2})(\.\d{2}\.\d{4})$', text)
        if match:
            rest = match.group(2)
            return f"XX{rest}"

        # Pattern: "2024-03-15" (ISO)
        match = re.match(r'^(\d{4})-(\d{2})-(\d{2})$', text)
        if match:
            year = match.group(1)
            month = match.group(2)
            return f"{year}-{month}-XX"

        # Fallback
        return "XX.XX.XXXX"

    def validate(self, params: Dict = None) -> None:
        pass

    def operator_name(self) -> str:
        return "date_mask"

    def operator_type(self) -> OperatorType:
        return OperatorType.Anonymize


# Custom Operator: Maskiert Aktenzeichen (behält Jahr)
class CaseNumberMaskOperator(Operator):
    """Maskiert Aktenzeichen aber behält Jahr"""

    def operate(self, text: str, params: Dict = None) -> str:
        """
        "123 C 456/2024" → "*** C ***/2024"
        "Az.: 12 Js 345/24" → "Az.: ** Js ***/24"
        """
        if not text or not text.strip():
            return "*** *** ***"

        text = text.strip()

        # Pattern: "123 C 456/2024" oder "12 Js 345/24"
        # Behalte Buchstaben und Jahr
        match = re.match(r'^(Az\.?:?\s*)?(\d+)\s+([A-Z][a-z]?)\s+(\d+)/(\d{2,4})$', text)

        if match:
            prefix = match.group(1) or ""
            letter = match.group(3)  # "C" oder "Js"
            year = match.group(5)    # "2024" oder "24"

            return f"{prefix}*** {letter} ***/{year}"

        # Fallback
        return "*** *** ***"

    def validate(self, params: Dict = None) -> None:
        pass

    def operator_name(self) -> str:
        return "case_number_mask"

    def operator_type(self) -> OperatorType:
        return OperatorType.Anonymize


# Custom Operator: Ersetzt Ortsnamen durch ersten Buchstaben
class LocationFirstLetterOperator(Operator):
    """Anonymisiert Orte zu 'PLZ X.'"""

    def operate(self, text: str, params: Dict = None) -> str:
        """
        Ersetzt Ortsnamen und PLZ durch Maskierung

        "12345 Musterstadt" → "XXXXX M."
        "Berlin" → "B."
        """
        if not text or not text.strip():
            return text

        text = text.strip()

        # Pattern: PLZ + Stadt (z.B. "12345 Musterstadt")
        match = re.match(r'^(\d{5})\s+([A-ZÄÖÜ][a-zäöüß]+(?:\s+[a-zäöüß]+)?)$', text)

        if match:
            # PLZ maskieren mit XXXXX
            city = match.group(2)     # "Musterstadt"

            # Erster Buchstabe der Stadt
            first_letter = city[0].upper()
            return f"XXXXX {first_letter}."

        # Kein PLZ: Nur Stadt
        # z.B. "Berlin" → "B."
        words = text.split()
        if words:
            first_letter = words[0][0].upper()
            return f"{first_letter}."

        return f"{text[0].upper()}."

    def validate(self, params: Dict = None) -> None:
        pass

    def operator_name(self) -> str:
        return "location_first_letter"

    def operator_type(self) -> OperatorType:
        return OperatorType.Anonymize


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


class TextAnonymizer:
    """Anonymisiert Text mit Presidio und erweiterten deutschen Patterns + Whitelist"""

    def __init__(self, language: str = "de"):
        """
        Initialisiert den Anonymizer

        Args:
            language: Sprache für die Analyse (de für Deutsch, en für Englisch)
        """
        self.language = language
        self.analyzer = None
        self.anonymizer = None

        # Lade Config und Whitelist
        try:
            # Versuche relativen Import (wenn als Modul importiert)
            try:
                from .config_loader import get_config
            except ImportError:
                # Fallback: Absoluter Import (wenn direkt ausgeführt)
                from config_loader import get_config

            self.config = get_config()
            self.whitelist = self.config.get_whitelist()
            self.recognition_mode = self.config.get_recognition_mode()
            self.person_threshold = self.config.get_person_score_threshold()
            self.other_threshold = self.config.get_other_score_threshold()
            logger.info(f"Whitelist geladen: {len(self.whitelist)} Einträge")
            logger.info(f"Erkennungs-Modus: {self.recognition_mode}")
            logger.info(f"Score-Thresholds: Namen={self.person_threshold}, Andere={self.other_threshold}")
        except Exception as e:
            logger.warning(f"Config konnte nicht geladen werden: {e}")
            self.config = None
            self.whitelist = []
            self.recognition_mode = 'fast'
            self.person_threshold = 0.7
            self.other_threshold = 0.6

    def _create_registry(self) -> RecognizerRegistry:
        """Erstellt Registry mit allen erweiterten Recognizers"""
        registry = RecognizerRegistry()

        # E-Mail
        email_pattern = Pattern(
            name="email",
            regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            score=0.9
        )
        registry.add_recognizer(PatternRecognizer(
            supported_entity="EMAIL_ADDRESS",
            patterns=[email_pattern],
            supported_language="en"
        ))

        # Telefon (deutsche Formate)
        # WICHTIG: Muss auch "030 555-1234" matchen (mit Bindestrich in der Nummer)
        phone_patterns = [
            # Mobilfunk: 0171 1234567 oder 0171-123-4567
            Pattern(name="phone_mobile", regex=r"0\d{3,4}[\s\-/]?\d{3,4}[\s\-/]?\d{3,4}", score=0.8),
            # International: +49 30 123456 oder +49-30-123456
            Pattern(name="phone_intl", regex=r"\+49[\s\-/]?\d{2,4}[\s\-/]?\d{3,9}", score=0.8),
            # Festnetz: 030 12345678 oder 030 555-1234 (mit Bindestrich!)
            Pattern(name="phone_landline", regex=r"0\d{2,5}[\s\-/]?(\d{3,4}[\s\-/]?)?\d{4,8}", score=0.7),
        ]
        registry.add_recognizer(PatternRecognizer(
            supported_entity="PHONE_NUMBER",
            patterns=phone_patterns,
            supported_language="en"
        ))

        # Namen (deutsche Vor- und Nachnamen)
        # SEHR RESTRIKTIV: Nur mit Titeln, mindestens 2+3 Zeichen!
        name_patterns = [
            # Mit Anrede + akadem. Titeln (sehr sicher) - ALLE KOMBINATIONEN!
            # z.B. "Herr Prof. Dr. Klaus-Dieter Schneider", "Frau Dr. med. Anna-Maria Müller-Hoffmann"
            # Vornamen: min 2 Zeichen ([A-ZÄÖÜ][a-zäöüß]{1,}  =  mind. 2 Zeichen gesamt)
            # Nachname: min 3 Zeichen ([A-ZÄÖÜ][a-zäöüß]{2,} = mind. 3 Zeichen gesamt)
            Pattern(
                name="name_with_title_complex",
                regex=r"\b(Herr|Frau|Hr\.|Fr\.|Herrn)\s+(Prof\.\s+)?(Dr\.\s+)?(med\.\s+)?(Prof\.\s+)?(Dr\.\s+)?([A-ZÄÖÜ][a-zäöüß]{1,}(-[A-ZÄÖÜ][a-zäöüß]+)?\s+)*[A-ZÄÖÜ][a-zäöüß]{2,}(-[A-ZÄÖÜ][a-zäöüß]+)?",
                score=0.95
            ),
            # Mit akademischem Titel (ohne Anrede) - MEHRERE VORNAMEN
            # z.B. "Dr. Heinrich Weber", "Prof. Dr. Müller"
            Pattern(
                name="name_with_dr",
                regex=r"\b(Prof\.\s+)?(Dr\.\s+)?(med\.\s+)?([A-ZÄÖÜ][a-zäöüß]{2,}(-[A-ZÄÖÜ][a-zäöüß]+)?\s+)*[A-ZÄÖÜ][a-zäöüß]{3,}(-[A-ZÄÖÜ][a-zäöüß]+)?",
                score=0.9
            ),
            # Nach Komma mit Titel
            # z.B. "namens meiner Mandantin, Frau Dr. Anna-Maria Weber"
            Pattern(
                name="name_after_comma_title",
                regex=r",\s+(Herr|Frau|Hr\.|Fr\.|Herrn)\s+(Dr\.\s+)?(med\.\s+)?([A-ZÄÖÜ][a-zäöüß]{2,}(-[A-ZÄÖÜ][a-zäöüß]+)?\s+)*[A-ZÄÖÜ][a-zäöüß]{3,}(-[A-ZÄÖÜ][a-zäöüß]+)?",
                score=0.95
            ),
        ]
        registry.add_recognizer(PatternRecognizer(
            supported_entity="PERSON",
            patterns=name_patterns,
            supported_language="en"
        ))

        # Straßenadressen
        street_patterns = [
            Pattern(name="street_strasse", regex=r"\b[A-ZÄÖÜ][a-zäöüß]+straße\s+\d+[a-zA-Z]?", score=0.85),
            Pattern(name="street_str", regex=r"\b[A-ZÄÖÜ][a-zäöüß]+str\.\s+\d+[a-zA-Z]?", score=0.85),
            Pattern(name="street_weg", regex=r"\b[A-ZÄÖÜ][a-zäöüß]+weg\s+\d+[a-zA-Z]?", score=0.85),
            Pattern(name="street_platz", regex=r"\b[A-ZÄÖÜ][a-zäöüß]+platz\s+\d+[a-zA-Z]?", score=0.85),
            Pattern(name="street_allee", regex=r"\b[A-ZÄÖÜ][a-zäöüß]+allee\s+\d+[a-zA-Z]?", score=0.85),
        ]
        registry.add_recognizer(PatternRecognizer(
            supported_entity="STREET_ADDRESS",
            patterns=street_patterns,
            supported_language="en"
        ))

        # PLZ + Stadt
        postal_patterns = [
            Pattern(name="plz_stadt", regex=r"\b\d{5}\s+[A-ZÄÖÜ][a-zäöüß]+(?:\s+[a-zäöüß]+)?\b", score=0.8),
        ]
        registry.add_recognizer(PatternRecognizer(
            supported_entity="LOCATION",
            patterns=postal_patterns,
            supported_language="en"
        ))

        # Aktenzeichen
        case_patterns = [
            Pattern(name="aktenzeichen", regex=r"\b\d+\s+[A-Z]{1,3}\s+\d+/\d{2,4}\b", score=0.9),
            Pattern(name="aktenzeichen_az", regex=r"\bAz\.?:?\s*\d+\s+[A-Z]{1,3}\s+\d+/\d{2,4}\b", score=0.95),
        ]
        registry.add_recognizer(PatternRecognizer(
            supported_entity="CASE_NUMBER",
            patterns=case_patterns,
            supported_language="en"
        ))

        # IBAN
        iban_pattern = Pattern(
            name="iban_de",
            regex=r"\bDE\d{2}[\s]?\d{4}[\s]?\d{4}[\s]?\d{4}[\s]?\d{4}[\s]?\d{2}\b",
            score=0.95
        )
        registry.add_recognizer(PatternRecognizer(
            supported_entity="IBAN_CODE",
            patterns=[iban_pattern],
            supported_language="en"
        ))

        # Kontonummer
        account_patterns = [
            Pattern(name="account_number", regex=r"\bKonto[-\s]?Nr\.?:?\s*\d{6,10}\b", score=0.9),
            Pattern(name="account_number_simple", regex=r"\bKontonummer:?\s*\d{6,10}\b", score=0.9),
        ]
        registry.add_recognizer(PatternRecognizer(
            supported_entity="ACCOUNT_NUMBER",
            patterns=account_patterns,
            supported_language="en"
        ))

        # Steuer-ID
        tax_patterns = [
            Pattern(name="steuer_id", regex=r"\b\d{11}\b", score=0.6),
            Pattern(name="steuer_id_labeled", regex=r"\b(Steuer-ID|Steueridentifikationsnummer|St\.-Nr\.|Steuernummer|Steuer-Nr\.):?\s*\d{2,3}/\d{3}/\d{4,5}\b", score=0.95),
        ]
        registry.add_recognizer(PatternRecognizer(
            supported_entity="TAX_ID",
            patterns=tax_patterns,
            supported_language="en"
        ))

        # Grundbuchnummern (Notariat)
        grundbuch_patterns = [
            Pattern(name="grundbuch_blatt", regex=r"\b(Grundbuch|GB)[\s\-]?(von\s+)?[A-ZÄÖÜ][a-zäöüß\-]+,?\s+(Blatt\s+)?\d{4,6}(/\d{2,4}[\-]\d{2,4})?\b", score=0.9),
            Pattern(name="grundbuch_short", regex=r"\bGB\s+\d{4,6}/\d{2,4}[\-]\d{2,4}\b", score=0.9),
        ]
        registry.add_recognizer(PatternRecognizer(
            supported_entity="PROPERTY_REF",
            patterns=grundbuch_patterns,
            supported_language="en"
        ))

        # Flurstück-Nummern (Kataster)
        flurstueck_patterns = [
            Pattern(name="flurstueck", regex=r"\b(Flurstück|Flur)\s+\d{1,4}(/\d{2,4})?\b", score=0.85),
            Pattern(name="gemarkung", regex=r"\b(Gemarkung|Gmkg\.)\s+[A-ZÄÖÜ][a-zäöüß\-]+,\s+Flur\s+\d{1,4}\b", score=0.9),
        ]
        registry.add_recognizer(PatternRecognizer(
            supported_entity="LAND_PARCEL",
            patterns=flurstueck_patterns,
            supported_language="en"
        ))

        # Sozialversicherungsnummer
        sv_pattern = Pattern(
            name="sozialversicherungsnummer",
            regex=r"\b\d{2}\s?\d{6}\s?[A-Z]\s?\d{3}\b",
            score=0.8
        )
        registry.add_recognizer(PatternRecognizer(
            supported_entity="SOCIAL_SECURITY_NUMBER",
            patterns=[sv_pattern],
            supported_language="en"
        ))

        # Personalausweisnummer
        id_patterns = [
            Pattern(name="perso_nummer", regex=r"\b[A-Z]\d{9}\b", score=0.7),
            Pattern(name="perso_labeled", regex=r"\b(Personalausweis|Ausweis-Nr\.|PA):?\s*[A-Z0-9]{9,10}\b", score=0.9),
        ]
        registry.add_recognizer(PatternRecognizer(
            supported_entity="ID_NUMBER",
            patterns=id_patterns,
            supported_language="en"
        ))

        # Datum
        date_patterns = [
            Pattern(name="date_de_dot", regex=r"\b\d{1,2}\.\d{1,2}\.\d{4}\b", score=0.7),
            Pattern(name="date_de_slash", regex=r"\b\d{1,2}/\d{1,2}/\d{4}\b", score=0.7),
            Pattern(name="date_iso", regex=r"\b\d{4}-\d{2}-\d{2}\b", score=0.7),
        ]
        registry.add_recognizer(PatternRecognizer(
            supported_entity="DATE_TIME",
            patterns=date_patterns,
            supported_language="en"
        ))

        # Kreditkarte
        credit_card_pattern = Pattern(
            name="credit_card",
            regex=r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b",
            score=0.8
        )
        registry.add_recognizer(PatternRecognizer(
            supported_entity="CREDIT_CARD",
            patterns=[credit_card_pattern],
            supported_language="en"
        ))

        # IP-Adresse
        ip_pattern = Pattern(
            name="ip_address",
            regex=r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
            score=0.8
        )
        registry.add_recognizer(PatternRecognizer(
            supported_entity="IP_ADDRESS",
            patterns=[ip_pattern],
            supported_language="en"
        ))

        # URL
        url_patterns = [
            Pattern(name="url_http", regex=r"https?://[^\s]+", score=0.9),
            Pattern(name="url_www", regex=r"www\.[^\s]+", score=0.8),
        ]
        registry.add_recognizer(PatternRecognizer(
            supported_entity="URL",
            patterns=url_patterns,
            supported_language="en"
        ))

        return registry

    def _filter_whitelist(self, text: str, analyzer_results: List[RecognizerResult]) -> List[RecognizerResult]:
        """
        Filtert erkannte Entities und entfernt die, die auf der Whitelist stehen

        WICHTIG: Whitelist gilt NUR für PERSON entities!
        E-Mail, Telefon, IBAN, etc. werden IMMER anonymisiert.

        Args:
            text: Der Original-Text
            analyzer_results: Liste von erkannten Entities

        Returns:
            Gefilterte Liste ohne Whitelist-Einträge
        """
        if not self.whitelist:
            return analyzer_results

        filtered_results = []
        removed_count = 0

        # Entity-Typen die IMMER anonymisiert werden (keine Whitelist-Filterung)
        always_anonymize = {
            "EMAIL_ADDRESS", "PHONE_NUMBER", "IBAN_CODE", "CREDIT_CARD",
            "IP_ADDRESS", "URL", "TAX_ID", "SOCIAL_SECURITY_NUMBER",
            "ID_NUMBER", "ACCOUNT_NUMBER", "DATE_TIME",
            "PROPERTY_REF", "LAND_PARCEL"  # Grundbuch + Flurstück
        }

        for result in analyzer_results:
            # IMMER anonymisieren für bestimmte Typen
            if result.entity_type in always_anonymize:
                filtered_results.append(result)
                continue

            # Extrahiere den erkannten Text
            detected_text = text[result.start:result.end]

            # Prüfe ob auf Whitelist (case-insensitive)
            if detected_text.lower() in self.whitelist:
                logger.debug(f"Whitelist-Match: '{detected_text}' wird NICHT anonymisiert")
                removed_count += 1
                continue

            # Prüfe ob ein Teil eines Whitelist-Eintrags ist
            # NUR für PERSON, LOCATION, STREET_ADDRESS
            is_whitelisted = False
            if result.entity_type in ["PERSON", "LOCATION", "STREET_ADDRESS"]:
                for whitelisted_term in self.whitelist:
                    if whitelisted_term in detected_text.lower():
                        logger.debug(f"Whitelist-Partial-Match: '{detected_text}' enthält '{whitelisted_term}'")
                        removed_count += 1
                        is_whitelisted = True
                        break

            if not is_whitelisted:
                filtered_results.append(result)

        if removed_count > 0:
            logger.info(f"Whitelist: {removed_count} Entities ausgeschlossen")

        return filtered_results

    def _create_nlp_engine(self):
        """Erstellt NLP-Engine basierend auf Modus"""
        if self.recognition_mode == 'fast':
            # Dummy Engine: Nur Pattern-Matching (schnell)
            logger.info("Verwende Dummy NLP Engine (nur Patterns, schnell)")
            return DummyNlpEngine()

        elif self.recognition_mode in ['balanced', 'accurate']:
            # Versuche spaCy zu laden
            try:
                logger.info(f"Versuche spaCy zu laden für Modus '{self.recognition_mode}'...")

                # Lade deutsches Modell
                model_name = "de_core_news_sm"  # Klein für balanced
                if self.recognition_mode == 'accurate':
                    # Versuche großes Modell für accurate
                    try:
                        import spacy
                        spacy.load("de_core_news_lg")
                        model_name = "de_core_news_lg"
                        logger.info("Verwende großes spaCy-Modell (genauer, langsamer)")
                    except:
                        logger.warning("Großes Modell nicht gefunden, nutze kleines Modell")

                nlp_engine = SpacyNlpEngine(models=[{"lang_code": "de", "model_name": model_name}])
                logger.info(f"spaCy NLP Engine geladen: {model_name}")
                return nlp_engine

            except Exception as e:
                logger.warning(f"Konnte spaCy nicht laden: {e}")
                logger.warning("Falle zurück auf Dummy Engine (nur Patterns)")
                logger.warning("Installiere spaCy für bessere Erkennung:")
                logger.warning("  pip install spacy")
                logger.warning("  python -m spacy download de_core_news_sm")
                return DummyNlpEngine()

        else:
            logger.warning(f"Unbekannter Modus '{self.recognition_mode}', nutze 'fast'")
            return DummyNlpEngine()

    def initialize(self):
        """Initialisiert Presidio Engines (kann etwas dauern beim ersten Start)"""
        try:
            logger.info("Initialisiere Presidio Analyzer...")
            logger.info(f"Modus: {self.recognition_mode}")
            start_time = time.time()

            # Erstelle Registry mit allen Patterns
            registry = self._create_registry()

            # Erstelle NLP Engine basierend auf Modus
            nlp_engine = self._create_nlp_engine()

            # Erstelle Analyzer
            # Sprache muss konsistent mit Registry sein (alle Recognizers nutzen "en")
            self.analyzer = AnalyzerEngine(
                registry=registry,
                nlp_engine=nlp_engine,
                supported_languages=["en"]  # Patterns funktionieren auch für deutsche Texte
            )

            logger.info("Initialisiere Presidio Anonymizer...")
            self.anonymizer = AnonymizerEngine()

            # Registriere Custom Operators (Klassen, nicht Instanzen!)
            self.anonymizer.add_anonymizer(FirstLetterOperator)
            self.anonymizer.add_anonymizer(StreetFirstLetterOperator)
            self.anonymizer.add_anonymizer(LocationFirstLetterOperator)
            self.anonymizer.add_anonymizer(EmailMaskOperator)
            self.anonymizer.add_anonymizer(PhoneMaskOperator)
            self.anonymizer.add_anonymizer(IbanMaskOperator)
            self.anonymizer.add_anonymizer(DateMaskOperator)
            self.anonymizer.add_anonymizer(CaseNumberMaskOperator)

            elapsed = time.time() - start_time
            logger.info(f"Presidio erfolgreich initialisiert! ({elapsed:.1f}s)")
            return True
        except Exception as e:
            logger.error(f"Fehler beim Initialisieren von Presidio: {e}", exc_info=True)
            return False

    def _normalize_multiline_names(self, text: str) -> str:
        """
        Normalisiert mehrzeilige Namen für bessere Erkennung

        Problem: Namen mit Titel stehen auf eigener Zeile, dann kommen Details:
        "Herr Maximilian Josef Müller-Hoffmann\n   geb. am ..."

        Lösung: Entferne übermäßige Leerzeichen nach Namen
        """
        # Erstes Problem: Nach einem vollen Namen (Herr + Vornamen + Nachname)
        # kommt oft ein Newline mit vielen Leerzeichen für Einrückung
        # z.B. "Herr Max Müller\n   geb. am ..." → "Herr Max Müller geb. am ..."

        # Aber: Wir wollen nur Namen-Zeilen normalisieren, nicht alles!
        # Lösung: Ersetze "\n   " (Newline + 3+ Leerzeichen) mit einem Leerzeichen
        # NUR wenn davor ein Nachname steht (erkennbar an Großbuchstabe-Kleinbuchstaben)
        normalized = re.sub(
            r'([A-ZÄÖÜ][a-zäöüß]+(-[A-ZÄÖÜ][a-zäöüß]+)?)\n\s{2,}',
            r'\1 ',
            text
        )

        return normalized

    def anonymize(self, text: str, entities_to_anonymize: Optional[List[str]] = None) -> str:
        """
        Anonymisiert den gegebenen Text

        Args:
            text: Der zu anonymisierende Text
            entities_to_anonymize: Liste von Entity-Typen die anonymisiert werden sollen.
                                   None = alle unterstützten Entities (siehe DEFAULT_ENTITIES)

        Returns:
            Anonymisierter Text
        """
        if not text or not text.strip():
            return text

        # Default: Alle unterstützten Entity-Typen
        if entities_to_anonymize is None:
            entities_to_anonymize = [
                # Persönliche Daten
                "PERSON",                    # Namen (mit Pattern + spaCy)
                "EMAIL_ADDRESS",             # E-Mails
                "PHONE_NUMBER",              # Telefonnummern
                "DATE_TIME",                 # Geburtsdaten, Termine

                # Adressen & Orte
                "STREET_ADDRESS",            # Straßen (Musterstraße 123)
                "LOCATION",                  # PLZ + Städte (12345 Berlin)

                # Finanz-Daten
                "IBAN_CODE",                 # IBAN
                "CREDIT_CARD",               # Kreditkarten
                "ACCOUNT_NUMBER",            # Kontonummern

                # Identifikation
                "TAX_ID",                    # Steuer-ID / Steuernummer
                "SOCIAL_SECURITY_NUMBER",    # Sozialversicherungsnummer
                "ID_NUMBER",                 # Ausweis-/Personalausweisnummer

                # Juristische Daten
                "CASE_NUMBER",               # Aktenzeichen (123 C 456/2024)
                "PROPERTY_REF",              # Grundbuchnummern
                "LAND_PARCEL",               # Flurstücknummern

                # Internet
                "IP_ADDRESS",                # IP-Adressen
                "URL",                       # URLs/Webseiten
            ]
            logger.info(f"Verwende Standard-Entities: {len(entities_to_anonymize)} Typen")

        if not self.analyzer or not self.anonymizer:
            logger.warning("Presidio nicht initialisiert, initialisiere jetzt...")
            if not self.initialize():
                return "FEHLER: Presidio konnte nicht initialisiert werden!"

        try:
            # Normalisiere mehrzeilige Namen VORHER
            text_normalized = self._normalize_multiline_names(text)

            # Analysiere Text und erkenne PII (nutze normalisierten Text!)
            logger.info(f"Analysiere Text ({len(text)} Zeichen)...")
            start_analyze = time.time()
            analyzer_results = self.analyzer.analyze(
                text=text_normalized,  # Nutze normalisierten Text für Analyse
                language="en",  # Muss konsistent mit Registry sein
                entities=entities_to_anonymize
            )
            analyze_time = time.time() - start_analyze

            logger.info(f"{len(analyzer_results)} PII-Entities gefunden (Analyse: {analyze_time:.2f}s)")

            # Filtere Whitelist-Einträge (nutze normalisierten Text!)
            analyzer_results = self._filter_whitelist(text_normalized, analyzer_results)
            logger.info(f"{len(analyzer_results)} PII-Entities nach Whitelist-Filter")

            # Filtere nach Confidence-Score (konfigurierbar via config.toml)
            # Thresholds aus Config: person_threshold, other_threshold
            analyzer_results = [
                r for r in analyzer_results
                if (r.entity_type == "PERSON" and r.score >= self.person_threshold) or
                   (r.entity_type != "PERSON" and r.score >= self.other_threshold)
            ]
            logger.info(f"{len(analyzer_results)} PII-Entities nach Score-Filter (>={self.person_threshold} für Namen, >={self.other_threshold} für andere)")

            # Anonymisiere erkannte PII (nutze normalisierten Text!)
            # Namen werden zu "X." (erster Buchstabe + Punkt)
            # Andere werden komplett ersetzt
            start_anonymize = time.time()
            anonymized_result = self.anonymizer.anonymize(
                text=text_normalized,  # Nutze normalisierten Text!
                analyzer_results=analyzer_results,
                operators={
                    "DEFAULT": OperatorConfig("replace", {"new_value": "***"}),
                    "PERSON": OperatorConfig("first_letter"),  # Custom: "Herr Müller" → "Herr M."
                    "STREET_ADDRESS": OperatorConfig("street_first_letter"),  # Custom: "Musterstr. 123" → "M.str. 123"
                    "LOCATION": OperatorConfig("location_first_letter"),  # Custom: "12345 Berlin" → "XXXXX B."
                    "EMAIL_ADDRESS": OperatorConfig("email_mask"),  # Custom: "max@firma.de" → "***@***.de"
                    "PHONE_NUMBER": OperatorConfig("phone_mask"),  # Custom: "030 123456" → "030 XXXXXX"
                    "DATE_TIME": OperatorConfig("date_mask"),  # Custom: "15.03.2024" → "XX.03.2024"
                    "IBAN_CODE": OperatorConfig("iban_mask"),  # Custom: "DE89 3704..." → "DE** ****"
                    "CASE_NUMBER": OperatorConfig("case_number_mask"),  # Custom: "123 C 456/2024" → "*** C ***/2024"
                    "CREDIT_CARD": OperatorConfig("replace", {"new_value": "**** **** ****"}),
                    "IP_ADDRESS": OperatorConfig("replace", {"new_value": "***.***.***.***"}),
                    "URL": OperatorConfig("replace", {"new_value": "www.***.***"}),
                    "TAX_ID": OperatorConfig("replace", {"new_value": "**/***/****"}),
                    "SOCIAL_SECURITY_NUMBER": OperatorConfig("replace", {"new_value": "** ****** * ***"}),
                    "ID_NUMBER": OperatorConfig("replace", {"new_value": "*********"}),
                    "ACCOUNT_NUMBER": OperatorConfig("replace", {"new_value": "Konto-Nr.: *******"}),
                    "PROPERTY_REF": OperatorConfig("replace", {"new_value": "GB ****/***-***"}),  # Grundbuch
                    "LAND_PARCEL": OperatorConfig("replace", {"new_value": "Flurstück ***/***"}),  # Flurstück
                }
            )
            anonymize_time = time.time() - start_anonymize

            total_time = analyze_time + anonymize_time
            logger.info(f"Text erfolgreich anonymisiert (Anonymisierung: {anonymize_time:.2f}s, Gesamt: {total_time:.2f}s)")
            return anonymized_result.text

        except Exception as e:
            logger.error(f"Fehler beim Anonymisieren: {e}", exc_info=True)
            return f"FEHLER beim Anonymisieren: {str(e)}\n\n(Originaltext wurde NICHT anonymisiert)"


# Singleton Instance
_anonymizer_instance = None

def get_anonymizer() -> TextAnonymizer:
    """Gibt die Singleton-Instanz des Anonymizers zurück"""
    global _anonymizer_instance
    if _anonymizer_instance is None:
        _anonymizer_instance = TextAnonymizer(language="de")
    return _anonymizer_instance
