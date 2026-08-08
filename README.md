# Bot do Discord para Controle do Aternos (24/7)

Este bot permite controlar o seu servidor do Aternos diretamente pelo chat do Discord utilizando comandos simples. Ele está configurado para rodar em serviços como o Render usando um servidor Flask em paralelo para manter a conexão ativa.

## Funcionalidades
- `!ligar`: Inicia o servidor do Aternos.
- `!desligar`: Desliga o servidor do Aternos.
- `!status`: Mostra informações detalhadas sobre o servidor.

## Hospedagem 24/7 no Render (Plano Gratuito)

### Método 1: Deploy Manual via UI (Recomendado para Começar)

1. Crie uma conta no [Render](https://render.com/).
2. Conecte seu repositório do GitHub.
3. Escolha **Web Service**.
4. Configure as seguintes opções:
   - **Runtime**: `Python 3`
   - **Python version**: `3.11.9` (definida pelo arquivo `.python-version`)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
5. Adicione as **Environment Variables** (Variáveis de Ambiente) no Render:
   - `DISCORD_TOKEN`
   - `ATERNOS_USER`
   - `ATERNOS_PASSWORD`
   - `ATERNOS_SERVER_ADDRESS`
6. Após o deploy, copie a URL do seu serviço (ex: `https://seu-bot.onrender.com`).
7. Use um serviço como o [UptimeRobot](https://uptimerobot.com/) para monitorar essa URL a cada 5-10 minutos. Isso impedirá que o Render coloque o bot para dormir.

### Método 2: Deploy com Infraestrutura as Code (render.yaml)

Este repositório agora inclui um arquivo `render.yaml` que automatiza o deploy com **cronjob integrado**:

1. Faça o push das mudanças para o GitHub.
2. No Render, selecione **Infrastructure as Code** durante o setup.
3. Aponte para o arquivo `render.yaml` neste repositório.
4. Configure as variáveis do Web Service conforme descrito acima. No Cron Job, configure `SERVICE_URL` com a URL pública do Web Service, por exemplo `https://aternos-bot.onrender.com`.
5. O Render criará automaticamente:
   - **Web Service**: Executa o bot Discord com Flask keep-alive
   - **Cron Job**: Faz ping na API a cada 5 minutos para manter o serviço acordado

### Configuração de Variáveis de Ambiente

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `DISCORD_TOKEN` | Token do seu bot Discord | `MTk4NjIyNDgzNTgxMjgwMzI4.Clwa7A...` |
| `ATERNOS_USER` | Seu email/username do Aternos | `seu_email@example.com` |
| `ATERNOS_PASSWORD` | Sua senha do Aternos | `sua_senha_segura` |
| `ATERNOS_SERVER_ADDRESS` | Endereço do seu servidor Aternos | `seu_servidor.aternos.me` |
| `PYTHON_VERSION` | Versão compatível com `python-aternos` | `3.11.9` |
| `SERVICE_URL` | URL pública usada pelo Cron Job | `https://aternos-bot.onrender.com` |

## Arquivos Importantes

- **`bot.py`**: Código principal do bot Discord
- **`ping.py`**: Script do cronjob que consulta `/health` e exige `SERVICE_URL`
- **`render.yaml`**: Configuração de infraestrutura para o Render
- **`Procfile`**: Define como o Render deve iniciar o serviço
- **`requirements.txt`**: Dependências Python necessárias

## Instalação Local

1. Clone o repositório e instale as dependências:
   ```bash
   git clone https://github.com/skibidieoak-dev/aternos.git
   cd aternos
   pip install -r requirements.txt
   ```
2. Configure o arquivo `.env`:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas credenciais
   ```
3. Execute:
   ```bash
   python bot.py
   ```

## Como Obter o Token do Discord

1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications).
2. Clique em "New Application" e dê um nome ao seu bot.
3. Vá para a aba "Bot" e clique em "Add Bot".
4. Copie o token sob "TOKEN".
5. Ative as permissões necessárias em "Privileged Gateway Intents" (Message Content Intent).

## Solução de Problemas

### Bot não responde no Discord
- Verifique se o `DISCORD_TOKEN` está correto.
- Certifique-se de que o bot foi adicionado ao seu servidor com permissões adequadas.
- Verifique os logs no Render para erros.

### Servidor Aternos não liga/desliga
- Verifique as credenciais do Aternos (`ATERNOS_USER` e `ATERNOS_PASSWORD`).
- Confirme que o `ATERNOS_SERVER_ADDRESS` está correto (deve estar em minúsculas).
- Verifique se sua conta do Aternos tem acesso ao servidor.

### Render coloca o bot para dormir
- Certifique-se de que o cronjob está configurado e rodando.
- Se estiver usando o método manual, configure o UptimeRobot para fazer ping a cada 5-10 minutos.

## Licença

Este projeto é fornecido como está, sem garantias.
