import PIL.Image, PIL.ImageTk
from tkinter import *
from tkinter.ttk import *
import argparse
import datetime
import cv2
import os
from com.common import *
class GUI_Birds:

    def __init__(self, image, N, birds, cnt, coord, output_path, F ):
        """ Initialize application which uses OpenCV + Tkinter. It displays
            a video stream in a Tkinter window and stores current snapshot on disk """
        #self.vs = cv2.imread(image, 0)
        self.F = F
        self.output_path = output_path
        self.birds = birds
        self.cnt = cnt
        self.N = N
        self.ix = [coord[i][0] for i in range (len(coord))]
        self.x =  [coord[i][1] for i in range (len(coord))]
        self.y =  [coord[i][2] for i in range (len(coord))]
        self.x1 = [coord[i][3] for i in range(len(coord))]
        self.y1 = [coord[i][4] for i in range(len(coord))]
        self.s =  [coord[i][5] for i in range (len(coord))]
        self.L =  [coord[i][6] for i in range (len(coord))]
        self.path_for_annotation_txt = 'annotation_log'
        # Set up GUI
        self.root = Tk()  # initialize root window
        self.root.title("Birds Detected")  # set window title
        self.root.config(background="#FFFFFF")
        self.root.focus_set()
        # Entry widget
        e1 = Entry(self.root)
        e1.focus_set()
        # make the top right close button minimize (iconify) the main window

        self.A = [True for n in range(N)]
       #self.root.protocol("WM_DELETE_WINDOW", lambda: self.destructor())
        #self.root.bind('<space>', lambda e: self.destructor())

        self.root.grab_set()
        # Graphic window

        h, w,_ = image.shape

        imgtk = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(image)) #PIL.Image.fromarray(

        label = Label(self.root, image=imgtk)#.pack(fill = BOTH, expand = 1)
        label.image = imgtk
        label.configure(image=imgtk)
        label.pack()
        #topFrame.confi panel = Label(self.root, image=birds).pack()

       # panel.image = birds
      #  panel.config(image=birds)
        #canvas.create_image(0,0, image = photo,anchor=NW)
        #image = PhotoImage(file=image)

        bottomFrame0 = Frame(self.root)
        bottomFrame0.pack()
        bottomFrame1 = Frame(self.root)
        bottomFrame1.pack()

        bottomFrame2 = Frame(self.root)
        bottomFrame2.pack(side=BOTTOM)
        self.label = []
        self.btn = []


        for i in range(N):
            labl_text = 'frame_' + str(self.cnt) + '_' + str(self.ix[i]) + '_' + 'x_' + str(self.x[i]) + '_y_' + str(self.y[i]) + '_' + 'x1_' + str(self.x1[i]) + '_' + 'y1_' + str(self.y1[i])
            lbl = Label(bottomFrame0)
            lbl.config(text=labl_text)
            lbl.pack(side=LEFT)
            self.label.append(lbl)
            #self.btn.append(Button(bottomFrame1, text = "REMOVE " +str(self.A[i]), command = lambda:self.clickButtonRemove(L=i)).pack(side=LEFT))
            self.btn.append(Button(bottomFrame1, text = "Birds " +str(self.A[i]),command = lambda i=i :self.clickButtonRemove(L=i)))
            self.btn[i].pack(side=LEFT)

    #        label = Label(bottomFrame0, text='Birds 1').grid(row=0, column = 1)
    #    label2 = Label(bottomFrame0, text='Birds 2').grid(row=0, column = 2)
    #    label3 = Label(bottomFrame0, text='Birds 3').grid(row=0, column = 3)

       # button0 = Button(bottomFrame1, text = "Button 0", fg="red")
        #button1 = Button(bottomFrame1, text = "Button 1", fg="blue")
        #button2 = Button(bottomFrame1, text = "Button 2", fg="green")
        #button3 = Button(bottomFrame1, text = "Button 3", fg="red")



        self.button4 = Button(bottomFrame2, text = "CONTINUE", style = 'TButton',command = lambda: self.destructor()) #fg="red",
        self.button4.pack(fill = X, expand = YES)
        self.button4.focus_set()
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.destructor())
        self.root.bind('<space>', lambda e: self.destructor())

        #button4.bind('<ENTER>', close_window())

        ##button0.pack(side=LEFT)
        #button1.pack(side=LEFT)
        #button2.pack(side=LEFT)
        #button3.pack(side=LEFT)



        #self.panel = tk.Label(self.root)  # initialize image panel
        #self.panel.pack()

        # create a button, that when pressed, will take the current frame and save it to file
        #btn = tk.Button(self.root,  text="Press ENTER to continue", command=self.take_snapshot)
        #btn.pack(side= BOTTOM)

        # start a self.video_loop that constantly pools the video sensor
        # for the most recently read frame
        #self.image_loop()
    def clickButtonRemove(self,L):
        print (L)
        print(COLOR.GREEN+ str(self.A) + COLOR.END)
        self.A[L] =not self.A[L]
        print (L)
        self.btn[L].config(text = 'BIRDS '+ str(self.A[L]) )
        self.button4.focus_set()
        print(COLOR.RED + str(self.A) + COLOR.END)

    def remove_birds(self, num):
        print (COLOR.GREEN + str(self.A) + COLOR.END)
        self.A[num] = False
        print(COLOR.RED + str(self.A) + COLOR.END)

    def image_loop(self):
        """ Get frame from the video stream and show it in Tkinter """
        cv2image = self.vs.copy()
        h, w = self.vs.shape
           # cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
        self.current_image = Image.fromarray(cv2image)  # convert image for PIL
        imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter
        self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
        self.panel.config(image=imgtk)  # show the image
        #self.root.after(30, self.video_loop)  # call the same function after 30 milliseconds

    def take_snapshot(self):
        """ Take snapshot and save it to the file """
        ts = datetime.datetime.now() # grab the current timestamp
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))  # construct filename
        p = os.path.join(self.output_path, filename)  # construct output path
        self.current_image.save(p, "JPEG")  # save image as jpeg file
        print("[INFO] saved {}".format(filename))



    def image_save (self):
        print('Birds', self.A)
        for i in range(self.N):
            print (i)
            if self.A[i] == True:
                frame_name = 'frame_' + str(self.cnt) + '_' + str(self.ix[i]) + '_' + 'x_' + str(self.x[i]) + '_y_' + str(self.y[i]) + '_' + 'x1_' + str(self.x1[i]) + '_y1_' + str(self.y1[i]) + '_s_' + str(self.s[i])+ '.png'
                print(COLOR.GREEN + frame_name + COLOR.END)
                self.F.write('{0:5}{1:8}{2:8}{3:8}{4:8}{5:6}{6:4}\n'.format(self.cnt, self.x[i], self.y[i], self.x1[i], self.y1[i], self.s[i], self.A.count(True)))
                print (self.output_path+'/'+frame_name)
                cv2.imwrite(self.output_path+'/'+frame_name, self.birds[i])
            else:
                print(COLOR.RED + "Birds REMOVED" + COLOR.END)
                #print (COLOR.RED + self.output_path+'/'+frame_name + 'unsaved'+ COLOR.END)

    def destructor(self):
        """ Destroy the root object and release all resources """
        self.image_save()
        print(COLOR.GREEN + str(self.A) + COLOR.END)
        self.root.destroy()
#
        #cv2.destroyAllWindows()  # it is not mandatory in this application
        # self.F.write('{0:5}{1:8}{2:8}{3:6}{4:4}\n'.format(self.cnt, x, y, s, len(self.b_x[i][:])))

# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--input",required=False,
##                    help= 'input image',
#                    type=str,
#                    default='frame_12_0_x_1267_y_1445_C_0.346.png')
#args = vars(ap.parse_args())

# start the app
#print("[INFO] starting...")
#pba = GUI_Birds(args["input"])
#pba.root.mainloop()