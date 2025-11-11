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
        Ersetzt Text durch ersten Buchstaben + Punkt

        "Max Mustermann" → "M."
        "Dr. Anna Schmidt" → "D."
        "Herr Müller" → "H."
        """
        if not text or not text.strip():
            return text

        # Entferne Leerzeichen
        text = text.strip()

        # Finde ersten Buchstaben (nicht Titel wie Dr., Herr, etc.)
        # Entferne häufige Titel
        text_without_title = re.sub(r'^(Herr|Frau|Dr\.|Prof\.|Hr\.|Fr\.|Herrn)\s+', '', text)

        # Erster Buchstabe vom Rest
        if text_without_title:
            first_letter = text_without_title[0].upper()
            return f"{first_letter}."

        # Fallback: Erster Buchstabe vom Original
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
            from .config_loader import get_config
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
        phone_patterns = [
            Pattern(name="phone_mobile", regex=r"0\d{3,4}[\s\-/]?\d{3,4}[\s\-/]?\d{3,4}", score=0.8),
            Pattern(name="phone_intl", regex=r"\+49[\s\-/]?\d{2,4}[\s\-/]?\d{3,9}", score=0.8),
            Pattern(name="phone_landline", regex=r"0\d{2,5}[\s\-/]?\d{5,9}", score=0.7),
        ]
        registry.add_recognizer(PatternRecognizer(
            supported_entity="PHONE_NUMBER",
            patterns=phone_patterns,
            supported_language="en"
        ))

        # Namen (deutsche Vor- und Nachnamen)
        # WICHTIG: Nur mit Titeln oder sehr spezifische Patterns!
        name_patterns = [
            # Mit Anrede (sehr sicher)
            Pattern(
                name="name_with_title",
                regex=r"\b(Herr|Frau|Hr\.|Fr\.|Herrn)\s+(Dr\.\s+)?(Prof\.\s+)?(Dr\.\s+)?[A-ZÄÖÜ][a-zäöüß]+\s+[A-ZÄÖÜ][a-zäöüß]+(-[A-ZÄÖÜ][a-zäöüß]+)?\b",
                score=0.95
            ),
            # Mit akademischem Titel (sehr sicher)
            Pattern(
                name="name_with_dr",
                regex=r"\b(Dr\.|Prof\.|Prof\.\s+Dr\.)\s+[A-ZÄÖÜ][a-zäöüß]{3,}\s+[A-ZÄÖÜ][a-zäöüß]{3,}(-[A-ZÄÖÜ][a-zäöüß]+)?\b",
                score=0.9
            ),
            # Nur lange, untypische Namen (reduziert False Positives)
            # Mindestens 4 Buchstaben pro Wort, keine Artikel/Präpositionen
            Pattern(
                name="long_name",
                regex=r"\b[A-ZÄÖÜ][a-zäöüß]{3,}\s+[A-ZÄÖÜ][a-zäöüß]{4,}(-[A-ZÄÖÜ][a-zäöüß]+)?\b",
                score=0.75  # Erhöht von 0.65, damit es über Threshold (0.7) liegt
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
            Pattern(name="steuer_id_labeled", regex=r"\b(Steuer-ID|Steueridentifikationsnummer|St\.-Nr\.|Steuernummer):?\s*\d{10,13}\b", score=0.95),
        ]
        registry.add_recognizer(PatternRecognizer(
            supported_entity="TAX_ID",
            patterns=tax_patterns,
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

        for result in analyzer_results:
            # Extrahiere den erkannten Text
            detected_text = text[result.start:result.end]

            # Prüfe ob auf Whitelist (case-insensitive)
            if detected_text.lower() in self.whitelist:
                logger.debug(f"Whitelist-Match: '{detected_text}' wird NICHT anonymisiert")
                removed_count += 1
                continue

            # Prüfe ob ein Teil eines Whitelist-Eintrags ist
            is_whitelisted = False
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

            # Registriere Custom Operator für Namen (Klasse, nicht Instanz!)
            self.anonymizer.add_anonymizer(FirstLetterOperator)

            elapsed = time.time() - start_time
            logger.info(f"Presidio erfolgreich initialisiert! ({elapsed:.1f}s)")
            return True
        except Exception as e:
            logger.error(f"Fehler beim Initialisieren von Presidio: {e}", exc_info=True)
            return False

    def anonymize(self, text: str, entities_to_anonymize: Optional[List[str]] = None) -> str:
        """
        Anonymisiert den gegebenen Text

        Args:
            text: Der zu anonymisierende Text
            entities_to_anonymize: Liste von Entity-Typen die anonymisiert werden sollen.
                                   None = alle erkannten Entities

        Returns:
            Anonymisierter Text
        """
        if not text or not text.strip():
            return text

        if not self.analyzer or not self.anonymizer:
            logger.warning("Presidio nicht initialisiert, initialisiere jetzt...")
            if not self.initialize():
                return "FEHLER: Presidio konnte nicht initialisiert werden!"

        try:
            # Analysiere Text und erkenne PII
            logger.info(f"Analysiere Text ({len(text)} Zeichen)...")
            analyzer_results = self.analyzer.analyze(
                text=text,
                language="en",  # Muss konsistent mit Registry sein
                entities=entities_to_anonymize
            )

            logger.info(f"{len(analyzer_results)} PII-Entities gefunden")

            # Filtere Whitelist-Einträge
            analyzer_results = self._filter_whitelist(text, analyzer_results)
            logger.info(f"{len(analyzer_results)} PII-Entities nach Whitelist-Filter")

            # Filtere nach Confidence-Score (konfigurierbar via config.toml)
            # Thresholds aus Config: person_threshold, other_threshold
            analyzer_results = [
                r for r in analyzer_results
                if (r.entity_type == "PERSON" and r.score >= self.person_threshold) or
                   (r.entity_type != "PERSON" and r.score >= self.other_threshold)
            ]
            logger.info(f"{len(analyzer_results)} PII-Entities nach Score-Filter (>={self.person_threshold} für Namen, >={self.other_threshold} für andere)")

            # Anonymisiere erkannte PII
            # Namen werden zu "X." (erster Buchstabe + Punkt)
            # Andere werden komplett ersetzt
            anonymized_result = self.anonymizer.anonymize(
                text=text,
                analyzer_results=analyzer_results,
                operators={
                    "DEFAULT": OperatorConfig("replace", {"new_value": "<ANONYMISIERT>"}),
                    "PERSON": OperatorConfig("first_letter"),  # Custom: "Max" → "M."
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
                    "ACCOUNT_NUMBER": OperatorConfig("replace", {"new_value": "<KONTO-NR>"}),
                }
            )

            logger.info("Text erfolgreich anonymisiert")
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
