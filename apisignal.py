import requests
import time
import logging
from datetime import datetime

# ======================== 📌 YOUR INFO HERE ========================
BOT_TOKEN = "8685552473:AAH_3DUNAyQsJ8LsM7aagqV9oBNfRrufyqo"       # Your bot token from BotFather
CHANNEL_ID = "-1003753611487"           # Your channel ID
API_URL = "https://ins.skysysx.com/api/api/v1/webhook/NiDEE4rwp-lxKv5HCYDznQMTMGx9Sfdmo1ZpGwowZy0/account-push"  # API to monitor (hidden from messages)
# ====================================================================

# Telegram API
SEND_MESSAGE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Track status
previous_status = None

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

def send_channel_message(message):
    """Send message to channel"""
    payload = {
        'chat_id': CHANNEL_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(SEND_MESSAGE_URL, json=payload, timeout=10)
        if response.status_code == 200:
            logging.info("✅ Message sent")
            return True
        else:
            logging.error(f"❌ Failed: {response.text}")
            return False
    except Exception as e:
        logging.error(f"❌ Error: {e}")
        return False

def check_api():
    """Check API status - Handles undefined, empty, null responses"""
    try:
        response = requests.get(API_URL, timeout=10)
        
        # Get response text
        response_text = response.text.strip().lower()
        
        # Check 1: HTTP Status Code must be 200-299
        if not (200 <= response.status_code < 300):
            logging.warning(f"🔴 DOWN | HTTP: {response.status_code}")
            return False
        
        # Check 2: Response contains 'undefined' → DOWN
        if 'undefined' in response_text:
            logging.warning(f"🔴 DOWN | Response contains 'undefined'")
            return False
        
        # Check 3: Empty response → DOWN
        if not response_text or response_text == '':
            logging.warning(f"🔴 DOWN | Empty response")
            return False
        
        # Check 4: Response is 'null' → DOWN
        if response_text == 'null':
            logging.warning(f"🔴 DOWN | Response is null")
            return False
        
        # All checks passed
        logging.info(f"🟢 UP | Status: {response.status_code}")
        return True
        
    except requests.exceptions.RequestException as e:
        logging.warning(f"🔴 DOWN | Connection error")
        return False

def get_current_time():
    """Get current time"""
    now = datetime.now()
    return now.strftime("%I:%M:%S %p").lstrip("0")

def main():
    global previous_status
    
    print("="*50)
    print("🤖 API MONITOR BOT STARTED")
    print("="*50)
    print(f"📢 Channel: MAX API SIGNAL 🚦")
    print(f"⏱️ Interval: 30 seconds")
    print("="*50)
    
    logging.info("Bot Started")
    
    # First status check
    current_status = check_api()
    previous_status = current_status
    
    # Startup message (SAME AS BEFORE)
    if current_status:
        msg = f"""🚀 <b>MONITOR ACTIVE</b> 🚀

✅ Server is currently <b>UP</b>.
⏰ Time: {get_current_time()}

────────────────
🟢 STATUS: ONLINE 🟢
────────────────

📌 Monitoring in progress..."""
    else:
        msg = f"""🚨 <b>ALERT: DOWN</b> 🚨

❌ Server is currently <b>DOWN</b>.
⏰ Time: {get_current_time()}

────────────────
🔴 STATUS: OFFLINE 🔴
────────────────

📌 Monitoring in progress..."""
    
    send_channel_message(msg)
    
    # Main loop
    while True:
        try:
            current_status = check_api()
            
            if current_status != previous_status:
                if current_status:
                    # DOWN ➜ UP (SAME MESSAGE)
                    msg = f"""🟢 <b>ALERT: BACK ONLINE</b> 🟢

✅ Server is now <b>UP</b>.
⏰ Time: {get_current_time()}

────────────────
✅ STATUS: ONLINE ✅
────────────────

✨ Everything is back to normal."""
                else:
                    # UP ➜ DOWN (SAME MESSAGE)
                    msg = f"""🚨 <b>ALERT: OFFLINE</b> 🚨

❌ Server is now <b>DOWN</b>.
⏰ Time: {get_current_time()}

────────────────
🔴 STATUS: OFFLINE 🔴
────────────────

⚠️ Please check your server immediately."""
                
                send_channel_message(msg)
                previous_status = current_status
            
            time.sleep(30)
            
        except Exception as e:
            logging.error(f"Loop error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main()
