import mouse
import time
import keyboard
import json



lastActionTime = 0
actionsQueue = []

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

def printHotkeysSummary():
    summaryMessage = '''CopyMe Hotkeys Summary 🦆

ESC: Pauses any recording reproduction and quits the CopyMe

ALT + Z: Initialize the mouse recording
ALT + X: Stops the mouse recording
ALT + C: Reproduces the recording

ALT + V: Saves the current mouse recording
ALT + B: Loads the saved mouse recording

ALT + Q: While reproducing a record, hold the hotkeys to stops the reproduction

ALT + H: Prints this summary

NOTE: The keybindings will work till the ESC key be pressed
'''
    
    print(summaryMessage)

def reproduceMouseRecording():
    global actionsQueue

    for action in actionsQueue:
        needToStop = keyboard.is_pressed("alt+q")
        
        if needToStop:
            break
        
        x = action["x"]
        y = action["y"]
        
        actionTime = action["time"]

        mouse.move(x, y, duration=actionTime)
        mouse.click()

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

def registerKeyboardHotkeys():
    keyboard.add_hotkey("alt+z", startMouseRecording)
    keyboard.add_hotkey("alt+x", stopMouseRecording)
    keyboard.add_hotkey("alt+c", reproduceMouseRecording)
    keyboard.add_hotkey("alt+v", saveMouseRecording)
    keyboard.add_hotkey("alt+b", loadSavedMouseRecording)
    keyboard.add_hotkey("alt+h", printHotkeysSummary)
    
    keyboard.add_hotkey("esc", quitCopyMe)

def initializeCopyMe():
    printHotkeysSummary()
    
    registerKeyboardHotkeys()
    
initializeCopyMe()
