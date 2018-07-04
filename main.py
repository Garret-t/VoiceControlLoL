import pyautogui
import time
import threading
from pocketsphinx import LiveSpeech, get_model_path
import os
import re
import ctypes

#Pyautogui inputs are not accounted for in games, they are virtual keys and did not work so opted for another methon
# found here: https://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
SendInput = ctypes.windll.user32.SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]
#Press/Release functions
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
#http://www.gamespp.com/directx/directInputKeyboardScanCodes.html

#Screen Variables
distance = 200
centerX = 800
centerY = 450

time.sleep(5)#Time to start the program and tab back.

#Variable to get the updated value for threads.
global update

#Huge function with the sea of if statements checking for each word
def checkwords(audioIN):
    #Made directional inputs continouous so no need to repeat multiple times
    while audioIN == "up":
        pyautogui.dragTo(centerX + distance, centerY -distance, duration=0.2, button='right')
        if update != "up":
            pyautogui.moveTo(centerX, centerY, duration= .1)
            break
        pass
    while audioIN == "down":
        pyautogui.dragTo(centerX-distance, centerY + distance, duration=0.2, button='right')
        if update != "down":
            pyautogui.moveTo(centerX, centerY, duration= .1)
            break
        pass
    while audioIN == "left":
        pyautogui.dragTo(centerX -distance, centerY-distance, duration=0.2, button='right')
        if update != "left":
            pyautogui.moveTo(centerX, centerY, duration= .1)
            break
    pass
    while audioIN == "right":
        pyautogui.dragTo(centerX + distance, centerY + distance, duration=0.2, button='right')
        if update != "right":
            pyautogui.moveTo(centerX, centerY, duration= .1)
            break
    pass
    if audioIN == "q":
        PressKey(0x10)
        time.sleep(.1)
        ReleaseKey(0x10)
    if audioIN == "w":
        PressKey(0x11)
        time.sleep(.1)
        ReleaseKey(0x11)
    if audioIN == "e":
        PressKey(0x12)
        time.sleep(.1)
        ReleaseKey(0x12)
    if audioIN == "r":
        PressKey(0x13)
        time.sleep(.1)
        ReleaseKey(0x13)
    if audioIN == "level":
        PressKey(0x1D)
        time.sleep(2)
        ReleaseKey(0x1D)
    if audioIN == "back":
        PressKey(0x30)
        time.sleep(.1)
        ReleaseKey(0x30)
    if audioIN == "stop":
        print("Doing nothing")
    if audioIN == "flash":
        PressKey(0x20)
        time.sleep(.1)
        ReleaseKey(0x20)
    if audioIN == "heal":
        PressKey(0x21)
        time.sleep(.1)
        ReleaseKey(0x21)
    if audioIN == "ward":
        PressKey(0x05)
        time.sleep(.1)
        ReleaseKey(0x05)
    if audioIN == "champ":
        PressKey(0x33)
        time.sleep(.1)
        ReleaseKey(0x33)

#Threading function
#Opted to use threading so we could do multiple functions at once like ctrl + q
def inputThread(inp):
    thread1 = threading.Thread(target = checkwords, args = (inp,))
    thread1.start()

#PocketSphinx location vars
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
model_path = get_model_path()

speech = LiveSpeech(
    verbose = False,
    sampling_rate = 16000,
    buffer_size = 2048,
    no_search = False,
    full_utt = False,
    hmm=os.path.join(model_path, 'other'),
    lm=os.path.join(model_path, 'en-us.lm.bin'),
    dic = os.path.join(__location__, 'commands.dict'), #Path to my own dictionary of words
    audio_device = "Microphone (Realtek High Definition Audio)"
)

#Gets the phrase and sends it through the functions
for phrase in speech:
    print(phrase)
    update = str(phrase)
    inputThread(str(phrase))


#IGNORE
#Reference's for pyautogui
#pyautogui.moveTo(100, 100, duration = .5)
#pyautogui.moveRel(0, 50, duration = 1)
#pyautogui.click(100, 100)
#pyautogui.hotkey("ctrlleft", "a")
#pyautogui.typewrite(["a", "left", "ctrlleft"])
#pyautogui.click(200, 250, button='right')
#pyautogui.click(400, 400)
#while True:
    #pyautogui.moveTo(600, 600, duration= .1)
    #pyautogui.dragRel(distance, distance, duration=0.2)
    