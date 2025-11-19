import sounddevice as sd
import numpy as np
import whisper
import tempfile
import scipy.io.wavfile as wav
import os
from time import sleep

audio_buffer = []
stream = None
samplerate = 16000

#--------------------GRAVAÇÃO DE AÚDIO------------------------------------------------

def iniciar_gravacao():
    global audio_buffer, stream
    audio_buffer = []

    sd.default.samplerate = samplerate
    sd.default.channels = 1

    sleep(0.2)  # microfone estabiliza

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

    # Junta áudio
    audio_array = np.concatenate(audio_buffer, axis=0)
    print("Tamanho do áudio capturado:", audio_array.shape)

    # Cria wav temporário
    temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp.close()

    wav.write(temp.name, samplerate, (audio_array * 32767).astype(np.int16))

    # Carrega modelo Whisper
    modelo = whisper.load_model("small")

    # Transcreve
    resultado = modelo.transcribe(temp.name, language="pt")

    # Extrai texto
    texto_transcrito = resultado.get("text", "") if isinstance(resultado, dict) else resultado

    print("Texto transcrito:", texto_transcrito)

    os.remove(temp.name)

    return texto_transcrito