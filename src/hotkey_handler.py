"""
Globaler Hotkey Handler für Strg+Alt+A
"""

import keyboard
import pyperclip
import logging
from typing import Callable

logger = logging.getLogger(__name__)


class HotkeyHandler:
    """Verwaltet globale Hotkeys"""

    def __init__(self, on_anonymize_callback: Callable):
        """
        Args:
            on_anonymize_callback: Funktion die aufgerufen wird wenn der Hotkey gedrückt wird
        """
        self.on_anonymize_callback = on_anonymize_callback
        self.hotkey = "ctrl+alt+a"
        self.is_running = False

    def start(self):
        """Startet den Hotkey Listener"""
        try:
            logger.info(f"Registriere Hotkey: {self.hotkey}")
            keyboard.add_hotkey(self.hotkey, self._on_hotkey_pressed)
            self.is_running = True
            logger.info("Hotkey erfolgreich registriert!")
        except Exception as e:
            logger.error(f"Fehler beim Registrieren des Hotkeys: {e}")
            raise

    def stop(self):
        """Stoppt den Hotkey Listener"""
        try:
            if self.is_running:
                keyboard.remove_hotkey(self.hotkey)
                self.is_running = False
                logger.info("Hotkey deregistriert")
        except Exception as e:
            logger.error(f"Fehler beim Deregistrieren des Hotkeys: {e}")

    def _on_hotkey_pressed(self):
        """Wird aufgerufen wenn der Hotkey gedrückt wird"""
        logger.info(f"Hotkey {self.hotkey} gedrückt!")

        try:
            # Lese Text aus Zwischenablage
            text = pyperclip.paste()

            if not text or not text.strip():
                logger.warning("Zwischenablage ist leer")
                return

            logger.info(f"Text aus Zwischenablage gelesen ({len(text)} Zeichen)")

            # Anonymisiere Text
            anonymized_text = self.on_anonymize_callback(text)

            # Schreibe anonymisierten Text zurück in Zwischenablage
            pyperclip.copy(anonymized_text)
            logger.info("Anonymisierter Text in Zwischenablage kopiert!")

        except Exception as e:
            logger.error(f"Fehler beim Verarbeiten des Hotkeys: {e}")
            # Bei Fehler trotzdem eine Nachricht in die Zwischenablage schreiben
            pyperclip.copy(f"FEHLER beim Anonymisieren: {str(e)}")
