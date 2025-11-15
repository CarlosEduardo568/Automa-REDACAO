import sounddevice as sd
import numpy as np
import whisper
import tempfile
import scipy.io.wavfile as wav
import os
import sys

audio_buffer = []
stream = None
samplerate = 16000

def ffmpeg_path():
    base = getattr(sys, "_MEIPASS", os.getcwd())
    return os.path.join(base, "ffmpeg.exe")

def iniciar_gravacao():
    global audio_buffer, stream
    audio_buffer = []
    sd.default.samplerate = samplerate
    sd.default.channels = 1

    stream = sd.InputStream(callback=lambda indata, f, t, s: audio_buffer.append(indata.copy()))
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

    # carrega modelo
    modelo = whisper.load_model("small")

    # roda whisper
    resultado = modelo.transcribe(temp.name, language="pt")

    # trata retorno (pode ser dict ou string)
    if isinstance(resultado, dict):
        texto_transcrito = resultado.get("text", "")
    else:
        texto_transcrito = resultado

    print("Texto transcrito:", texto_transcrito)

    # limpa arquivo
    os.remove(temp.name)

    return texto_transcrito