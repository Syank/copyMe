import mouse
import time
import keyboard

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

ESC: Quits the CopyMe

CTRL + Z: Initialize the mouse recording
CTRL + X: Stops the mouse recording
CTRL + C: Reproduces the recording

CTRL + H: Prints this summary

NOTE: The keybindings will work till the ESC key be pressed
'''
    
    print(summaryMessage)

def reproduceMouseRecording():
    global actionsQueue

    for action in actionsQueue:
        x = action["x"]
        y = action["y"]
        
        actionTime = action["time"]

        time.sleep(actionTime)

        mouse.move(x, y, duration=actionTime / 2)
        mouse.click()

def registerKeyboardHotkeys():
    keyboard.add_hotkey("ctrl+z", startMouseRecording)
    keyboard.add_hotkey("ctrl+x", stopMouseRecording)
    keyboard.add_hotkey("ctrl+c", reproduceMouseRecording)
    keyboard.add_hotkey("ctrl+h", printHotkeysSummary)
    
    keyboard.add_hotkey("esc", quitCopyMe)
    
def initializeCopyMe():
    printHotkeysSummary()
    
    registerKeyboardHotkeys()
    
initializeCopyMe()
