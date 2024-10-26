import vosk
import sys
import os
import wave
import json

# Загрузка модели
# if not os.path.exists("vosk-model-ru-0.22"):
#     print("Пожалуйста, скачайте модель с https://alphacephei.com/vosk/models и распакуйте ее в текущий каталог.")
#     sys.exit()

model = vosk.Model("vosk-model-small-ru-0.22")

# Открытие аудиофайла
wf = wave.open(r"C:\Users\juryk\Desktop\Sirius_AI_code\ConspectPRO\ai_tools\multi_recognition\audio_read\test_600.wav", "rb")
rec = vosk.KaldiRecognizer(model, wf.getframerate())

# Распознавание речи
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        print(result['text'], end="")