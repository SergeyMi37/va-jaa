# Core plugin
# author: Vladislav Janvarev

from vacore import VACore

# функция на старте
def start(core:VACore):
    manifest = {
        "name": "Core plugin",
        "version": "2.3",

        "default_options": {
            "mpcIsUse": True,
            "mpcHcPath": "C:\Program Files (x86)\K-Lite Codec Pack\MPC-HC64\mpc-hc64_nvo.exe",
            "mpcIsUseHttpRemote": False,

            "isOnline": False,
            #"ttsIndex": 0,
            "ttsEngineId": "pyttsx",
            "ttsEngineId2": "", # двиг для прямой озвучки на сервере. Если пуст - используется ttsEngineId
            "playWavEngineId": "audioplayer",
            "linguaFrancaLang": "ru", # язык для библиотеки lingua-franca конвертирования чисел
            "voiceAssNames": "лика|лики|лику",
            "logPolicy": "cmd", # all | cmd | none
            
			"logCmd": "print_and_say", # print_and_say Выводить в терминал сообщения VA и говорить | print_only без голоса 
			"durationContext": 50,
			
            "replyNoCommandFound": "Извини, я не поняла",
            "replyNoCommandFoundInContext": "Не поняла...",
            "replyOnlineRequired": "Для этой команды необходим онлайн",

            "tempDir": "temp",
        },

    }
    return manifest

def start_with_options(core:VACore, manifest:dict):
    #print(manifest["options"])
    options = manifest["options"]
    #core.setup_assistant_voice(options["ttsIndex"])

    core.mpcHcPath = options["mpcHcPath"]
    core.mpcIsUse = options["mpcIsUse"]
    core.mpcIsUseHttpRemote = options["mpcIsUseHttpRemote"]
    core.isOnline = options["isOnline"]

    core.voiceAssNames = options["voiceAssNames"].split("|")
    core.ttsEngineId = options["ttsEngineId"]
    core.ttsEngineId2 = options["ttsEngineId2"]
    core.playWavEngineId = options["playWavEngineId"]
    core.logPolicy = options["logPolicy"]
    core.logCmd = options["logCmd"]
    core.durationContext = options["durationContext"]
    core.tmpdir = options["tempDir"]
    import os
    if not os.path.exists(core.tmpdir):
        os.mkdir(core.tmpdir)

    import lingua_franca
    lingua_franca.load_language(options["linguaFrancaLang"])


    return manifest
