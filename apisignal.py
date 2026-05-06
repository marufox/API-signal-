import telebot
import requests
import time
import threading
from datetime import datetime

# ================= 🔧 [ কনফিগারেশন ] =================

BOT_TOKEN = "8685552473:AAGIN70mMdpdgq1upwmMUdJKKrfdyxsfPIA"

bot = telebot.TeleBot(BOT_TOKEN)

# যে API চেক করবেন
API_URL = "https://ins.skysysx.com/api/api/v1/webhook/QWiLIc9BkNU9F1yh1c6mBQG5p06B-npMHRcgCKRicNM/account-push"

# মনিটরিং সেটিংস
CHECK_INTERVAL = 30  # 30 সেকেন্ড পর পর চেক করবে

# প্রতিটি ইউজারের শেষ স্ট্যাটাস ট্র্যাক করার জন্য
user_status = {}
user_last_state = {}

# ================= 🔍 [ API চেক ফাংশন ] =================

def check_api():
    """API অন/অফ চেক করে - শুধু 200 OK মানেই অন"""
    try:
        response = requests.get(API_URL, timeout=10)
        # শুধুমাত্র 200 Status Code মানেই সাকসেস
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def send_signal(chat_id, is_online):
    """শুধু অন/অফ সিগন্যাল পাঠায়"""
    
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
    """একটি নির্দিষ্ট ইউজারের জন্য API মনিটর করে"""
    previous_status = None
    
    while True:
        try:
            # বর্তমান স্ট্যাটাস চেক
            current_status = check_api()
            
            # স্ট্যাটাস চেঞ্জ হলে সিগন্যাল পাঠাও
            if current_status != previous_status:
                send_signal(chat_id, current_status)
                previous_status = current_status
            
            time.sleep(CHECK_INTERVAL)
            
        except Exception as e:
            time.sleep(CHECK_INTERVAL)

# ================= 🚀 [ স্টার্ট কমান্ড - একবার দিলেই চলতে থাকবে ] =================

@bot.message_handler(commands=['start'])
def start_cmd(m):
    chat_id = m.chat.id
    
    # প্রথমবার বর্তমান স্ট্যাটাস দেখাও
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
            f"📌 *Bot will notify you when status changes*"
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
            f"📌 *Bot will notify you when status changes*"
        )
    
    bot.send_message(chat_id, msg, parse_mode="Markdown")
    
    # ইউজারের জন্য আলাদা মনিটরিং থ্রেড স্টার্ট করো
    if chat_id not in user_status:
        user_status[chat_id] = True
        monitor_thread = threading.Thread(target=monitor_for_user, args=(chat_id,), daemon=True)
        monitor_thread.start()

@bot.message_handler(commands=['status'])
def status_cmd(m):
    """বর্তমান স্ট্যাটাস ম্যানুয়ালি চেক করতে"""
    is_online = check_api()
    current_time = datetime.now().strftime("%I:%M %p")
    
    if is_online:
        msg = f"🟢 *API IS ONLINE* - READY\n⏰ {current_time}"
    else:
        msg = f"🔴 *API IS OFFLINE* - NOT WORKING\n⏰ {current_time}"
    
    bot.send_message(m.chat.id, msg, parse_mode="Markdown")

@bot.message_handler(commands=['stop'])
def stop_cmd(m):
    """নিজের জন্য মনিটরিং বন্ধ করতে"""
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
    print("✅ Shows ONLY ON/OFF signals")
    print("=" * 50)
    print("✅ Bot Started!")
    print("💡 Send /start - Get auto updates")
    print("💡 Send /status - Check manually")
    print("=" * 50)
    
    # বট চালু
    bot.infinity_polling(timeout=30, skip_pending=True)