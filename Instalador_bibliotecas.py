import asyncio
import sys
import subprocess
import os
import requests
import tempfile
from notificacoes import mostrar_notificacao
from main import main

async def instalar_playwright_se_preciso():
    """
    Garante que o Playwright e os navegadores estejam instalados.
    Mesmo em PCs sem Python ou Playwright pré-instalados.
    """
    try:
        import playwright
        print("✅ Playwright já instalado.")
    except ImportError:
        mostrar_notificacao('Instalador',"🔄 Instalando Playwright...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "playwright"], check=True)
            print("✅ Playwright instalado!")
        except Exception as e:
            print("❌ Erro ao instalar Playwright:", e)
            return


async def chrome_instalado():
    """Verifica se o Google Chrome está instalado no Windows."""
    caminhos = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    ]

    for caminho in caminhos:
        if os.path.exists(caminho):
            print(f"✅ Chrome encontrado em: {caminho}")
            return True
    await mostrar_notificacao('Instalador', "❌ Google Chrome não encontrado.")
    return False


async def instalar_chrome():
    """Baixa e instala o Google Chrome automaticamente (modo silencioso)."""
    url_instalador = "https://dl.google.com/chrome/install/latest/chrome_installer.exe"

    await mostrar_notificacao('Instalador', "⬇️ Baixando instalador do Google Chrome...")
    temp_path = os.path.join(tempfile.gettempdir(), "chrome_installer.exe")

    try:
        response = requests.get(url_instalador, stream=True)
        response.raise_for_status()
        with open(temp_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        await mostrar_notificacao('Instalador', "📦 Instalador baixado")

        await mostrar_notificacao('Instalador', "⚙️ Instalando o Google Chrome...")
        subprocess.run([temp_path, "/silent", "/install"], check=True,stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL)
        await mostrar_notificacao('Instalador', "✅ Instalação concluída com sucesso!")

    except Exception as e:
        await mostrar_notificacao('Instalador', f"❌ Erro ao baixar ou instalar o Chrome: {e}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            print("🧹 Instalador temporário removido.")
    
# 🔧 Função principal assíncrona que organiza a execução
async def instalar():
    await instalar_playwright_se_preciso()

    if not await chrome_instalado():
        await instalar_chrome()

    await main()


if __name__ == "__main__":
    asyncio.run(instalar())
