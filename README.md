# Bot do Discord para Controle do Aternos (24/7)

Este bot permite controlar o seu servidor do Aternos diretamente pelo chat do Discord utilizando comandos simples. Ele está configurado para rodar em serviços como o Render usando um servidor Flask em paralelo para manter a conexão ativa.

## Funcionalidades
- `!ligar`: Inicia o servidor do Aternos.
- `!desligar`: Desliga o servidor do Aternos.
- `!status`: Mostra informações detalhadas sobre o servidor.

## Hospedagem 24/7 no Render (Plano Gratuito)

1. Crie uma conta no [Render](https://render.com/).
2. Conecte seu repositório do GitHub.
3. Escolha **Web Service**.
4. Configure as seguintes opções:
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
5. Adicione as **Environment Variables** (Variáveis de Ambiente) no Render:
   - `DISCORD_TOKEN`
   - `ATERNOS_USER`
   - `ATERNOS_PASSWORD`
   - `ATERNOS_SERVER_ADDRESS`
6. Após o deploy, copie a URL do seu serviço (ex: `https://seu-bot.onrender.com`).
7. Use um serviço como o [UptimeRobot](https://uptimerobot.com/) para monitorar essa URL a cada 5-10 minutos. Isso impedirá que o Render coloque o bot para dormir.

## Instalação Local

1. Clone o repositório e instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure o arquivo `.env`.
3. Execute:
   ```bash
   python bot.py
   ```
