from tkinter import *
import pyautogui

from apply_ocr import do_ocr
from launch_search import google_search, chatgpt_search

def take_bounded_screenshot(x1, y1, x2, y2):
    image = pyautogui.screenshot(region=(x1, y1, x2, y2))
    file_name = "to_ocr" #datetime.datetime.now().strftime("%f")
    image.save("snips/" + file_name + ".png")


class Application():
    def __init__(self, master):
        self.snip_surface = None
        self.master = master
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None

        root.geometry('400x100+200+200')  # set new geometry
        root.title('Lil Snippy')

        self.menu_frame = Frame(master)
        self.menu_frame.pack(fill=BOTH, expand=YES, padx=1, pady=1)
        self.menu_frame.columnconfigure(0, weight=2)
        self.menu_frame.columnconfigure(1, weight=2)

        self.buttonBar = Frame(self.menu_frame, bg="")
        self.buttonBar.grid(column=1, row=0, sticky=W)

        self.snipButton = Button(self.buttonBar, width=5, height=5, command=self.create_screen_canvas, background="green")
        self.snipButton.pack()

        self.options = ["Google", "ChatGPT"]
        self.engine = StringVar()
        self.engine.set("ChatGPT")
        self.dropdown_frame = Frame(self.menu_frame)
        self.dropdown_frame.grid(column=2, row=0, sticky=W)
        self.dropdown = OptionMenu(self.dropdown_frame , self.engine , *self.options)
        self.dropdown.pack()

        self.master_screen = Toplevel(root)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "maroon3")
        self.picture_frame = Frame(self.master_screen, background="maroon3")
        self.picture_frame.pack(fill=BOTH, expand=YES)
        

    def create_screen_canvas(self):
        self.master_screen.deiconify()
        root.withdraw()

        self.snip_surface = Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.snip_surface.pack(fill=BOTH, expand=YES)

        self.snip_surface.bind("<ButtonPress-1>", self.on_button_press)
        self.snip_surface.bind("<B1-Motion>", self.on_snip_drag)
        self.snip_surface.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', .3)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_release(self, event):
        self.display_rectangle_position()

        # Calculate the coordinates of the screenshot region
        x1, y1 = min(self.start_x, self.current_x), min(self.start_y, self.current_y)
        x2, y2 = max(self.start_x, self.current_x), max(self.start_y, self.current_y)

        # Pass the coordinates of the screenshot region to the take_bounded_screenshot function
        take_bounded_screenshot(x1, y1, x2 - x1, y2 - y1)

        self.exit_screenshot_mode()
        text = do_ocr()
        engine_to_use = self.engine.get()
        print(f"Engine: {engine_to_use}")
        if engine_to_use == "ChatGPT":
            chatgpt_search(text)
        else:
            google_search(text)

        return event

    def exit_screenshot_mode(self):
        self.snip_surface.destroy()
        self.master_screen.withdraw()
        root.deiconify()

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.snip_surface.canvasx(event.x)
        self.start_y = self.snip_surface.canvasy(event.y)
        self.snip_surface.create_rectangle(0, 0, 1, 1, outline='red', width=3, fill="maroon3")

    def on_snip_drag(self, event):
        self.current_x, self.current_y = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.snip_surface.coords(1, self.start_x, self.start_y, self.current_x, self.current_y)

    def display_rectangle_position(self):
        print(self.start_x)
        print(self.start_y)
        print(self.current_x)
        print(self.current_y)


if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.mainloop()

    # What is the definition of Terrible ?