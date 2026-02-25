#!/usr/bin/env python3

from __future__ import annotations

import argparse
import locale
import os
from typing import Optional

from anastasia import airquality, confighelper, fact, help, joke, nude, roomcommand, todolist, weather
from anastasia.eat import eat_callback, new_eat
from anastasia.loghelper import log
from telegram.ext import Application, CallbackQueryHandler, CommandHandler


def _try_set_french_locale() -> None:
    # Windows machines often don't have 'fr_FR.UTF-8' installed.
    for candidate in ("fr_FR.UTF-8", "fr_FR", "French_France.1252"):
        try:
            locale.setlocale(locale.LC_TIME, candidate)
            return
        except Exception:
            continue


def _parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="anastasia", description="Anastasia Telegram bot")
    parser.add_argument(
        "token",
        nargs="?",
        help="Telegram bot API token. If omitted, TELEGRAM_TOKEN env var is used.",
    )
    parser.add_argument(
        "--config",
        dest="config_path",
        default=None,
        help="Optional legacy config file path (enables extra features like /room and webhook).",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> None:
    _try_set_french_locale()
    args = _parse_args(argv)

    token = args.token or os.environ.get("TELEGRAM_TOKEN")
    if not token:
        raise SystemExit("Missing token. Pass it as an argument or set TELEGRAM_TOKEN.")

    conf = confighelper.ConfigHelper(args.config_path) if args.config_path else None

    application = Application.builder().token(token).build()

    todo = todolist.Todo()

    # Always-available commands (no config file needed)
    application.add_handler(CommandHandler("joke", joke.give_joke))
    application.add_handler(CommandHandler("blc", joke.give_blc))
    application.add_handler(CommandHandler("todo", todo.give_todo))
    application.add_handler(CommandHandler("addtodo", todo.give_add_todo))
    application.add_handler(CommandHandler("keskonmange", new_eat))
    application.add_handler(CommandHandler("weather", weather.give_weather))
    application.add_handler(CommandHandler("airquality", airquality.give_airquality))
    application.add_handler(CommandHandler("nude", nude.get_nude))
    application.add_handler(CommandHandler("nude_scoreboard", nude.nude_scoreboard))
    application.add_handler(CommandHandler("chatte", joke.get_chatte))
    application.add_handler(CommandHandler("chienne", joke.get_chienne))
    application.add_handler(CommandHandler("kappa", joke.send_kappa))
    application.add_handler(CommandHandler("help", help.give_credits))
    application.add_handler(CommandHandler("fact", fact.give_fact))
    application.add_handler(CommandHandler("citation", fact.give_citation))

    application.add_handler(CallbackQueryHandler(eat_callback), group=0)
    application.add_handler(CallbackQueryHandler(todo.todo_callback), group=1)
    application.add_handler(CallbackQueryHandler(nude.nude_vote_callback, pattern="^nude_upvote$"), group=2)

    # Optional commands & webhook mode (legacy config file)
    if conf and conf.path_ics():
        room = roomcommand.RoomCommand(log, conf.path_ics())
        application.add_handler(CommandHandler("room", room.give_room))

    if conf and conf.get_webhook():
        application.run_webhook(
            listen="0.0.0.0",
            port=int(conf.get_webhook_port()),
            url_path=token,
            key=conf.get_webhook_private_ssl(),
            cert=conf.get_webhook_certif(),
            webhook_url=f"{conf.get_webhook_adress()}:{conf.get_webhook_port()}/{token}",
        )
    else:
        application.run_polling()
