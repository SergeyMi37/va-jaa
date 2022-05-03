# Приветствие (и демо-плагин)
# author: Vladislav Janvarev (inspired by EnjiRouz)

import random
from vacore import VACore

# функция на старте
def start(core:VACore):
    manifest = { # возвращаем настройки плагина - словарь
        "name": "Привет", # имя
        "version": "1.0", # версия
        "require_online": False, # требует ли онлайн?

        "commands": { # набор скиллов. Фразы скилла разделены | . Если найдены - вызывается функция
            "привет|доброе утро|здравствуй|хай|хэлоу": play_greetings,
        }
    }
    return manifest

def play_greetings(core:VACore, phrase: str): # в phrase находится остаток фразы после названия скилла,
                                              # если юзер сказал больше
                                              # в этом плагине не используется
    # Проигрывание случайной приветственной речи
    greetings = [
        "И тебе привет!",
        "Рада тебя видеть!",
		"Рада тебя слышать!",
		"и тебе не хворать!",
		"здоровья тебе!",
		"доброго дня!",
		"ух ты, кто здесь?",
		"слушаю и повинуюсь",
		"я вся внимание",
    ]
    core.play_voice_assistant_speech(greetings[random.randint(0, len(greetings) - 1)])
