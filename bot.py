import asyncio
import logging
import os
import threading
from typing import Optional

import discord
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask, jsonify
from python_aternos import Client

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "").strip()
ATERNOS_USER = os.getenv("ATERNOS_USER", "").strip()
ATERNOS_PASSWORD = os.getenv("ATERNOS_PASSWORD", "").strip()
ATERNOS_SERVER_ADDRESS = os.getenv("ATERNOS_SERVER_ADDRESS", "").strip().lower()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("aternos-bot")

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify({"status": "ok", "service": "aternos-bot"})


@app.get("/health")
def health():
    return jsonify({"status": "healthy"})


def run_flask() -> None:
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port, use_reloader=False)


def keep_alive() -> None:
    thread = threading.Thread(target=run_flask, name="health-server", daemon=True)
    thread.start()


def get_server():
    if not ATERNOS_USER or not ATERNOS_PASSWORD:
        raise RuntimeError("ATERNOS_USER e ATERNOS_PASSWORD precisam estar configuradas")

    aternos = Client.from_credentials(ATERNOS_USER, ATERNOS_PASSWORD)
    servers = aternos.list_servers()
    if not servers:
        return None

    if ATERNOS_SERVER_ADDRESS:
        for server in servers:
            if getattr(server, "address", "").lower() == ATERNOS_SERVER_ADDRESS:
                return server

    return servers[0]


async def fetch_server():
    return await asyncio.to_thread(get_server)


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


@bot.event
async def on_ready():
    logger.info("Bot conectado como %s (ID: %s)", bot.user, bot.user.id)
    logger.info("Pronto para controlar o servidor Aternos")


@bot.command(name="ajuda")
async def ajuda(ctx: commands.Context):
    await ctx.send("Comandos disponíveis: `!ligar`, `!desligar` e `!status`.")


@bot.command(name="ligar", help="Liga o servidor do Aternos")
async def ligar(ctx: commands.Context):
    await ctx.send("Tentando ligar o servidor do Aternos. Aguarde...")
    try:
        server = await fetch_server()
        if server is None:
            await ctx.send("Servidor não encontrado ou não há servidores disponíveis.")
            return

        await asyncio.to_thread(server.update)
        if str(server.status).lower() == "online":
            await ctx.send("O servidor já está ligado.")
            return

        await asyncio.to_thread(server.start)
        await ctx.send("Comando enviado. O servidor está iniciando...")
    except Exception:
        logger.exception("Erro ao ligar o servidor")
        await ctx.send("Não foi possível ligar o servidor. Consulte os logs do Render.")


@bot.command(name="desligar", help="Desliga o servidor do Aternos")
async def desligar(ctx: commands.Context):
    await ctx.send("Tentando desligar o servidor do Aternos. Aguarde...")
    try:
        server = await fetch_server()
        if server is None:
            await ctx.send("Servidor não encontrado ou não há servidores disponíveis.")
            return

        await asyncio.to_thread(server.update)
        if str(server.status).lower() == "offline":
            await ctx.send("O servidor já está desligado.")
            return

        await asyncio.to_thread(server.stop)
        await ctx.send("Comando enviado. O servidor está desligando...")
    except Exception:
        logger.exception("Erro ao desligar o servidor")
        await ctx.send("Não foi possível desligar o servidor. Consulte os logs do Render.")


@bot.command(name="status", help="Verifica o status atual do servidor do Aternos")
async def status(ctx: commands.Context):
    try:
        server = await fetch_server()
        if server is None:
            await ctx.send("Servidor não encontrado ou não há servidores disponíveis.")
            return

        await asyncio.to_thread(server.update)
        status_text = str(getattr(server, "status", "desconhecido"))
        software = str(getattr(server, "software", "desconhecido"))
        version = str(getattr(server, "version", "desconhecida"))
        players_count = getattr(server, "players_count", 0)
        players_max = getattr(server, "players_max", 0)

        embed = discord.Embed(
            title="Status do Servidor Aternos",
            color=discord.Color.green() if status_text.lower() == "online" else discord.Color.red(),
        )
        embed.add_field(name="Endereço", value=getattr(server, "address", "não informado"), inline=False)
        embed.add_field(name="Status", value=status_text.capitalize(), inline=True)
        embed.add_field(name="Software/Versão", value=f"{software} {version}", inline=True)
        embed.add_field(name="Jogadores", value=f"{players_count}/{players_max}", inline=True)
        await ctx.send(embed=embed)
    except Exception:
        logger.exception("Erro ao consultar status do servidor")
        await ctx.send("Não foi possível consultar o servidor. Consulte os logs do Render.")


def validate_environment() -> None:
    missing = [
        name
        for name, value in {
            "DISCORD_TOKEN": DISCORD_TOKEN,
            "ATERNOS_USER": ATERNOS_USER,
            "ATERNOS_PASSWORD": ATERNOS_PASSWORD,
            "ATERNOS_SERVER_ADDRESS": ATERNOS_SERVER_ADDRESS,
        }.items()
        if not value
    ]
    if missing:
        raise RuntimeError("Variáveis ausentes: " + ", ".join(missing))


if __name__ == "__main__":
    try:
        validate_environment()
        keep_alive()
        bot.run(DISCORD_TOKEN, log_handler=None)
    except Exception:
        logger.exception("Falha fatal na inicialização")
        raise
