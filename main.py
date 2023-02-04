import os
import easygui
import tkinter as tk
import tkinter.ttk
from tkinter.constants import *
from tkinter import messagebox
import subprocess

import torch

#easygui.fileopenbox()

import webbrowser

def callback(url):
    webbrowser.open_new(url)


def selectPhotoFolder():
    photoPath = easygui.diropenbox("字幕存放資料夾")
    output_dir.delete(0, 'end')
    output_dir.insert(0, photoPath)

def selectAudioFile():
    File = easygui.fileopenbox("選擇音檔檔案")
    displayAudioFilePath.delete(0, 'end')
    displayAudioFilePath.insert(0, File)
    
def detectAvailableDevice():
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            devices.append(torch.cuda.get_device_name(i))
        
    usingDevice['value'] = devices
    return

def deviceChange(index, value, op):
    #print("%s %s %s"%(index, value, op))
    dev = devices.index(usingDevice.get())
    if dev > 0:
        print("cuda:%s"%(dev-1))
    else:
        print("cpu")

def deviceDecode():
    dev = devices.index(usingDevice.get())
    if dev > 0:
        return("cuda:%s"%(dev-1))
    else:
        return("cpu")

    
def process():
    File = displayAudioFilePath.get()
    if File == "":
        messagebox.showerror(title="錯誤", message='未選擇音檔')
        return 0

    commandStr = "venv\\Scripts\\whisper "
    
    commandStr = commandStr + '"%s"'%File

    languageInput = usingLanguage.get()

    if languageInput != "自動偵測":
        commandStr = commandStr + " --language %s "%languageInput

    deviceInput = deviceDecode()
    commandStr = commandStr + " --device %s "%deviceInput

    commandStr = commandStr + " --model %s "%usingModel.get()

    output_dirInput = output_dir.get()

    if output_dirInput != "":
        commandStr = commandStr + " --output_dir %s "%output_dirInput

    commandStr = commandStr + " --model_dir %s "%("model")

    if translateToEnglishVar.get() == '1':
        commandStr = commandStr + " --task %s "%("translate")

    #print(os.system("echo %s"%commandStr))
    out = subprocess.Popen(commandStr)
    (out, err) = out.communicate()

    messagebox.showinfo(title="訊息", message="處理完成")
    #outputPreviewVar.set(out)
    #print(out)


window = tk.Tk()
window.title('WhisperGUI By The Walking Fish')
window.geometry('580x200')
window.resizable(False, False)
#window.iconbitmap('icon.ico')

label1 = tk.Label(text='選擇音檔')
label1.place(x=0, y=0)
displayAudioFilePath = tk.Entry(width=60)
displayAudioFilePath.place(x=80, y=0)
selectAudioFileButton = tk.Button(text='....', command=selectAudioFile)
selectAudioFileButton.place(x=500, y=0)


label2 = tk.Label(text='字幕存放資料夾')
label2.place(x=0, y=30)
output_dir = tk.Entry(width=55)
output_dir.place(x=120, y=30)
output_dir.insert(0, os.getcwd() + "\\output")
selectPhotoPathButton = tk.Button(text='....', command=selectPhotoFolder)
selectPhotoPathButton.place(x=500, y=30)

label_usingModel = tk.Label(text='使用模型')
label_usingModel.place(x=0, y=60)
var = tk.StringVar()
usingModel = tkinter.ttk.Combobox(window, textvariable=var)
usingModel['value'] = ('tiny', 'base', 'small', 'medium', 'large', 'large-v1', 'large-v2')
usingModel.current(2)
usingModel.place(x=60, y=60)

label_usingDevice = tk.Label(text='使用裝置')
label_usingDevice.place(x=0, y=80)
deviceVar = tk.StringVar()
deviceVar.trace("w", deviceChange)
usingDevice = tkinter.ttk.Combobox(window, textvariable=deviceVar)
devices = ['cpu']
usingDevice['value'] = devices
detectAvailableDevice()
usingDevice.current(0)
usingDevice.place(x=60, y=80)

label_language = tk.Label(text='辨識語言')
label_language.place(x=0, y=100)
languageVar = tk.StringVar()
usingLanguage = tkinter.ttk.Combobox(window, textvariable=languageVar)
languages = ['自動偵測', "Afrikaans","Albanian","Amharic","Arabic","Armenian","Assamese","Azerbaijani","Bashkir","Basque","Belarusian","Bengali","Bosnian","Breton","Bulgarian","Burmese","Castilian","Catalan","Chinese","Croatian","Czech","Danish","Dutch","English","Estonian","Faroese","Finnish","Flemish","French","Galician","Georgian","German","Greek","Gujarati","Haitian","Haitian Creole","Hausa","Hawaiian","Hebrew","Hindi","Hungarian","Icelandic","Indonesian","Italian","Japanese","Javanese","Kannada","Kazakh","Khmer","Korean","Lao","Latin","Latvian","Letzeburgesch","Lingala","Lithuanian","Luxembourgish","Macedonian","Malagasy","Malay","Malayalam","Maltese","Maori","Marathi","Moldavian","Moldovan","Mongolian","Myanmar","Nepali","Norwegian","Nynorsk","Occitan","Panjabi","Pashto","Persian","Polish","Portuguese","Punjabi","Pushto","Romanian","Russian","Sanskrit","Serbian","Shona","Sindhi","Sinhala","Sinhalese","Slovak","Slovenian","Somali","Spanish","Sundanese","Swahili","Swedish","Tagalog","Tajik","Tamil","Tatar","Telugu","Thai","Tibetan","Turkish","Turkmen","Ukrainian","Urdu","Uzbek","Valencian","Vietnamese","Welsh","Yiddish","Yoruba"]
usingLanguage['value'] = languages
usingLanguage.current(0)
usingLanguage.place(x=60, y=100)

translateToEnglishVar = tk.StringVar()
translateToEnglish = tk.Checkbutton(text="將輸出字幕翻譯為英文", variable=translateToEnglishVar, onvalue="1", offvalue="0")
translateToEnglish.deselect()
translateToEnglish.place(x=0, y=120)

label_copyright = tk.Label(text='MIT License')
label_copyright.place(x=0, y=160)
label_author = tk.Label(text='製作: The Walking Fish')
label_author.bind("<Button-1>", lambda e: callback("https://www.youtube.com/@the_walking_fish"))
label_author.place(x=0, y=180)


processButton = tk.Button(text='執行', width=20, command=process)
processButton.place(anchor='center', x=290, y=180)

window.mainloop()
