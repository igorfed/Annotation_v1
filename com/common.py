import numpy as np

import os
import matplotlib.pyplot as plt
import time
import sys
import cv2

class COLOR:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

blank_image = np.zeros((2160, 3840, 3), np.uint8)

def convertMillis(millis, print_en, numFrame):
   seconds = (millis / 1000) % 60
   minutes = (millis / (1000 * 60)) % 60
   hours = (millis / (1000 * 60 * 60)) % 24
   strTimeFrame = str(int(hours)) + ':' + str(int(minutes)) + ':' + str(round(seconds))
   return strTimeFrame

def VidCapture(cam, readFrom):


   cap = cv2.VideoCapture(cam)
   cap.set(1, readFrom)
   if (cap == False):
      print (COLOR.RED + 'Error Opening Video Stream or File' + cam + COLOR.END)
   else:
      length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
      fps = round(cap.get(cv2.CAP_PROP_FPS))
     # print (COLOR.GREEN + 'Opening Video Stream or File' + cam + ' length:' + str(length) + ' fps'+ str(fps) + COLOR.END)

   return cap, length, fps

def FrameCapture(cap):
   ret, frame = cap.read()
   cnt = round(cap.get(cv2.CAP_PROP_POS_FRAMES))
   return ret, frame, cnt

def ResizeImage(image, fx, fy):
   original = image.copy()
   resized = cv2.resize(original, None, fx=fx, fy=fy, interpolation=cv2.INTER_CUBIC)

   return resized

def PutText(img, text, fps, cnt, x, y, kp, kpAll):
   cv2.putText(img,
               text, #"S11333928",
               (10, 20),
               cv2.FONT_HERSHEY_SIMPLEX,
               0.5,
               (0,0, 255),
               1,
               1)
   cv2.putText(img,
               "fps = " + str(fps),
               (10, 40),
               cv2.FONT_HERSHEY_SIMPLEX,
               0.5,
               (0, 0, 255),
               1,
               1)
   cv2.putText(img,
               "[x, y] =" + '[ '+str(int(x)) +" , "+ str(int(y))+' ]',
               (10, 60),
               cv2.FONT_HERSHEY_SIMPLEX,
               0.5,
               (0, 0, 255),
               1,
               1)
   cv2.putText(img,
               "Total blobs: " + str(kpAll)+ " blobs in frame =" + str(kp) ,
               (10, 80),
               cv2.FONT_HERSHEY_SIMPLEX,
               0.5,
               (0, 0, 255),
               1,
               1)
   timestamp = 200
   timestamp = timestamp * (cnt - 1) + 1000 / (fps)
   strTimeFrame = convertMillis(abs(timestamp), True, cnt)
   out = cv2.putText(img, 'frame: ' + str(cnt) + '  timestamp: ' + strTimeFrame, (10, 100), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 1, 1)

   return out



def PressSpaceBar(img):
   cv2.putText(img,
               "<SPACEBAR pressed>",
               (10, 400),
               cv2.FONT_HERSHEY_SIMPLEX,
               4,
               (0, 0, 255),
               1,
               1)

def FindPoint( x1, y1, x2, y2, x, y):
    if (x > x1 and x < x2):
        if (y > y1 and y < y2):
            return False
        else: return True
    else: return True




def filename_gen():
    list_of_blobs = time.strftime("%Y%m%d-%H%M%S.txt")
    mp4_name = time.strftime("%Y%m%d-%H%M%S.avi")

    return [list_of_blobs, mp4_name]


X_filt = [  0, 150, 400, 700, 1400, 2800, 3100, 3840]
Y_filt = [400, 250, 220, 220,   180,   180,  180,    0]


def draw_marks(image, coord, color=(255, 255, 255), Thickness=2, length =10):
    """Draw mark points on image"""
    (x, y) = coord
    img = image.copy()
    cv2.line(img, (x,y+5), (x,y+length), color, Thickness, cv2.LINE_4)
    cv2.line(img, (x,y-5), (x,y-length), color, Thickness, cv2.LINE_4)
    cv2.line(img, (x+5,y), (x+length,y), color, Thickness, cv2.LINE_4)
    cv2.line(img, (x-5,y), (x-length,y), color, Thickness, cv2.LINE_4)
    return img

def main_menu():
    os.system('clear')
    print ("Check if you found the birds")
    print ("Press ENTER if everything is correct")
    print ("Press 0, 1, or N if object should be removed from the list")

    return

def check_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder

def annotation_file(filename='20200217-083636.txt', new_filename='annotated'):
    f_name, f_ext = os.path.splitext(filename)[0], os.path.splitext(filename)[1]
    folder = check_folder(folder='annotated_lists')
    new_filename =  f_name + '_' + new_filename + f_ext
    F = open(os.path.join(folder,new_filename), 'w')
    if F.closed:
        print(COLOR.RED + new_filename + ' is closed for writing' + COLOR.END)
    else:
        print(COLOR.GREEN + new_filename + ' is opened for writing' + COLOR.END)
    return  F

