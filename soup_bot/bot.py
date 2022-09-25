import hikari
import lightbulb
import miru

from typing import Optional
import os
import asyncio
import time
import datetime
import platform
import psutil
import random


bot = lightbulb.BotApp(
    os.environ["TOKEN"],
    # default_enabled_guilds=int(os.environ["DEFAULT_GUILD_ID"]),
    help_slash_command=True
)

miru.load(bot)


def run() -> None:
    if os.name != "nt":
        import uvloop
        uvloop.install()

    bot.run(
        asyncio_debug=True,  # enable asyncio debug to detect blocking and slow code.
        coroutine_tracking_depth=20,  # enable tracking of coroutines, makes some asyncio errors clearer.
        propagate_interrupts=True,  # Any OS interrupts get rethrown as errors.
        status=hikari.Status.ONLINE,
        activity=hikari.Activity(
            name="to x0rtex atm",
            type=hikari.ActivityType.LISTENING
        )
    )
