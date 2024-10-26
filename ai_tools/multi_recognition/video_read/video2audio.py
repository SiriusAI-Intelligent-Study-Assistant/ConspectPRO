# -*- coding: utf-8 -*-

import subprocess
import os

def convert_wav(video_filename: str) -> str:
    new_filename = f'{os.path.basename(video_filename).split(".")[0]}_audio.wav'
    command = ['ffmpeg', '-i', video_filename, '-ac', '1', '-ar', '16000', new_filename, '-y']

    subprocess.run(command)
    
    return new_filename