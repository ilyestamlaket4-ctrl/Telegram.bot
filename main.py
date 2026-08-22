import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not url.startswith(("http://", "https://")):
        await update.message.reply_text("أرسل رابط فيديو من TikTok أو Instagram.")
        return

    await update.message.reply_text("جاري تحميل الفيديو... ⏳")

    try:
        filename = "video.%(ext)s"

        options = {
            "outtmpl": filename,
            "format": "best[ext=mp4]/best",
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            video_file = ydl.prepare_filename(info)

        with open(video_file, "rb") as video:
            await update.message.reply_video(video=video)

        os.remove(video_file)

    except Exception:
        await update.message.reply_text(
            "لم أستطع تحميل هذا الفيديو. تأكد أن الرابط عام ويعمل."
        )


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN غير موجود")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, download_video)
    )

    app.run_polling()


if __name__ == "__main__":
    main()
