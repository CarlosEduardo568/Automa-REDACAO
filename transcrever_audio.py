import sounddevice as sd
import numpy as np
import whisper
import tempfile
import scipy.io.wavfile as wav
import os

audio_buffer = []
stream = None
samplerate = 16000

def callback(indata, frames, time, status):
    audio_buffer.append(indata.copy())

def iniciar_gravacao():
    global audio_buffer, stream
    audio_buffer = []
    stream = sd.InputStream(samplerate=samplerate, channels=1, callback=callback)
    stream.start()
    print("🎙 Gravando...")

def parar_gravacao():
    global stream

    if stream:
        stream.stop()
        stream.close()
        print("⏹ Gravação finalizada!")

    # junta áudio
    audio_array = np.concatenate(audio_buffer, axis=0)

    # salva temporário
    temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp.close()
    wav.write(temp.name, samplerate, (audio_array * 32767).astype(np.int16))

    # Whisper
    modelo = whisper.load_model("small")
    texto_transcrito = modelo.transcribe(temp.name, language="pt")

    os.remove(temp.name)

    return texto_transcrito["text"]