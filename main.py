import requests
import time

# Configuration
DOMAIN = "YOUR DOMAIN HERE"  # Replace with the domain you want to monitor
CHECK_INTERVAL = 20  # Time in seconds between checks
TELEGRAM_BOT_TOKEN = "YOUR TELEGRAM API HERE"  # Replace with your bot's API token
TELEGRAM_CHAT_ID = "YOUR TELEGRAM CHAT ID HERE"  # Replace with the chat ID where alerts should be sent
ALERT_COOLDOWN = 1200  # Cooldown period in seconds (20 minutes)

# Global state
time_of_last_alert = 0
was_down = False  # Track if the domain was previously down

def send_telegram_alert(message):
    """Send an alert message to a Telegram bot."""
    global time_of_last_alert
    current_time = time.time()
    # Check if cooldown period has passed for down alerts
    if "down" in message.lower() and current_time - time_of_last_alert < ALERT_COOLDOWN:
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
        time_of_last_alert = current_time  # Update the last alert time for down alerts
        print(f"Alert sent: {message}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram alert: {e}")

def check_website():
    """Check the status of the website."""
    global was_down
    try:
        response = requests.get(DOMAIN, timeout=10)
        if response.status_code == 200:
            print(f"{DOMAIN} is up.")
            if was_down:  # If it was down before, send a restored alert
                send_telegram_alert(f"{DOMAIN} is restored and currently accessible.")
                was_down = False  # Reset the flag
        else:
            print(f"{DOMAIN} returned status code {response.status_code}.")
            if not was_down:  # Only send down alert if not already down
                send_telegram_alert(f"{DOMAIN} is down! Status code: {response.status_code}")
                was_down = True
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {DOMAIN}: {e}")
        if not was_down:  # Only send down alert if not already down
            send_telegram_alert(f"{DOMAIN} is down! Error: {e}")
            was_down = True

if __name__ == "__main__":
    while True:
        check_website()
        time.sleep(CHECK_INTERVAL)
