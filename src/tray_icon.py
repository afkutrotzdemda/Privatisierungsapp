"""
System Tray Icon für die Anonymisierungs-App
"""

import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import logging
from typing import Callable

logger = logging.getLogger(__name__)


class TrayIcon:
    """System Tray Icon Manager"""

    def __init__(self, on_quit_callback: Callable):
        """
        Args:
            on_quit_callback: Funktion die beim Beenden aufgerufen wird
        """
        self.on_quit_callback = on_quit_callback
        self.icon = None

    def create_icon_image(self) -> Image.Image:
        """
        Erstellt ein einfaches Icon-Bild (64x64)
        Ein grünes "A" für Anonymisierung
        """
        width = 64
        height = 64

        # Erstelle ein Bild mit transparentem Hintergrund
        image = Image.new('RGB', (width, height), color='#2196F3')
        dc = ImageDraw.Draw(image)

        # Zeichne ein großes "A" in der Mitte
        # Einfache Darstellung als weißes "A"
        dc.text((width // 2 - 10, height // 2 - 15), "A", fill='white')

        # Alternativ: Zeichne einen Kreis mit A
        margin = 8
        dc.ellipse([margin, margin, width - margin, height - margin], outline='white', width=3)
        dc.text((width // 2 - 12, height // 2 - 18), "A", fill='white')

        return image

    def start(self):
        """Startet das Tray Icon"""
        try:
            logger.info("Erstelle System Tray Icon...")

            # Erstelle Icon Bild
            icon_image = self.create_icon_image()

            # Erstelle Menü
            menu = pystray.Menu(
                item(
                    'Text Anonymisierer',
                    lambda: None,
                    enabled=False
                ),
                item(
                    'Hotkey: Strg+Alt+A',
                    lambda: None,
                    enabled=False
                ),
                pystray.Menu.SEPARATOR,
                item(
                    'Status: Aktiv ✓',
                    lambda: None,
                    enabled=False
                ),
                pystray.Menu.SEPARATOR,
                item(
                    'Beenden',
                    self._on_quit
                )
            )

            # Erstelle Tray Icon
            self.icon = pystray.Icon(
                name="TextAnonymizer",
                icon=icon_image,
                title="Text Anonymisierer (Strg+Alt+A)",
                menu=menu
            )

            logger.info("Starte System Tray Icon...")
            # Blockiert bis icon.stop() aufgerufen wird
            self.icon.run()

        except Exception as e:
            logger.error(f"Fehler beim Starten des Tray Icons: {e}")
            raise

    def stop(self):
        """Stoppt das Tray Icon"""
        if self.icon:
            logger.info("Stoppe System Tray Icon...")
            self.icon.stop()

    def _on_quit(self, icon, item):
        """Wird beim Klick auf 'Beenden' aufgerufen"""
        logger.info("Beenden über Tray Icon gewählt")
        self.stop()
        self.on_quit_callback()
