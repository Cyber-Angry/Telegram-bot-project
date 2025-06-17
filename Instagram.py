import os
import yt_dlp
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from uuid import uuid4
from session_links import insta_links


# 🎯 Create inline buttons for download options
def build_instagram_buttons(url):
    uid = str(uuid4())[:8]
    insta_links[uid] = url

    buttons = [
        [InlineKeyboardButton("🎞️ 720p Video", callback_data=f"insta|720|{uid}")],
        [InlineKeyboardButton("🎞️ 1080p Video", callback_data=f"insta|1080|{uid}")],
        [InlineKeyboardButton("🎞️ 2K Video", callback_data=f"insta|2k|{uid}")],
        [InlineKeyboardButton("🎧 128k MP3", callback_data=f"insta|128|{uid}")],
        [InlineKeyboardButton("🎧 276k MP3", callback_data=f"insta|276|{uid}")],
        [InlineKeyboardButton("🎧 320k MP3", callback_data=f"insta|320|{uid}")]
    ]
    return InlineKeyboardMarkup(buttons)


# 📥 Download function
def download_instagram_format(url, quality="720"):
    unique_id = str(uuid4())[:6]
    os.makedirs("downloads", exist_ok=True)
    out_file = f"downloads/insta_{unique_id}"

    # Base yt-dlp options
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'outtmpl': f'{out_file}.%(ext)s',
    }

    # Audio quality handling
    if quality in ["128", "276", "320"]:
        ydl_opts.update({
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality,
            }]
        })
    else:
        # Video quality handling (attempting best possible)
        ydl_opts.update({
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Return the downloaded file path
        for file in os.listdir("downloads"):
            if file.startswith(f"insta_{unique_id}") and (
                file.endswith(".mp4") or file.endswith(".mp3")
            ):
                return os.path.join("downloads", file)

    except Exception as e:
        print(f"[Instagram] ❌ Error downloading {url}: {e}")

    return None