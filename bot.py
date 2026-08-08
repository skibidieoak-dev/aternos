import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from python_aternos import Client

# Carregar variáveis de ambiente
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ATERNOS_USER = os.getenv("ATERNOS_USER")
ATERNOS_PASSWORD = os.getenv("ATERNOS_PASSWORD")
ATERNOS_SERVER_ADDRESS = os.getenv("ATERNOS_SERVER_ADDRESS")

# Configurar intents do Discord
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def get_server():
    try:
        aternos = Client.from_credentials(ATERNOS_USER, ATERNOS_PASSWORD)
        servers = aternos.list_servers()
        for serv in servers:
            if serv.address.lower() == ATERNOS_SERVER_ADDRESS.lower():
                return serv
        # Se não encontrar pelo endereço exato, retorna o primeiro se houver
        if servers:
            return servers[0]
    except Exception as e:
        print(f"Erro ao conectar no Aternos: {e}")
    return None

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user} (ID: {bot.user.id})")
    print("Pronto para controlar o servidor Aternos!")

@bot.command(name="ligar", help="Liga o servidor do Aternos")
async def ligar(ctx):
    await ctx.send("🔄 Tentando ligar o servidor do Aternos... Por favor, aguarde.")
    try:
        serv = get_server()
        if not serv:
            await ctx.send("❌ Servidor não encontrado ou erro nas credenciais do Aternos.")
            return
        
        # Verificar o status atual
        serv.update()
        if serv.status == "online":
            await ctx.send("⚠️ O servidor já está **ligado**!")
            return
        
        serv.start()
        await ctx.send("✅ Comando enviado com sucesso! O servidor está iniciando...")
    except Exception as e:
        await ctx.send(f"❌ Ocorreu um erro ao tentar ligar o servidor: `{e}`")

@bot.command(name="desligar", help="Desliga o servidor do Aternos")
async def desligar(ctx):
    await ctx.send("🔄 Tentando desligar o servidor do Aternos...")
    try:
        serv = get_server()
        if not serv:
            await ctx.send("❌ Servidor não encontrado ou erro nas credenciais do Aternos.")
            return
        
        serv.update()
        if serv.status == "offline":
            await ctx.send("⚠️ O servidor já está **desligado**!")
            return
        
        serv.stop()
        await ctx.send("✅ Comando enviado com sucesso! O servidor está desligando...")
    except Exception as e:
        await ctx.send(f"❌ Ocorreu um erro ao tentar desligar o servidor: `{e}`")

@bot.command(name="status", help="Verifica o status atual do servidor do Aternos")
async def status(ctx):
    try:
        serv = get_server()
        if not serv:
            await ctx.send("❌ Servidor não encontrado ou erro nas credenciais do Aternos.")
            return
        
        serv.update()
        status_text = serv.status
        software = serv.software
        version = serv.version
        players_count = f"{serv.players_count}/{serv.players_max}"
        
        embed = discord.Embed(title="status do Servidor Aternos", color=discord.Color.green() if status_text == "online" else discord.Color.red())
        embed.add_field(name="Endereço", value=serv.address, inline=False)
        embed.add_field(name="Status", value=status_text.capitalize(), inline=True)
        embed.add_field(name="Software/Versão", value=f"{software} {version}", inline=True)
        embed.add_field(name="Jogadores", value=players_count, inline=True)
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Ocorreu um erro ao verificar o status: `{e}`")

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("Erro: DISCORD_TOKEN não encontrado nas variáveis de ambiente.")
    else:
        bot.run(DISCORD_TOKEN)
