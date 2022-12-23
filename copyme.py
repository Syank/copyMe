import mouse
import time
import keyboard
import json



lastActionTime = 0
actionsQueue = []
reprodutionMode = "singleReprodution"  # The available modes are "singleReprodution" and "loopReprodution"

def registerMousePosition():
    global lastActionTime, actionsQueue

    x, y = mouse.get_position()
    currentTime = time.time()

    elapsedTime = currentTime - lastActionTime

    lastActionTime = currentTime

    action = {
        "x": x,
        "y": y,
        "time": elapsedTime
    }

    actionsQueue.append(action)

def quitCopyMe():
    mouse.unhook_all()
    keyboard.unhook_all()

def startMouseRecording():
    global lastActionTime, actionsQueue

    actionsQueue = []
    
    lastActionTime = time.time()
    
    mouse.on_click(registerMousePosition)

def stopMouseRecording():
    mouse.unhook_all()

def needToStopReproducing():
    global reprodutionMode

    needToStop = keyboard.is_pressed("alt+q")

def reproduceActions():
    for action in actionsQueue:
        needToStop = keyboard.is_pressed("alt+q")
        
        if needToStop:
            return True
        
        x = action["x"]
        y = action["y"]
        
        actionTime = action["time"]

        mouse.move(x, y, duration=actionTime)
        mouse.click()

    return False

def reproduceMouseRecording():
    global actionsQueue, reprodutionMode

    needToStop = False

    if reprodutionMode == "singleReprodution":
        reproduceActions()

    elif reprodutionMode == "loopReprodution":
        needToStop = False
        
        while not needToStop:
            needToStop = reproduceActions()

def saveMouseRecording():
    global actionsQueue

    stringfiedQueue = json.dumps(actionsQueue)

    with open("savedActions.txt", "w") as savedActionsFile:
        savedActionsFile.write(stringfiedQueue)

def loadSavedMouseRecording():
    global actionsQueue

    with open ("savedActions.txt", "r") as savedActionsFile:
        stringfiedQueue = savedActionsFile.read()

        actionsQueue = json.loads(stringfiedQueue)

def changeReprodutionMode(newReprodutionMode):
    global reprodutionMode

    reprodutionMode = newReprodutionMode;

def registerKeyboardHotkeys():
    keyboard.add_hotkey("alt+z", startMouseRecording)
    keyboard.add_hotkey("alt+x", stopMouseRecording)
    keyboard.add_hotkey("alt+c", reproduceMouseRecording)
    keyboard.add_hotkey("alt+v", saveMouseRecording)
    keyboard.add_hotkey("alt+b", loadSavedMouseRecording)
    keyboard.add_hotkey("alt+h", printHotkeysSummary)
    keyboard.add_hotkey("alt+a", changeReprodutionMode, args=["singleReprodution"])
    keyboard.add_hotkey("alt+s", changeReprodutionMode, args=["loopReprodution"])
    
    keyboard.add_hotkey("esc", quitCopyMe)

def printHotkeysSummary():
    summaryMessage = '''CopyMe Hotkeys Summary 🦆

ESC: Quits the CopyMe. Note that it only works if no recording is being reprodution at the key press momment

ALT + Z: Initialize the mouse recording
ALT + X: Stops the mouse recording
ALT + C: Reproduces the recording

ALT + V: Saves the current mouse recording
ALT + B: Loads the saved mouse recording

ALT + A: Changes the reprodution mode to Single Reprodution
ALT + S: Changes the reprodution mode to Loop Reprodution

ALT + Q: While reproducing a record, hold the hotkeys to stops the reprodution

ALT + H: Prints this summary

NOTES:
  - The keybindings will work till the ESC key be pressed
  - With the exception of the ALT + Q hotkey, all the other hotkeys will be unnavailable to use while a record is being reproduced
'''
    
    print(summaryMessage)

def initializeCopyMe():
    printHotkeysSummary()
    
    registerKeyboardHotkeys()
    
initializeCopyMe()
