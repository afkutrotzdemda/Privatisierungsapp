"""
System Tray Icon für die Anonymisierungs-App mit Status-Farben
"""

import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import logging
from typing import Callable

logger = logging.getLogger(__name__)


class TrayIcon:
    """System Tray Icon Manager mit Farbwechsel"""

    def __init__(self, on_quit_callback: Callable):
        """
        Args:
            on_quit_callback: Funktion die beim Beenden aufgerufen wird
        """
        self.on_quit_callback = on_quit_callback
        self.icon = None
        self.current_status = 'ready'

    def create_icon_image(self, status='ready') -> Image.Image:
        """
        Erstellt ein Icon-Bild mit Statusfarbe (64x64)

        Args:
            status: 'ready' (grün), 'working' (gelb), 'error' (rot)
        """
        width = 64
        height = 64

        # Farben je nach Status
        colors = {
            'ready': '#4CAF50',    # 🟢 Grün - Bereit
            'working': '#FFC107',  # 🟡 Gelb - Anonymisiert gerade...
            'error': '#F44336'     # 🔴 Rot - Fehler
        }

        color = colors.get(status, '#4CAF50')

        # Erstelle Bild
        image = Image.new('RGB', (width, height), color=color)
        dc = ImageDraw.Draw(image)

        # Zeichne einen Kreis mit "A"
        margin = 8
        dc.ellipse([margin, margin, width - margin, height - margin], outline='white', width=4)

        # "A" für Anonymisierung - größerer Text
        try:
            from PIL import ImageFont
            # Versuche eine größere Schrift zu verwenden
            font = ImageFont.truetype("arial.ttf", 32)
            dc.text((width // 2 - 12, height // 2 - 20), "A", fill='white', font=font)
        except:
            # Fallback ohne Font - zeichne größeres A
            dc.rectangle([20, 15, 25, 45], fill='white')  # Linker Balken
            dc.rectangle([39, 15, 44, 45], fill='white')  # Rechter Balken
            dc.rectangle([20, 15, 44, 20], fill='white')  # Oberer Balken
            dc.rectangle([25, 28, 39, 32], fill='white')  # Mittlerer Balken

        return image

    def set_status(self, status: str):
        """
        Ändert den Status und aktualisiert das Icon

        Args:
            status: 'ready', 'working', oder 'error'
        """
        if self.icon and status != self.current_status:
            self.current_status = status
            new_icon = self.create_icon_image(status)
            self.icon.icon = new_icon

            # Update Title
            titles = {
                'ready': 'Text Anonymisierer - Bereit',
                'working': 'Text Anonymisierer - Anonymisiert...',
                'error': 'Text Anonymisierer - Fehler'
            }
            self.icon.title = titles.get(status, 'Text Anonymisierer')

            logger.info(f"Icon-Status geändert zu: {status}")

    def start(self):
        """Startet das Tray Icon"""
        try:
            logger.info("Erstelle System Tray Icon...")

            # Erstelle Icon Bild (startet mit grün = bereit)
            icon_image = self.create_icon_image('ready')

            # Erstelle Menü
            menu = pystray.Menu(
                item(
                    '⚖️ Text Anonymisierer',
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
                    '🟢 Status: Bereit',
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
                title="Text Anonymisierer - Bereit",
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
