import feedparser
import time
from plyer import notification
import os

# Configuration
RSS_URL = "https://www.gouvernement.fr/rss.xml"
CHECK_INTERVAL = 3600  # toutes les heures
LAST_ENTRY_FILE = "dernier_flux.txt"

# Mots-clés déclencheurs
KEYWORDS = ["alerte", "sécurité", "crise", "urgence", "évacuation", "attaque", "guerre", "conflit", "mobilisation", "terrorisme"]

def get_last_title():
    if os.path.exists(LAST_ENTRY_FILE):
        with open(LAST_ENTRY_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

def save_last_title(title):
    with open(LAST_ENTRY_FILE, "w", encoding="utf-8") as f:
        f.write(title)

def notify(title, message):
    notification.notify(
        title="🇫🇷 Vigi Notif – " + title,
        message=message,
        timeout=10,
        app_name="Vigi Notif",
        app_icon="drapeau.ico"  # remplacez ce chemin par votre icône si souhaité
    )

def check_alert():
    print("🔎 Vérification des alertes gouvernementales...")
    feed = feedparser.parse(RSS_URL)
    if not feed.entries:
        print("⚠️ Flux vide ou inaccessible.")
        return

    latest = feed.entries[0]
    last_title = get_last_title()

    title_lower = latest.title.lower()

    # Filtrage par mot-clé
    if latest.title != last_title and any(keyword in title_lower for keyword in KEYWORDS):
        notify("Nouvelle alerte", latest.title)
        save_last_title(latest.title)
        print("✅ Alerte pertinente détectée :", latest.title)
    else:
        print("🕊️ Pas de nouvelle alerte pertinente.")

while True:
    check_alert()
    time.sleep(CHECK_INTERVAL)
