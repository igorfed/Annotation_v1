from tkinter import *
from tkinter.ttk import *
import PIL.Image, PIL.ImageTk
import cv2
class GUI_main:

    def __init__(self, **kwargs):
        self.text = kwargs['text']
        self.gui_init()
        
    def gui_init(self):
        # initialize root window
        self.root = Tk()
        # set window title
        self.root.title(self.text)
        # self.destructor function gets fired when the window is closed
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)

        self.root.config(background="#FFFFFF")

    def imshow(self, **kwargs):
        image = kwargs['image']
        h, w, _ = image.shape
        print (image.shape)
        imgtk = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(image))
        label = Label(self.root, image=imgtk)
        label.image = imgtk
        label.configure(image=imgtk)

    def destructor(self):
        """ Destroy the root object and release all resources """
        print("[INFO] closing...")
        self.root.destroy()
