import pyautogui, time
time.sleep(6) 
screenshot = pyautogui.screenshot()
screenshot.save("data/screenshot1.png")