from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# بيانات البوت الخاص بك
API_ID = 37374621
API_HASH = "44a0d5a9e89debc87ff791707f0055ea"
BOT_TOKEN = "8986870283:AAGn6TKvqkxEKGCFLQ2ZOTK7X_6PIBGmaJA"

app = Client("audio_forward_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

muted_users = set()

main_keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("طريقة الاستخدام ℹ️", callback_data="help_info"),
        InlineKeyboardButton("حالة البوت ⚡", callback_data="bot_status")
    ]
])

@app.on_message(filters.command("start") & filters.private)
def start(client, message):
    message.reply_text(
        "👋 أهلاً بك في بوت إدارة الخاص وتحويل الصوتيات!\n\n"
        "• لكتم شخص: أرسل كلمة (كتم) متبوعة باليوزر أو الآيدي.\n"
        "• لتحويل الصوتيات: أضف البوت إلى القروب وارفعه مشرفاً.",
        reply_markup=main_keyboard
    )

@app.on_callback_query()
def callbacks(client, callback):
    if callback.data == "help_info":
        callback.answer(
            "لكتم شخص: أرسل (كتم @username).\n"
            "لتحويل الصوتيات: أضف البوت للقروب واجعله أدمن وسيحول أي صوتية يتم إرسالها بالقروب إليك!", 
            show_alert=True
        )
    elif callback.data == "bot_status":
        callback.answer("✅ البوت يعمل 24/7 بنجاح وبدون توقف!", show_alert=True)

@app.on_message(filters.private)
def handle_private(client, message):
    if not message.from_user:
        return
        
    user_id = str(message.from_user.id)
    username = f"@{message.from_user.username}" if message.from_user.username else ""

    if user_id in muted_users or username in muted_users:
        try:
            message.delete()
        except Exception as e:
            print(f"خطأ في الحذف: {e}")
        return

    if message.text and message.text.strip().startswith("كتم"):
        parts = message.text.strip().split(maxsplit=1)
        if len(parts) > 1:
            target = parts[1].strip()
            muted_users.add(target)
            message.reply_text(f"✅ تم كتم المستخدم `{target}` بنجاح ولن تصلك رسائله.")

@app.on_message(filters.group & (filters.audio | filters.voice))
def forward_audio_from_group(client, message):
    try:
        message.forward(message.from_user.id)
        print("✅ تم تحويل ملف صوتي بنجاح.")
    except Exception as e:
        print(f"❌ خطأ أثناء التحويل: {e}")

print("⚡ البوت يعمل الآن...")
app.run()
