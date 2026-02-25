import datetime
import random
import urllib.request

import requests
from bs4 import BeautifulSoup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from anastasia.nude_storage import NudeScoreStore

T_WOMEN = "women"
T_MEN = "men"
T_BLACKLIST = [252593638]
T_MAXFORBLACKLISTED = 30

_score_store = NudeScoreStore()


async def get_nude(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    args = context.args
    photo_url = None

    if len(args) > 0 and args[0] == "men":
        site = urllib.request.urlopen("http://www.pausephp.com/monsieur/random.html")
        html = site.read().decode("iso-8859-1")
        soup = BeautifulSoup(html, "html.parser")
        nude = soup.find("div", attrs={"class": "img"})
        if nude and nude.h1 and nude.h1.img and nude.h1.img.get("src"):
            photo_url = "http://www.pausephp.com/" + nude.h1.img["src"]
    else:
        # Random day between now and ~15 years ago, using bonjourmadame.fr/YYYY/MM/DD/
        for _ in range(40):
            days_before = random.randint(0, 15 * 365)
            day = datetime.datetime.now() - datetime.timedelta(days=days_before)
            url = f"https://bonjourmadame.fr/{day.year:04d}/{day.month:02d}/{day.day:02d}/"
            resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            container = soup.find("div", attrs={"class": "post-content"}) or soup
            img = container.find("img") if container else None
            if img and img.get("src"):
                photo_url = img["src"]
                break

    if not photo_url:
        await update.message.reply_text("Impossible de récupérer une image pour le moment.")
        return

    sent = await update.message.reply_photo(
        photo=photo_url,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("👍", callback_data="nude_upvote")]]
        ),
    )

    # Register this nude for voting
    _score_store.register_nude(
        chat_id=sent.chat.id,
        message_id=sent.message_id,
        url=photo_url,
    )


async def nude_vote_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.callback_query or not update.callback_query.message:
        return
    chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id
    key = f"{chat_id}:{message_id}"
    vote = _score_store.upvote(key)
    if vote is None:
        await update.callback_query.answer("Impossible d'enregistrer le vote.", show_alert=False)
        return
    await update.callback_query.answer(f"Merci ! Score actuel : {vote.score}", show_alert=False)


async def nude_scoreboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    top = _score_store.top(limit=5)
    if not top:
        await update.message.reply_text("Aucune nude n'a encore été notée.")
        return
    lines = []
    for idx, nude in enumerate(top, start=1):
        lines.append(f"{idx}. Score {nude.score} – {nude.url}")
    await update.message.reply_text("\n".join(lines))
