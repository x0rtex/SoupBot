import hikari
import lightbulb
import miru
import inspirobot
from typing import Optional
import logging
import os
import asyncio
import time
import datetime
import platform
import psutil
import random

bot = lightbulb.BotApp(
    os.environ["TOKEN"],
    default_enabled_guilds=int(os.environ["DEFAULT_GUILD_ID"]),
    help_slash_command=True,
    logs={
        "version": 1,
        "incremental": True,
        "loggers": {
            "hikari": {"level": "INFO"},
            "hikari.ratelimits": {"level": "TRACE_HIKARI"},
            "lightbulb": {"level": "DEBUG"},
        }
    }
)

miru.load(bot)


@bot.command()
@lightbulb.command("debug", "Debug")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def cmd_group_debug() -> None:
    pass


@cmd_group_debug.child()
@lightbulb.add_cooldown(5.0, 1, lightbulb.GuildBucket)
@lightbulb.command("ping", "Pong!")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def cmd_ping(ctx: lightbulb.SlashContext) -> None:
    await ctx.respond(f"Ping: **{bot.heartbeat_latency * 1000:0.0f}ms**")


@cmd_group_debug.child()
@lightbulb.add_cooldown(5.0, 1, lightbulb.GuildBucket)
@lightbulb.command("stats", "Displays the bot's statistics")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def cmd_stats(ctx: lightbulb.SlashContext) -> None:
    embed_msg = hikari.Embed(title="Bot Statistics")
    embed_msg.set_thumbnail(ctx.user.avatar_url)

    proc = psutil.Process()
    with proc.oneshot():
        uptime = datetime.timedelta(seconds=time.time() - proc.create_time())
        cpu_time = datetime.timedelta(seconds=(cpu := proc.cpu_times()).system + cpu.user)
        mem_total = psutil.virtual_memory().total / (1024 ** 2)
        mem_of_total = proc.memory_percent()
        mem_usage = mem_total * (mem_of_total / 100)
    fields = [
        ("Python version", platform.python_version(), True),
        ("Hikari-py version", hikari.__version__, True),
        ("Uptime", uptime, True),
        ("CPU time", cpu_time, True),
        ("Memory usage", f"{mem_usage:,.0f} MiB / {mem_total:,.0f} MiB ({mem_of_total:,.0f}%)", True),
        ("Servers", len(bot.cache.get_guilds_view()), True)
    ]
    for name, value, inline in fields:
        embed_msg.add_field(name=name, value=value, inline=inline)
    await ctx.respond(embed=embed_msg)


@bot.command()
@lightbulb.add_cooldown(5.0, 1, lightbulb.GuildBucket)
@lightbulb.option("question", "question", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command("8ball", "Use the magic 8 ball to seek fortune or advice!")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_8ball(ctx: lightbulb.Context) -> None:
    responses = ("As I see it, yes.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don’t count on it.",
                 "It is certain.",
                 "It is decidedly so.",
                 "Most likely.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Outlook good.",
                 "Reply hazy, try again.",
                 "Signs point to yes.",
                 "Very doubtful.",
                 "Without a doubt.",
                 "Yes.",
                 "Yes – definitely.",
                 "You may rely on it."
                 )
    await ctx.respond(f"🎱 **{random.choice(responses)}**")


@bot.command()
@lightbulb.add_cooldown(5.0, 1, lightbulb.GuildBucket)
@lightbulb.command("quote", "Become inspired with a high quality inspirational quote")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_quote(ctx: lightbulb.Context) -> None:
    quote = inspirobot.generate()
    await ctx.respond(attachment=quote.url)


@bot.command()
@lightbulb.add_cooldown(5.0, 1, lightbulb.GuildBucket)
@lightbulb.command("flow", "Become a master in the art of mindfulness with a high quality lesson")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_flow(ctx: lightbulb.Context) -> None:
    embed_msg = hikari.Embed(title="⠀")
    flow = inspirobot.flow()
    for quote in flow:
        embed_msg.add_field(name=quote.text, value="⠀")
    await ctx.respond(embed_msg)


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
            name="x0rtex atm",
            type=hikari.ActivityType.LISTENING
        )
    )
