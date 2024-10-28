# -*- coding: utf-8 -*-

import subprocess
import os

from .audio_models.vosk.vosk_api import VoskAudioModel


class AudioRecognizer:
    '''
    Documentation
    '''

    def __init__(self, model_config: dict) -> None:
        match model_config["model_name"]:
            case "vosk": self.model = VoskAudioModel(model_config["model_path"])
            case _: raise NameError("Invalid model name")

    def load_model(self) -> None:
        self.model.load()

    def file_open(self, path: str) -> None:
        self.model.file_open(convert_wav(path))

    def recognize(self) -> str:
        return self.model.recognize()

def convert_wav(video_filename: str) -> str:
    new_filename = f'media/{os.path.basename(video_filename).split(".")[0]}_audio.wav'
    command = ['ffmpeg', '-i', video_filename, '-ac', '1', '-ar', '16000', new_filename, '-y']
    subprocess.run(command)
    
    return new_filename
