# ----------

from fastapi import FastAPI, HTTPException
import uvicorn



#from pydantic import BaseModel


from vacore import VACore
#import time

# ------------------- main loop ------------------

core = VACore()
core.init_with_plugins()
core.init_plugin("webapi")
webapi_options = core.plugin_options("webapi")
print("WEB api for VoiceAssistantCore (remote control)")
# здесь двойная инициализация - на импорте, и на запуске сервера
# не очень хорошо, но это нужно, чтобы получить webapi_options = core.plugin_options("webapi")

"""
returnFormat Варианты:
- "none" (TTS реакции будут на сервере) (звук на сервере)
- "saytxt" (сервер вернет текст, TTS будет на клиенте) (звук на клиенте)
- "saywav" (TTS на сервере, сервер отрендерит WAV и вернет клиенту, клиент его проиграет) (звук на клиенте) **наиболее универсальный для клиента**
"""
def runCmd(cmd:str,returnFormat:str):
    if core.logPolicy == "cmd" or core.logPolicy == "all":
        print("Running cmd: ",cmd)

    tmpformat = core.remoteTTS
    core.remoteTTS = returnFormat
    core.remoteTTSResult = ""
    core.lastSay = ""
    core.execute_next(cmd,core.context)
    core.remoteTTS = tmpformat

app = FastAPI()


# рендерит текст в wav
@app.get("/ttsWav")
async def ttsWav(text:str):
    #runCmd(cmd,returnFormat)
    tmpformat = core.remoteTTS
    core.remoteTTS = "saywav"
    core.play_voice_assistant_speech(text)
    core.remoteTTS = tmpformat
    return core.remoteTTSResult


# выполняет команду Ирины
# Например: привет, погода.
@app.get("/sendTxtCmd")
async def sendSimpleTxtCmd(cmd:str,returnFormat:str = "none"):
    runCmd(cmd,returnFormat)
    return core.remoteTTSResult

# Посылает распознанный текстовый ввод. Если в нем есть имя помощника, выполняется команда.
# Пример: ирина погода, раз два
@app.get("/sendRawTxt")
async def sendRawTxt(rawtxt:str,returnFormat:str = "none"):
    tmpformat = core.remoteTTS
    core.remoteTTS = returnFormat
    core.remoteTTSResult = ""
    core.lastSay = ""
    isFound = core.run_input_str(rawtxt)
    core.remoteTTS = tmpformat

    if isFound:
        return core.remoteTTSResult
    else:
        return "NO_VA_NAME"

# Запускает внутреннюю процедуру проверки таймеров. Должна запускаться периодически
@app.get("/updTimers")
async def updTimers():
    #core.say("аа")
    #print("upd timers")
    core._update_timers()
    return ""

def core_update_timers_http(runReq=True):
    from threading import Timer
    if runReq:
        try:
            import requests
            reqstr = "http://{0}:{1}/updTimers".format(webapi_options["host"],webapi_options["port"])
            #print(reqstr)
            r = requests.get(reqstr)
        except Exception:
            pass
    t = Timer(2, core_update_timers_http)
    t.start()

if __name__ == "__main__":
    core_update_timers_http(False)
    uvicorn.run("runva_webapi:app", host=webapi_options["host"], port=webapi_options["port"],
                log_level=webapi_options["log_level"])