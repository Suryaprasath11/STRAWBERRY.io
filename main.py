
import yt_dlp
import dotenv
from typing import Final
from telegram import Update
from telegram.ext import ( Application , CommandHandler , MessageHandler , ContextTypes , filters , CallbackContext)
import os


 # Constants

USERNAME: Final = "@Bot_strawberrybot"
dotenv.load_dotenv()
TOKEN: Final = os.getenv("YOUR_TOKEN")
#Command Handlers

async def start_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello I'm Strawberry Bot, your professional video downloader!")

async def help_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Just drop a video URL, and I'll fetch it for you!")

async def clear_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    message_id = update.message.message_id

    await context.bot.delete_message(chat_id=chat_id, message_id=message_id)

    for i in range(1, 6):  
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id - i)
        except:
            pass

async def custom_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Custom command activated. Try sending a video URL!")

# Video Download Logic

def v_download(url: str) -> str:
    output_path = "video.mp4"
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path

async def send_video(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    try:
        video_path = v_download(url)
        with open(video_path, 'rb') as video:
            # time.sleep(2)
            await update.message.reply_video(video=video, supports_streaming=True, caption="Here's your video!")
            print("sent the video")
        os.remove(video_path)
    except Exception as e:
        # time.sleep(3)
            await update.message.reply_text(f"Failed to download video: {e}")
# Main Application Setup

def main():
    app = Application.builder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start_commands))
    app.add_handler(CommandHandler("help", help_commands))
    app.add_handler(CommandHandler("clear", clear_chat))
    app.add_handler(CommandHandler("custom", custom_commands))

    # Message handler for URLs
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_video))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
