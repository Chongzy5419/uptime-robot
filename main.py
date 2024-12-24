import requests
import time

# Configuration
DOMAIN = "YOUR DOMAIN HERE"  # Replace with the domain you want to monitor
CHECK_INTERVAL = 60  # Time in seconds between checks
TELEGRAM_BOT_TOKEN = "API KEY"  # Replace with your bot's API token
TELEGRAM_CHAT_ID = "ID"  # Replace with the chat ID where alerts should be sent
ALERT_COOLDOWN = 3600  # Cooldown period in seconds (1 hour)

# Global state for cooldown
time_of_last_alert = 0

def send_telegram_alert(message):
    """Send an alert message to a Telegram bot."""
    global time_of_last_alert
    current_time = time.time()
    # Check if cooldown period has passed
    if current_time - time_of_last_alert < ALERT_COOLDOWN:
        print("Cooldown period active. Skipping alert.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        time_of_last_alert = current_time  # Update the last alert time
        print(f"Alert sent: {message}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram alert: {e}")


def check_website():
    """Check the status of the website."""
    try:
        response = requests.get(DOMAIN, timeout=10)
        if response.status_code == 200:
            print(f"{DOMAIN} is up.")
        else:
            print(f"{DOMAIN} returned status code {response.status_code}.")
            send_telegram_alert(f"{DOMAIN} is down! Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {DOMAIN}: {e}")
        send_telegram_alert(f"{DOMAIN} is down! Error: {e}")


if __name__ == "__main__":
    while True:
        check_website()
        time.sleep(CHECK_INTERVAL)
