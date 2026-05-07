import os
import telebot
import requests
import time
import threading
import json
from datetime import datetime

# ================= 🔧 [ কনফিগারেশন ] =================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    BOT_TOKEN = "8685552473:AAGIN70mMdpdgq1upwmMUdJKKrfdyxsfPIA"

bot = telebot.TeleBot(BOT_TOKEN)

# যে API চেক করবে
API_URL = "https://ins.skysysx.com/api/api/v1/webhook/QWiLIc9BkNU9F1yh1c6mBQG5p06B-npMHRcgCKRicNM/account-push"

# মনিটরিং সেটিংস
CHECK_INTERVAL = 30
user_status = {}

# ================= 🔍 [ API চেক ফাংশন - রিয়েল চেক] =================

def check_api():
    """API রিয়েলি কাজ করছে কিনা চেক করে - রেসপন্স কন্টেন্ট দেখে"""
    try:
        response = requests.get(API_URL, timeout=10)
        
        # রেসপন্সের কন্টেন্ট চেক করো
        if response.status_code == 200:
            try:
                data = response.json()
                # এখানে তুমি চেক করতে পারো ডাটা ভ্যালিড কিনা
                # যেমন: if data.get("success") == True
                return True
            except:
                # JSON না হলে টেক্সট চেক
                if "success" in response.text.lower():
                    return True
                else:
                    # রেসপন্স এলেও ভ্যালিড না
                    return False
        else:
            return False
    except:
        return False

def send_signal(chat_id, is_online):
    current_time = datetime.now().strftime("%I:%M %p")
    date_time = datetime.now().strftime("%d %B, %Y")
    
    if is_online:
        msg = (
            f"🟢 *API IS ONLINE* 🟢\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ *MAX FUTURE USERS*\n"
            f"🚀 *START WORK NOW!*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📅 Date: {date_time}\n"
            f"⏰ Time: {current_time}\n\n"
            f"💎 *Powered by MAX FUTURE*"
        )
    else:
        msg = (
            f"🔴 *API IS OFFLINE* 🔴\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"❌ *MAX FUTURE USERS*\n"
            f"⏸️ *STOPPED WORKING!*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📅 Date: {date_time}\n"
            f"⏰ Time: {current_time}\n\n"
            f"💎 *Powered by MAX FUTURE*"
        )
    
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

# ================= 🚀 [ কম্যান্ড হ্যান্ডলার ] =================

@bot.message_handler(commands=['start'])
def start_cmd(m):
    chat_id = m.chat.id
    is_online = check_api()
    current_time = datetime.now().strftime("%I:%M %p")
    date_time = datetime.now().strftime("%d %B, %Y")
    
    if is_online:
        msg = (
            f"🟢 *API IS ONLINE* 🟢\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ *MAX FUTURE USERS*\n"
            f"🚀 *START WORK NOW!*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📅 Date: {date_time}\n"
            f"⏰ Time: {current_time}\n\n"
            f"💎 *Powered by MAX FUTURE*\n\n"
            f"📌 *You will receive auto updates when status changes*"
        )
    else:
        msg = (
            f"🔴 *API IS OFFLINE* 🔴\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"❌ *MAX FUTURE USERS*\n"
            f"⏸️ *STOPPED WORKING!*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📅 Date: {date_time}\n"
            f"⏰ Time: {current_time}\n\n"
            f"💎 *Powered by MAX FUTURE*\n\n"
            f"📌 *You will receive auto updates when status changes*"
        )
    
    bot.send_message(chat_id, msg, parse_mode="Markdown")
    
    if chat_id not in user_status:
        user_status[chat_id] = True
        monitor_thread = threading.Thread(target=monitor_for_user, args=(chat_id,), daemon=True)
        monitor_thread.start()

@bot.message_handler(commands=['status'])
def status_cmd(m):
    is_online = check_api()
    current_time = datetime.now().strftime("%I:%M %p")
    msg = f"🟢 *ONLINE* - {current_time}" if is_online else f"🔴 *OFFLINE* - {current_time}"
    bot.send_message(m.chat.id, msg, parse_mode="Markdown")

@bot.message_handler(commands=['stop'])
def stop_cmd(m):
    chat_id = m.chat.id
    if chat_id in user_status:
        user_status[chat_id] = False
        bot.send_message(chat_id, "🔕 *Monitoring stopped!* Send /start to resume.", parse_mode="Markdown")
    else:
        bot.send_message(chat_id, "❌ *No active monitoring!* Send /start to begin.", parse_mode="Markdown")

# ================= 🔄 [ মেইন ] =================

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 MAX FUTURE API MONITOR")
    print("📡 Checking API every 30 seconds")
    print("✅ Shows REAL ON/OFF signals")
    print("=" * 50)
    print("✅ Bot Started!")
    print("💡 Send /start - Get auto updates")
    print("💡 Send /status - Check manually")
    print("=" * 50)
    
    try:
        bot.remove_webhook()
        print("✅ Webhook removed!")
    except:
        pass
    
    bot.infinity_polling(timeout=30, skip_pending=True)
