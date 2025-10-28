import sounddevice as sd
import numpy as np
import whisper
import tempfile
import scipy.io.wavfile as wav
import os

def transcrever_audio_texto():
    print("Pressione Enter para começar a gravação...")
    input()  # espera Enter

    print("Gravando! Pressione Enter novamente para parar...")
    audio_buffer = []  # vai armazenar blocos

    def callback(indata, frames, time, status):
        audio_buffer.append(indata.copy())

    # Inicia stream
    samplerate = 16000
    stream = sd.InputStream(samplerate=samplerate, channels=1, callback=callback)
    stream.start()

    input()  # espera Enter para parar
    stream.stop()
    print("Gravação finalizada!")

    # Concatena todos os blocos
    audio_array = np.concatenate(audio_buffer, axis=0)

    # Salva arquivo temporário
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_file.close()
    wav.write(temp_file.name, samplerate, (audio_array * 32767).astype(np.int16))

    # Transcrição com Whisper
    model = whisper.load_model("small")
    texto_transcrito = model.transcribe(temp_file.name, language="pt")

    os.remove(temp_file.name)