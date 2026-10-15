from pyrogram import Client, filters
from flask import Flask
import threading

# 1. إعدادات بوت التيليجرام ببياناتك الخاصة
app = Client(
    "my_bot",
    api_id=37374621,
    api_hash="44a0d5a9e89debc87ff791707f0055ea",
    bot_token="8986870283:AAGn6TKvqkxEKGCFLQ2ZOTK7X_6PIBGmaJA"
)

# الاستجابة لأمر /start
@app.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply_text("⚡ أهلاً بك! البوت يعمل الآن بشكل دائم على سيرفر Render بنجاح.")

# 2. إنشاء سيرفر ويب (Flask) لإرضاء متطلبات الخطة المجانية في Render
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running 24/7 successfully!"

def run_web():
    # تشغيل خادم الويب على البورت 8080
    web_app.run(host='0.0.0.0', port=8080)

# تشغيل خادم الويب في الخلفية كخيط مستقل (Thread)
threading.Thread(target=run_web, daemon=True).start()

# 3. تشغيل البوت الرئيسي
if __name__ == "__main__":
    print("⚡ جارٍ تشغيل البوت والسيرفر...")
    app.run()