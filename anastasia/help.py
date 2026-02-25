#!/usr/bin/env python3

from telegram import Update
from telegram.ext import ContextTypes


async def give_credits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    await update.message.reply_text(
        "Je suis open source, viens m'inspecter ici : https://github.com/Anastadev/anastasia"
    )
