#!/usr/bin/env python3
import requests

from telegram import Update
from telegram.ext import ContextTypes


def retrieve_joke() -> str:
    """Fetch a joke from blague-api.vercel.app and format it."""
    resp = requests.get("https://blague-api.vercel.app/api?mode=global", timeout=10)
    resp.raise_for_status()
    data = resp.json()
    blague = data.get("blague") or ""
    reponse = data.get("reponse") or ""
    if not blague and not reponse:
        return "Pas de blague disponible pour le moment."
    if reponse:
        return f"{blague}\n\n{reponse}"
    return blague


async def give_joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    try:
        text = retrieve_joke()
    except Exception:
        text = "Impossible de récupérer une blague pour le moment."
    await update.message.reply_text(text)


async def give_blc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    await update.message.reply_text("On s'en bat les couilles ♫ ")


async def get_chatte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    site = requests.get("http://random.cat/meow")
    html = site.text
    print(html)
    photo = re.search('http[^"]*', html)
    photo = photo.group()
    photo = re.sub(r"\\", "", photo)
    await update.message.reply_photo(photo=photo)

async def get_chienne(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    site = requests.get("http://random.dog/")
    html = site.content
    soup = BeautifulSoup(html, 'html.parser')
    photo = soup.findAll("img")[0].get('src')
    photo = "http://random.dog/" + photo
    await update.message.reply_photo(photo=photo)

async def send_kappa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    await update.message.reply_photo(photo='https://pbs.twimg.com/media/B-wgfCWWkAAyWa_.jpg')