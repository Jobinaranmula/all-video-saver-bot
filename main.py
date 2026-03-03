import telebot
import yt_dlp
import os

# Render സെറ്റിങ്‌സിൽ നിന്ന് ടോക്കൺ എടുക്കുന്നു
API_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "സ്വാഗതം! വീഡിയോ ലിങ്ക് അയക്കൂ, ഞാൻ അത് ഡൗൺലോഡ് ചെയ്ത് തരാം. 📥")

@bot.message_handler(func=lambda message: message.text.startswith('http'))
def download_video(message):
    url = message.text
    msg = bot.reply_to(message, "വീഡിയോ പരിശോധിക്കുന്നു... ദയവായി കാത്തിരിക്കൂ ⏳")
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'quiet': True,
        'no_warnings': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        with open('video.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video, caption="നിങ്ങളുടെ വീഡിയോ ഇതാ! ✅")
        
        os.remove('video.mp4')
        bot.delete_message(message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"ക്ഷമിക്കണം, വീഡിയോ ഡൗൺലോഡ് ചെയ്യാൻ പറ്റിയില്ല. \nError: {str(e)}", message.chat.id, msg.message_id)

bot.infinity_polling()
