import asyncio
import sys
import subprocess
import os
import tempfile
from notificacoes import mostrar_notificacao
import whisper


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


# ----------- RESOLVE CAMINHOS DO PYINSTALLER -----------
def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(os.getcwd(), relative)


# Corrige caminho do MEL FILTERS (obrigatório para PyInstaller)
whisper.audio.MEL_FILTERS_PATH = resource_path("whisper/assets/mel_filters.npz")


# ----------- CONFIGURAÇÃO DO FFMPEG INTERNO -------------
def ffmpeg_folder():
    """Retorna o caminho da pasta ffmpeg/bin que deve estar junto do .exe"""
    base = getattr(sys, "_MEIPASS", os.getcwd())
    return os.path.join(base, "ffmpeg", "bin")


def configurar_ffmpeg():
    """Adiciona ffmpeg/bin ao PATH e define caminhos diretos para Whisper"""
    ffbin = ffmpeg_folder()

    ffmpeg_exe = os.path.join(ffbin, "ffmpeg.exe")
    ffprobe_exe = os.path.join(ffbin, "ffprobe.exe")

    # Adiciona ao PATH
    os.environ["PATH"] += os.pathsep + ffbin

    # Define para Whisper
    whisper.audio.FFMPEG_PATH = ffmpeg_exe
    whisper.audio.FFPROBE_PATH = ffprobe_exe



    
# 🔧 Função principal assíncrona que organiza a execução
async def instalar_dependencias():
    configurar_ffmpeg()
    
    if not await chrome_instalado():
        await instalar_chrome()
