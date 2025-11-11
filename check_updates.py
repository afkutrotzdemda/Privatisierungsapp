"""
Prüft ob Updates verfügbar sind (optional beim Start)
"""
import subprocess
import sys
import os
from pathlib import Path

def check_for_updates(silent=False):
    """
    Prüft ob Updates von GitHub verfügbar sind

    Args:
        silent: Wenn True, keine Ausgabe

    Returns:
        tuple: (updates_available: bool, count: int, error: str or None)
    """
    try:
        # Prüfe ob Git verfügbar ist
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode != 0:
            return (False, 0, "Git nicht installiert")

        # Aktuellen Branch ermitteln
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=Path(__file__).parent
        )
        if result.returncode != 0:
            return (False, 0, "Kein Git Repository")

        current_branch = result.stdout.strip()

        # Fetch updates (leise)
        result = subprocess.run(
            ["git", "fetch", "origin", current_branch],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=Path(__file__).parent
        )
        if result.returncode != 0:
            return (False, 0, "Keine Verbindung zu GitHub")

        # Zähle verfügbare Updates
        result = subprocess.run(
            ["git", "rev-list", "HEAD...origin/" + current_branch, "--count"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=Path(__file__).parent
        )
        if result.returncode != 0:
            return (False, 0, "Fehler beim Zählen der Updates")

        count = int(result.stdout.strip())

        if not silent and count > 0:
            print(f"\n✨ {count} Update(s) verfügbar!")
            print("   Führe 'update.bat' aus um zu aktualisieren.\n")

        return (count > 0, count, None)

    except subprocess.TimeoutExpired:
        return (False, 0, "Timeout bei Git-Abfrage")
    except Exception as e:
        return (False, 0, f"Fehler: {str(e)}")


if __name__ == "__main__":
    # Standalone-Aufruf
    updates_available, count, error = check_for_updates(silent=False)

    if error:
        print(f"⚠️  Konnte nicht auf Updates prüfen: {error}")
        sys.exit(1)

    if updates_available:
        print(f"✅ {count} Update(s) verfügbar!")
        print("\nFühre 'update.bat' aus um zu aktualisieren.")
        sys.exit(0)
    else:
        print("✅ Du hast die neueste Version!")
        sys.exit(0)
