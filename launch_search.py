import webbrowser
from pynput.keyboard import Key, Controller
import time

def google_search(text: str) -> bool:
    text = text.replace(" ", "+")
    url = f"https://www.google.com/search?q={text}"
    webbrowser.open(url, new=0, autoraise=True)
    return True
    
def chatgpt_search(text: str) -> bool:
    keyboard = Controller()
    chrome_path = "C://Program Files (x86)//Google//Chrome//Application//Chrome.exe"
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    url = f"https://chat.openai.com/chat"
    webbrowser.get('chrome').open(url, new=0, autoraise=True)
    time.sleep(1) 
    keyboard.type(text)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    return True