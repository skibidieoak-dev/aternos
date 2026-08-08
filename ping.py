import os
import requests

def ping_server():
    url = os.getenv("RENDER_EXTERNAL_URL")
    if not url:
        print("Erro: RENDER_EXTERNAL_URL não configurada. Não é possível fazer o ping.")
        return

    try:
        response = requests.get(url)
        print(f"Ping em {url}: Status {response.status_code}")
    except Exception as e:
        print(f"Erro ao tentar pingar {url}: {e}")

if __name__ == "__main__":
    ping_server()
