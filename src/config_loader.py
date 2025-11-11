"""
Konfigurations-Loader für Anonymify

Lädt Einstellungen aus config.toml
"""

import os
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

# Fallback wenn toml nicht installiert ist
try:
    import tomli as toml
except ImportError:
    try:
        import tomllib as toml  # Python 3.11+
    except ImportError:
        logger.warning("toml/tomllib nicht gefunden, verwende manuelle TOML-Parser")
        toml = None


class Config:
    """Konfigurations-Manager"""

    DEFAULT_CONFIG = {
        'hotkey': {
            'combination': 'ctrl+alt+a'
        },
        'whitelist': {
            'court_terms': ['Gericht', 'Richter', 'Staatsanwaltschaft', 'Amtsgericht',
                           'Landgericht', 'Oberlandesgericht', 'Bundesgerichtshof'],
            'authorities': ['Finanzamt', 'Polizei', 'Bundesamt', 'Krankenkasse'],
            'professions': ['Rechtsanwalt', 'Notar', 'Steuerberater', 'Arzt'],
            'organizations': ['Deutsche Bank', 'Sparkasse', 'AOK', 'TÜV'],
            'common_words': ['Der', 'Die', 'Das', 'Im', 'Am', 'Zum', 'Zur', 'Vom', 'Bei', 'Mit', 'Durch'],
            'custom': []
        },
        'anonymization': {
            'recognition_mode': 'fast',
            'person_score_threshold': 0.7,
            'other_score_threshold': 0.6,
            'enable_person': True,
            'enable_email': True,
            'enable_phone': True,
            'enable_address': True,
            'enable_location': True,
            'enable_date': True,
            'enable_iban': True,
            'enable_account_number': True,
            'enable_case_number': True,
            'enable_tax_id': True,
            'enable_social_security': True,
            'enable_id_number': True,
            'enable_credit_card': True,
            'enable_ip_address': True,
            'enable_url': True,
        },
        'advanced': {
            'log_level': 'INFO',
            'icon_color_ready': '#4CAF50',
            'icon_color_working': '#FFC107',
            'icon_color_error': '#F44336',
            'clipboard_delay_ms': 200,
            'error_reset_seconds': 3,
        }
    }

    def __init__(self, config_path: str = 'config.toml'):
        self.config_path = config_path
        self.config = self.DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        """Lädt Konfiguration aus Datei"""
        if not os.path.exists(self.config_path):
            logger.info(f"Config-Datei nicht gefunden: {self.config_path}")
            logger.info("Verwende Standard-Konfiguration")
            self._save_default()
            return

        try:
            if toml:
                with open(self.config_path, 'rb') as f:
                    loaded_config = toml.load(f)
            else:
                loaded_config = self._parse_toml_simple(self.config_path)

            # Merge mit Default Config
            self._merge_config(loaded_config)
            logger.info(f"Konfiguration geladen: {self.config_path}")

        except Exception as e:
            logger.warning(f"Fehler beim Laden der Config: {e}")
            logger.info("Verwende Standard-Konfiguration")

    def _parse_toml_simple(self, path: str) -> Dict:
        """Einfacher TOML-Parser als Fallback"""
        config = {}
        current_section = None

        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue

                # Section header
                if line.startswith('[') and line.endswith(']'):
                    current_section = line[1:-1]
                    config[current_section] = {}
                    continue

                # Key-value pair
                if '=' in line and current_section:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    # Parse value
                    if value.startswith('[') and value.endswith(']'):
                        # Array
                        items = value[1:-1].split(',')
                        value = [item.strip().strip('"\'') for item in items if item.strip()]
                    elif value.lower() == 'true':
                        value = True
                    elif value.lower() == 'false':
                        value = False
                    elif value.isdigit():
                        value = int(value)
                    else:
                        value = value.strip('"\'')

                    config[current_section][key] = value

        return config

    def _merge_config(self, loaded: Dict):
        """Merged geladene Config mit Defaults"""
        for section, values in loaded.items():
            if section in self.config:
                if isinstance(values, dict):
                    self.config[section].update(values)
                else:
                    self.config[section] = values
            else:
                self.config[section] = values

    def _save_default(self):
        """Speichert Default-Config (wenn config.toml nicht existiert)"""
        try:
            # Wird beim ersten Start erstellt
            logger.info("Default-Config wurde bereits als config.toml erstellt")
        except Exception as e:
            logger.warning(f"Konnte Default-Config nicht speichern: {e}")

    def get_hotkey(self) -> str:
        """Gibt Hotkey-Kombination zurück"""
        return self.config['hotkey']['combination']

    def get_whitelist(self) -> List[str]:
        """Gibt komplette Whitelist zurück (alle Kategorien kombiniert)"""
        whitelist_config = self.config.get('whitelist', {})
        all_items = []

        for category in ['court_terms', 'authorities', 'professions', 'organizations', 'common_words', 'custom']:
            items = whitelist_config.get(category, [])
            all_items.extend(items)

        # Konvertiere zu lowercase für case-insensitive matching
        return [item.lower() for item in all_items]

    def is_entity_enabled(self, entity_type: str) -> bool:
        """Prüft ob Entity-Type aktiviert ist"""
        key = f"enable_{entity_type.lower()}"
        return self.config['anonymization'].get(key, True)

    def get_icon_colors(self) -> Dict[str, str]:
        """Gibt Icon-Farben zurück"""
        return {
            'ready': self.config['advanced']['icon_color_ready'],
            'working': self.config['advanced']['icon_color_working'],
            'error': self.config['advanced']['icon_color_error'],
        }

    def get_clipboard_delay(self) -> float:
        """Gibt Clipboard-Verzögerung in Sekunden zurück"""
        return self.config['advanced']['clipboard_delay_ms'] / 1000.0

    def get_error_reset_time(self) -> int:
        """Gibt Error-Reset Zeit in Sekunden zurück"""
        return self.config['advanced']['error_reset_seconds']

    def get_log_level(self) -> str:
        """Gibt Log-Level zurück"""
        return self.config['advanced']['log_level']

    def get_recognition_mode(self) -> str:
        """Gibt Erkennungs-Modus zurück (fast/balanced/accurate)"""
        return self.config['anonymization'].get('recognition_mode', 'fast')

    def get_person_score_threshold(self) -> float:
        """Gibt Score-Threshold für Namen zurück"""
        return self.config['anonymization'].get('person_score_threshold', 0.7)

    def get_other_score_threshold(self) -> float:
        """Gibt Score-Threshold für andere Entities zurück"""
        return self.config['anonymization'].get('other_score_threshold', 0.6)


# Globale Config-Instanz
_config_instance = None

def get_config() -> Config:
    """Gibt globale Config-Instanz zurück (Singleton)"""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance
