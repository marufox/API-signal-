import os
import telebot
import requests
import time
import threading
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise Exception("BOT_TOKEN environment variable not set!")

bot = telebot.TeleBot(BOT_TOKEN)

API_URL = "https://ins.skysysx.com/api/api/v1/webhook/QWiLIc9BkNU9F1yh1c6mBQG5p06B-npMHRcgCKRicNM/account-push"
CHECK_INTERVAL = 30
user_status = {}

def check_api():
    try:
        response = requests.get(API_URL, timeout=10)
        return response.status_code == 200
    except:
        return False

def send_signal(chat_id, is_online):
    current_time = datetime.now().strftime("%I:%M %p")
    date_time = datetime.now().strftime("%d %B, %Y")
    if is_online:
        msg = (f"🟢 *API IS ONLINE* 🟢\n━━━━━━━━━━━━━━━━━━━━\n✅ *MAX FUTURE USERS*\n🚀 *START WORK NOW!*\n━━━━━━━━━━━━━━━━━━━━\n📅 Date: {date_time}\n⏰ Time: {current_time}\n\n💎 *Powered by MAX FUTURE*")
    else:
        msg = (f"🔴 *API IS OFFLINE* 🔴\n━━━━━━━━━━━━━━━━━━━━\n❌ *MAX FUTURE USERS*\n⏸️ *STOPPED WORKING!*\n━━━━━━━━━━━━━━━━━━━━\n📅 Date: {date_time}\n⏰ Time: {current_time}\n\n💎 *Powered by MAX FUTURE*")
    try:
        bot.send_message(chat_id, msg, parse_mode="Markdown")
    except:
        pass

def monitor_for_user(chat_id):
    previous_status = None
    while True:
        try:
            current_status = check_api()
            if current_status != previous_status:
                send_signal(chat_id, current_status)
                previous_status = current_status
            time.sleep(CHECK_INTERVAL)
        except:
            time.sleep(CHECK_INTERVAL)

@bot.message_handler(commands=['start'])
def start_cmd(m):
    chat_id = m.chat.id
    is_online = check_api()
    current_time = datetime.now().strftime("%I:%M %p")
    date_time = datetime.now().strftime("%d %B, %Y")
    if is_online:
        msg = (f"🟢 *API IS ONLINE* 🟢\n━━━━━━━━━━━━━━━━━━━━\n✅ *MAX FUTURE USERS*\n🚀 *START WORK NOW!*\n━━━━━━━━━━━━━━━━━━━━\n📅 Date: {date_time}\n⏰ Time: {current_time}\n\n💎 *Powered by MAX FUTURE*\n\n📌 *Bot will notify you when status changes*")
    else:
        msg = (f"🔴 *API IS OFFLINE* 🔴\n━━━━━━━━━━━━━━━━━━━━\n❌ *MAX FUTURE USERS*\n⏸️ *STOPPED WORKING!*\n━━━━━━━━━━━━━━━━━━━━\n📅 Date: {date_time}\n⏰ Time: {current_time}\n\n💎 *Powered by MAX FUTURE*\n\n📌 *Bot will notify you when status changes*")
    bot.send_message(chat_id, msg, parse_mode="Markdown")
    if chat_id not in user_status:
        user_status[chat_id] = True
        monitor_thread = threading.Thread(target=monitor_for_user, args=(chat_id,), daemon=True)
        monitor_thread.start()

@bot.message_handler(commands=['status'])
def status_cmd(m):
    is_online = check_api()
    current_time = datetime.now().strftime("%I:%M %p")
    msg = f"🟢 ONLINE - {current_time}" if is_online else f"🔴 OFFLINE - {current_time}"
    bot.send_message(m.chat.id, msg, parse_mode="Markdown")

@bot.message_handler(commands=['stop'])
def stop_cmd(m):
    chat_id = m.chat.id
    if chat_id in user_status:
        user_status[chat_id] = False
        bot.send_message(chat_id, "🔕 Monitoring stopped! Send /start to resume.", parse_mode="Markdown")
    else:
        bot.send_message(chat_id, "❌ No active monitoring! Send /start to begin.", parse_mode="Markdown")

if __name__ == "__main__":
    print("Starting MAX FUTURE API MONITOR...")
    try:
        bot.remove_webhook()
        print("Webhook cleared.")
    except Exception as e:
        print("Webhook cleanup skipped.")
    bot.infinity_polling(timeout=30, skip_pending=True)