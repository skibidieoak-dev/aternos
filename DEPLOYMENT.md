# Guia Completo de Deploy no Render

Este documento fornece instruções passo a passo para fazer o deploy do bot Aternos no Render com suporte a cronjob.

## Pré-requisitos

- Conta no [GitHub](https://github.com)
- Conta no [Render](https://render.com)
- Token do Discord Bot
- Credenciais do Aternos (email e senha)
- Endereço do servidor Aternos

## Passo 1: Preparar o Repositório GitHub

1. Faça um fork ou clone deste repositório.
2. Certifique-se de que todos os arquivos estão presentes:
   - `bot.py`
   - `ping.py`
   - `render.yaml`
   - `Procfile`
   - `requirements.txt`
   - `.env.example`

3. Faça o push de todas as mudanças para o GitHub:
   ```bash
   git add .
   git commit -m "Preparar para deploy no Render"
   git push origin main
   ```

## Passo 2: Conectar Render ao GitHub

1. Acesse [Render Dashboard](https://dashboard.render.com).
2. Clique em "New +" e selecione "Web Service".
3. Clique em "Connect a repository".
4. Selecione o repositório `aternos`.
5. Clique em "Connect".

## Passo 3: Configurar o Web Service

1. Preencha os campos:
   - **Name**: `aternos-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
   - **Instance Type**: `Free`

2. Clique em "Advanced" e adicione as variáveis de ambiente:

   | Chave | Valor |
   |-------|-------|
   | `DISCORD_TOKEN` | Seu token do Discord |
   | `ATERNOS_USER` | Seu email do Aternos |
   | `ATERNOS_PASSWORD` | Sua senha do Aternos |
   | `ATERNOS_SERVER_ADDRESS` | Seu endereço do servidor |

3. Clique em "Create Web Service".

## Passo 4: Configurar o Cron Job (Opcional mas Recomendado)

Para manter o bot acordado 24/7 no plano gratuito, configure um cronjob:

### Opção A: Usando render.yaml (Automático)

1. No Render, clique em "Infrastructure as Code".
2. Selecione o repositório `aternos`.
3. Aponte para o arquivo `render.yaml`.
4. Configure as mesmas variáveis de ambiente.
5. Clique em "Deploy".

O Render criará automaticamente um cronjob que faz ping no serviço a cada 5 minutos.

### Opção B: Usando UptimeRobot (Manual)

1. Acesse [UptimeRobot](https://uptimerobot.com).
2. Crie uma conta gratuita.
3. Clique em "Add New Monitor".
4. Selecione "HTTP(s)" como tipo.
5. Cole a URL do seu serviço Render (ex: `https://aternos-bot.onrender.com`).
6. Configure o intervalo para **5 minutos**.
7. Clique em "Create Monitor".

## Passo 5: Testar o Bot

1. Vá para o seu servidor Discord.
2. Digite `!status` para verificar se o bot responde.
3. Se funcionar, o bot está pronto para usar!

## Monitoramento

### Verificar Logs no Render

1. Acesse o dashboard do Render.
2. Selecione o serviço `aternos-bot`.
3. Clique em "Logs" para ver a saída do bot.

### Verificar Status do Cronjob

1. No Render, selecione o cronjob `aternos-bot-ping`.
2. Verifique se ele está rodando a cada 5 minutos.
3. Procure por mensagens de sucesso nos logs.

## Solução de Problemas

### Erro: "DISCORD_TOKEN não encontrado"

- Verifique se você configurou a variável de ambiente no Render.
- Certifique-se de que o token está correto (sem espaços extras).

### Erro: "Servidor não encontrado"

- Verifique se o `ATERNOS_SERVER_ADDRESS` está correto.
- Certifique-se de que está em minúsculas (ex: `seu_servidor.aternos.me`).
- Confirme que sua conta do Aternos tem acesso ao servidor.

### Bot desconecta após algumas horas

- Certifique-se de que o cronjob está configurado.
- Verifique se o UptimeRobot está fazendo ping corretamente.
- Consulte os logs do Render para erros.

### Erro ao conectar no Aternos

- Verifique as credenciais do Aternos.
- Tente fazer login manualmente no site do Aternos.
- Verifique se sua conta não foi bloqueada.

## Custos

- **Web Service (Render)**: Gratuito (com limite de 750 horas/mês)
- **Cron Job (Render)**: Gratuito
- **UptimeRobot**: Gratuito (com limite de 50 monitores)

## Próximos Passos

- Personalize os comandos do bot em `bot.py`.
- Adicione mais funcionalidades conforme necessário.
- Configure alertas no UptimeRobot para ser notificado se o bot cair.

## Suporte

Se encontrar problemas, verifique:
1. Os logs no Render
2. As variáveis de ambiente
3. A documentação do [discord.py](https://discordpy.readthedocs.io/)
4. A documentação do [python-aternos](https://github.com/DarkCat09/python-aternos)
