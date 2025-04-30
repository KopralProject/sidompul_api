import telegram
import subprocess
import os

# Ganti dengan token bot Telegram Anda
BOT_TOKEN = '8187353779:AAGps6cekrxUmKvYnXV9janleVGRd3wYuE8'

# Fungsi untuk menjalankan script sidompul.sh
def jalankan_sidompul(nomor_xl):
    try:
        # Pastikan script sidompul.sh ada di direktori yang sama
        proses = subprocess.run(['./sidompul.sh', nomor_xl], capture_output=True, text=True, timeout=60)
        
        # Cek jika script berhasil dijalankan
        if proses.returncode == 0:
            return proses.stdout
        else:
            return f"Error: {proses.stderr}"
    except subprocess.TimeoutExpired:
        return "Error: Script timeout"
    except FileNotFoundError:
        return "Error: sidompul.sh tidak ditemukan. Pastikan file ada di direktori yang sama."

# Fungsi untuk menangani pesan dari Telegram
def handle_message(update, context):
    chat_id = update.message.chat_id
    nomor_xl = update.message.text

    # Validasi nomor XL (contoh sederhana)
    if not nomor_xl.isdigit() or len(nomor_xl) < 10:
        context.bot.send_message(chat_id=chat_id, text="Nomor XL tidak valid.")
        return

    # Jalankan script dan dapatkan hasilnya
    hasil = jalankan_sidompul(nomor_xl)

    # Kirim hasilnya ke Telegram
    context.bot.send_message(chat_id=chat_id, text=hasil)

def main():
    # Buat bot Telegram
    bot = telegram.Bot(BOT_TOKEN)

    # Tangani pesan masuk
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Handler untuk pesan teks
    message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)
    dispatcher.add_handler(message_handler)

    # Mulai bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
