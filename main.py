import json
import os
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# File lưu proxy
DATA_FILE = "proxy_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def validate_proxy_format(proxy):
    parts = proxy.strip().split(".")
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(p) <= 255 for p in parts)
    except:
        return False

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.strip()
    lines = message.splitlines()

    data = load_data()
    response_lines = []

    for line in lines:
        proxy = line.strip()
        if not validate_proxy_format(proxy):
            continue

        if proxy in data:
            response_lines.append(f"⚠️ Proxy {proxy} đã được sử dụng vào {data[proxy]}")
        else:
            now = datetime.now().strftime("%H:%M %d-%m-%Y")
            data[proxy] = now
            response_lines.append(f"✅ Proxy {proxy} đã được lưu lúc {now}. Chúc ông chủ thắng lớn nhé!")

    if response_lines:
        save_data(data)
        await update.message.reply_text("\n".join(response_lines))
    else:
        await update.message.reply_text("Không tìm thấy proxy hợp lệ nào trong tin nhắn.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Gửi proxy cho tôi (1 hoặc nhiều dòng). Tôi sẽ giúp lưu lại và tránh trùng lặp!")

def main():
    TOKEN = "7221833132:AAGKcnF9vwmpo-0LftQMW-k1w2EtCfY2sVo"  # <--- Thay bằng token của bạn

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot đang chạy...")
    app.run_polling()

if __name__ == "__main__":
    main()
