# Интеллектуальный помощник для создания учебных материалов
### Sirius AI
---
Является модулем для нашего приложения.

---
### Использование:
`import ai_tools`

---
# Документация:

### Краткое содержание:
- [CreateLLMSession](#сессия)
    - [summarize](#суммаризация)
    - [paraphrase](#перефразирование)
    - [chat](#чат)
    - [get_chat_history](#получение-истории-чата)
- [translate](#перевод)
- [Multi-recognize](#распознавание-мультиконтента)
    - [audio](#распознавание-аудио)

---
## Перевод:
```Python
from ai_tools import translate

print( translate( "ru", "en", "Привет, мир!" ) )
```

---
## LLM Сессия:
### Создание LLM сессии:
```Python
from ai_tools import CreateLLMSession
from ai_tools.config import MISTRAL_API_KEY

model_config = {
    "API_KEY": MISTRAL_API_KEY,
    "model_name": "mistral",
}

llm_session = CreateLLMSession( model_config )
```

- ### Суммаризация:
  ```Python
  text = '''Большие языковые модели невероятно гибкие. 
  Одна модель может выполнять совершенно разные задачи, 
  такие как ответы на вопросы, обобщение документов, языковые 
  переводы и составление предложений. LLM могут кардинально 
  повлиять на создание контента и использованию людьми поисковых 
  систем и виртуальных помощников.
  '''

  llm_session.summarize( text )
  ```

- ### Перефразирование:
  ```Python
  llm_session.paraphrase( text )
  ```

- ### Чат:
  ```Python
  llm_session.chat( text )
  llm_session.chat( 'Что ещё умеют LLM?' )
  llm_session.chat( 'О чём мы говорим?' )
  ```

- ### Получение истории чата:
    ```Python
    llm_session.get_chat_history()
    ```

---
## Распознавание мультиконтента

- ### Распознавание аудио:
  ```Python
  from ai_tools import AudioRecognizer

  model_config = {
    "model_name": "vosk", # whisper
    "model_path": "vosk-model-small-ru-0.22"
  }

  stt = AudioRecognizer( model_config )

  stt.file_open( "test.wav" )
  stt.recognize()
  ```