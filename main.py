"""
Text Anonymisierer - Hauptprogramm

Drücke Strg+Alt+A um Text aus der Zwischenablage zu anonymisieren.
"""

import sys
import logging
import threading
from src.anonymizer import get_anonymizer
from src.hotkey_handler import HotkeyHandler
from src.tray_icon import TrayIcon

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('anonymizer.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class TextAnonymizerApp:
    """Hauptanwendung"""

    def __init__(self):
        self.anonymizer = get_anonymizer()
        self.hotkey_handler = None
        self.tray_icon = None
        self.should_quit = False

    def initialize(self):
        """Initialisiert die Anwendung"""
        logger.info("=" * 60)
        logger.info("Text Anonymisierer wird gestartet...")
        logger.info("=" * 60)

        # Initialisiere Presidio
        logger.info("Initialisiere Presidio (kann beim ersten Start etwas dauern)...")
        if not self.anonymizer.initialize():
            logger.error("Fehler beim Initialisieren von Presidio!")
            return False

        # Erstelle Hotkey Handler
        self.hotkey_handler = HotkeyHandler(
            on_anonymize_callback=self.anonymizer.anonymize
        )

        # Erstelle Tray Icon
        self.tray_icon = TrayIcon(
            on_quit_callback=self.quit
        )

        return True

    def start(self):
        """Startet die Anwendung"""
        try:
            # Initialisiere
            if not self.initialize():
                logger.error("Initialisierung fehlgeschlagen!")
                return

            # Starte Hotkey Handler
            self.hotkey_handler.start()

            logger.info("=" * 60)
            logger.info("Text Anonymisierer läuft!")
            logger.info("Drücke Strg+Alt+A um Text zu anonymisieren")
            logger.info("=" * 60)

            # Starte Tray Icon (blockiert bis Beenden)
            self.tray_icon.start()

        except KeyboardInterrupt:
            logger.info("Programm durch Benutzer unterbrochen")
        except Exception as e:
            logger.error(f"Fehler beim Starten der Anwendung: {e}", exc_info=True)
        finally:
            self.cleanup()

    def quit(self):
        """Beendet die Anwendung"""
        logger.info("Beende Anwendung...")
        self.should_quit = True

    def cleanup(self):
        """Räumt Ressourcen auf"""
        logger.info("Räume auf...")

        if self.hotkey_handler:
            self.hotkey_handler.stop()

        if self.tray_icon:
            self.tray_icon.stop()

        logger.info("Auf Wiedersehen!")


def main():
    """Haupteinstiegspunkt"""
    app = TextAnonymizerApp()
    app.start()


if __name__ == "__main__":
    main()
