from tkinter import *
from tkinter.ttk import *
import PIL.Image, PIL.ImageTk
class GUI_main:

    def __init__(self):
        #self.text = kwargs[1]
        self.gui_init()

    def gui_init(self):
        self.root = Tk()
        self.root.title(self.text)
        self.root.config(background="#FFFFFF")

    def imshow(self, **kwargs):
        image = kwargs[0]
        h, w, _ = image.shape
        imgtk = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(image))
        label = Label(self.root, image=imgtk)
        label.image = imgtk
        label.configure(image=imgtk)
        label.pack()
        self.root.mainloop()