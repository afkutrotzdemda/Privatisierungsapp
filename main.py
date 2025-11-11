"""
Anonymify - Hauptprogramm

Drücke Strg+Alt+A um Text aus der Zwischenablage zu anonymisieren.
"""

import sys
import logging
import threading
import ctypes
import platform
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


def is_admin():
    """Prüft ob das Programm mit Admin-Rechten läuft (nur Windows)"""
    if platform.system() != "Windows":
        return True  # Auf anderen Systemen nicht relevant

    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def check_admin_rights():
    """Gibt Warnung aus wenn keine Admin-Rechte vorhanden sind"""
    if not is_admin():
        logger.warning("=" * 60)
        logger.warning("WARNUNG: Programm läuft NICHT als Administrator!")
        logger.warning("=" * 60)
        logger.warning("")
        logger.warning("Der globale Hotkey (Strg+Alt+A) funktioniert möglicherweise")
        logger.warning("nicht richtig ohne Administrator-Rechte.")
        logger.warning("")
        logger.warning("LÖSUNG:")
        logger.warning("  1. Beende das Programm")
        logger.warning("  2. Rechtsklick auf start.bat")
        logger.warning("  3. Wähle 'Als Administrator ausführen'")
        logger.warning("")
        logger.warning("=" * 60)
        logger.warning("")

        # Gebe dem Benutzer 5 Sekunden zum Lesen
        import time
        time.sleep(5)

        return False
    return True


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
        logger.info("Anonymify wird gestartet...")
        logger.info("=" * 60)

        # Prüfe Admin-Rechte (für keyboard library)
        has_admin = check_admin_rights()
        if not has_admin:
            logger.info("Fahre trotzdem fort, aber Hotkey funktioniert evtl. nicht...")
            logger.info("")

        # Initialisiere Presidio
        logger.info("Initialisiere Presidio (kann beim ersten Start etwas dauern)...")
        try:
            if not self.anonymizer.initialize():
                logger.error("=" * 60)
                logger.error("FEHLER: Presidio konnte nicht initialisiert werden!")
                logger.error("=" * 60)
                logger.error("")
                logger.error("Mögliche Lösungen:")
                logger.error("  1. Führe install.bat erneut aus")
                logger.error("  2. Überprüfe Internet-Verbindung")
                logger.error("  3. Prüfe anonymizer.log für Details")
                logger.error("")
                logger.error("=" * 60)
                return False
        except Exception as e:
            logger.error("=" * 60)
            logger.error("KRITISCHER FEHLER beim Initialisieren!")
            logger.error("=" * 60)
            logger.error(f"Fehler: {e}")
            logger.error("")
            logger.error("Bitte führe install.bat erneut aus oder erstelle ein")
            logger.error("GitHub Issue mit dem Inhalt von anonymizer.log")
            logger.error("")
            logger.error("=" * 60)
            return False

        # Erstelle Tray Icon
        self.tray_icon = TrayIcon(
            on_quit_callback=self.quit
        )

        # Erstelle Hotkey Handler mit Status-Callback
        self.hotkey_handler = HotkeyHandler(
            on_anonymize_callback=self.anonymizer.anonymize,
            on_status_change=self.tray_icon.set_status  # Verbindet Hotkey mit Tray Icon
        )

        return True

    def start(self):
        """Startet die Anwendung"""
        try:
            # Initialisiere
            if not self.initialize():
                logger.error("Initialisierung fehlgeschlagen!")
                logger.error("Programm wird beendet.")
                input("\nDrücke Enter zum Beenden...")
                return

            # Starte Hotkey Handler
            try:
                self.hotkey_handler.start()
            except Exception as e:
                logger.error("=" * 60)
                logger.error("FEHLER: Hotkey konnte nicht registriert werden!")
                logger.error("=" * 60)
                logger.error(f"Fehler: {e}")
                logger.error("")
                logger.error("Mögliche Lösungen:")
                logger.error("  1. Starte als Administrator (Rechtsklick -> Als Administrator ausführen)")
                logger.error("  2. Überprüfe ob eine andere App Strg+Alt+A verwendet")
                logger.error("  3. Starte Windows neu")
                logger.error("")
                logger.error("=" * 60)
                input("\nDrücke Enter zum Beenden...")
                return

            logger.info("=" * 60)
            logger.info("Anonymify läuft!")
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
