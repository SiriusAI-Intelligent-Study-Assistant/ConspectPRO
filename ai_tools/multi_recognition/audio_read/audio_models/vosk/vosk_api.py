import wave
import json
import vosk
import logging


class VoskAudioModel:
    '''
    vosk_API
    '''

    def __init__(self, model_path: str) -> None:
        self.model_path = model_path
    
    # Загрузка модели
    def load(self) -> None:
        try:
            self.model = vosk.Model(self.model_path)
            logging.info(f'The model "{self.model_path}" has been successfully loaded')
        except:
            raise FileNotFoundError("Please download the model from\
                                         https://alphacephei.com/vosk/models and extract\
                                         it to the current directory or use the absolute path")
    
    # Открытие аудиофайла
    def file_open(self, path: str) -> None:
        '''
        Opening a file and creating a recognition objects
        '''

        self.wf = wave.open(path, "rb")
        logging.info(f'Audio file opened: "{path}"')
        self.rec = vosk.KaldiRecognizer(self.model, self.wf.getframerate())
        logging.info(f'Recognition object created. AudioFramerate: {self.wf.getframerate()}')
    
    # Распознавание речи
    def recognize(self) -> str:
        text = str

        while True:
            data = self.wf.readframes(4000)
            if len(data) == 0:
                break
            if self.rec.AcceptWaveform(data):
                result = json.loads(self.rec.Result())
                text += result['text']
        
        logging.info(f'Audio file recognized: "{text}"')
        return text