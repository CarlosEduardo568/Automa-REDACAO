import asyncio
import sys
import subprocess
import os
import tempfile
from notificacoes import mostrar_notificacao


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
    """Baixa e instala o Google Chrome automaticamente."""
    import requests
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
        await asyncio.sleep(2)

        subprocess.run([temp_path, "/install", "/nolaunchchrome"], check=True)
        await mostrar_notificacao('Instalador', "✅ Instalação concluída com sucesso!")

    except Exception as e:
        await mostrar_notificacao('Instalador', f"❌ Erro ao baixar ou instalar o Chrome: {e}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            print("🧹 Instalador temporário removido.")


def verificar_ffmpeg():
    """
    Adiciona automaticamente o ffmpeg ao PATH.
    Funciona em Python normal e PyInstaller.
    """
    base = getattr(sys, "_MEIPASS", os.getcwd())
    ffmpeg_dir = base  

    if ffmpeg_dir not in os.environ["PATH"]:
        os.environ["PATH"] += ";" + ffmpeg_dir
    
# 🔧 Função principal assíncrona que organiza a execução
async def instalar_dependencias():
    verificar_ffmpeg
    
    if not await chrome_instalado():
        await instalar_chrome()
