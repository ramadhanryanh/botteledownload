import telebot
import yt_dlp
import os

# JANGAN UBAH KODE INI, KITA AKAN MASUKKAN TOKEN DI RENDER NANTI
TOKEN = os.environ.get('BOT_TOKEN')
YOUR_CHAT_ID = os.environ.get('MY_CHAT_ID')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if str(message.chat.id) != YOUR_CHAT_ID:
        bot.reply_to(message, "Maaf, ini bot pribadi.")
        return
    bot.reply_to(message, "Halo! Kirimkan link video yang ingin didownload (Max 50MB karena aturan Telegram).")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    if str(message.chat.id) != YOUR_CHAT_ID:
        return

    url = message.text
    proses_msg = bot.reply_to(message, "⏳ Sedang mencoba mendownload... Tunggu sebentar.")

    # Pengaturan Download
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video_downloaded.%(ext)s',
        'max_filesize': 50000000, # Batas 50MB
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        bot.edit_message_text("✅ Video berhasil didownload! Sedang mengirim ke Telegram...", chat_id=message.chat.id, message_id=proses_msg.message_id)
        
        with open(filename, 'rb') as video_file:
            bot.send_video(message.chat.id, video_file)
            
        os.remove(filename) # Hapus video dari server agar memori tidak penuh
        
    except Exception as e:
        bot.edit_message_text(f"❌ Gagal. Kemungkinan file lebih dari 50MB, atau situs tersebut memblokir bot.\n\nError teknis: {str(e)[:100]}", chat_id=message.chat.id, message_id=proses_msg.message_id)

bot.infinity_polling()
