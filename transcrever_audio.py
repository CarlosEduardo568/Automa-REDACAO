import sounddevice as sd
import numpy as np
import whisper
import tempfile
import scipy.io.wavfile as wav
import os
import asyncio
import sys
from time import sleep
from notificacoes import mostrar_notificacao

audio_buffer = []
stream = None
samplerate = 16000

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return relative

# Corrige caminho do assets
whisper.audio.MEL_FILTERS_PATH = resource_path("whisper/assets/mel_filters.npz")

 # carrega modelo
modelo = None

def ffmpeg_path():
    base = getattr(sys, "_MEIPASS", os.getcwd())
    return os.path.join(base, "ffmpeg.exe")

async def get_modelo():
    global modelo
    if modelo is None:
        await mostrar_notificacao('Gravador🎙️','Carregando Arquivos de aúdio.')
        modelo = whisper.load_model("small")
        await mostrar_notificacao('Gravador🎙️','✅Carregado, pronto para usar')
    return modelo

def iniciar_gravacao():
    global audio_buffer, stream
    audio_buffer = []
    sd.default.samplerate = samplerate
    sd.default.channels = 1

    sleep(0.2)  # <<< IMPORTANTE! deixa o microfone estabilizar

    stream = sd.InputStream(
        samplerate=samplerate,
        channels=1,
        blocksize=2048,
        callback=lambda indata, f, t, s: audio_buffer.append(indata.copy())
    )

    stream.start()
    print("🎙 Gravando...")

def parar_gravacao():
    global stream

    if stream:
        stream.stop()
        stream.close()
        print("⏹ Gravação finalizada!")
        print("Tamanho do buffer:", len(audio_buffer))

    if not audio_buffer:
        return "(nenhum áudio capturado)"

    # junta audio
    audio_array = np.concatenate(audio_buffer, axis=0)
    print("Tamanho do áudio capturado:", audio_array.shape)

    # arquivo temporário
    temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp.close()

    wav.write(temp.name, samplerate, (audio_array * 32767).astype(np.int16))

    # FFmpeg no PATH (para o .exe)
    os.environ["PATH"] += ";" + ffmpeg_path()

    # roda whisper
    resultado = get_modelo().transcribe(temp.name, language="pt")

    # trata retorno (pode ser dict ou string)
    if isinstance(resultado, dict):
        texto_transcrito = resultado.get("text", "")
    else:
        texto_transcrito = resultado

    print("Texto transcrito:", texto_transcrito)

    # limpa arquivo
    os.remove(temp.name)

    return texto_transcrito