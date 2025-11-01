"""
Text Anonymisierung mit Microsoft Presidio
"""

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class TextAnonymizer:
    """Anonymisiert Text mit Presidio"""

    def __init__(self, language: str = "de"):
        """
        Initialisiert den Anonymizer

        Args:
            language: Sprache für die Analyse (de für Deutsch, en für Englisch)
        """
        self.language = language
        self.analyzer = None
        self.anonymizer = None

    def initialize(self):
        """Initialisiert Presidio Engines (kann etwas dauern beim ersten Start)"""
        try:
            logger.info("Initialisiere Presidio Analyzer...")
            self.analyzer = AnalyzerEngine()

            logger.info("Initialisiere Presidio Anonymizer...")
            self.anonymizer = AnonymizerEngine()

            logger.info("Presidio erfolgreich initialisiert!")
            return True
        except Exception as e:
            logger.error(f"Fehler beim Initialisieren von Presidio: {e}")
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
            self.initialize()

        try:
            # Analysiere Text und erkenne PII
            logger.info(f"Analysiere Text ({len(text)} Zeichen)...")
            analyzer_results = self.analyzer.analyze(
                text=text,
                language=self.language,
                entities=entities_to_anonymize
            )

            logger.info(f"{len(analyzer_results)} PII-Entities gefunden")

            # Anonymisiere erkannte PII
            anonymized_result = self.anonymizer.anonymize(
                text=text,
                analyzer_results=analyzer_results,
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
                }
            )

            logger.info("Text erfolgreich anonymisiert")
            return anonymized_result.text

        except Exception as e:
            logger.error(f"Fehler beim Anonymisieren: {e}")
            return f"FEHLER: {str(e)}\n\nOriginaltext:\n{text}"


# Singleton Instance
_anonymizer_instance = None

def get_anonymizer() -> TextAnonymizer:
    """Gibt die Singleton-Instanz des Anonymizers zurück"""
    global _anonymizer_instance
    if _anonymizer_instance is None:
        _anonymizer_instance = TextAnonymizer(language="de")
    return _anonymizer_instance
