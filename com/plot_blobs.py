import cv2
import numpy as np
import os
from com.common import *
import pynput
from pynput.keyboard import Key, Controller
import tkinter
import numpy as np
#import Image, ImageTk
from com.obj_detector import *
from com.tkinint1 import *
from com.gui_window import *
class PlotBlobs(object):
    def __init__(self, b, v, output_path, extract_frames, pnts, c):
        self.full_frame_extract_enable = c
        #self.F = annotation_file(filename=b, new_filename='annotated')
        self.Node = os.getcwd() + v
        self.readFrom = 7
        self.readTill = self.readFrom + 50
        self.cap, self.length, self.fps = VidCapture(self.Node, readFrom =self.readFrom)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.b_id = pnts.b_id
        self.b_in_frame = pnts.b_in_frame
        self.b_x = pnts.b_x
        self.b_y = pnts.b_y
        self.b_s = pnts.b_s
        self.BoundingBox = 200
        self.output_path =output_path
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        self.extract_frames = extract_frames


    def windowtk(self):
        self.window = tkinter.Tk()  # Makes main window
        self.window.wm_title("Digital Microscope")
        self.window.config(background="#FFFFFF")

    def showFrames(self):
        def if_more(n):
            if n >= 0:
                n = n
            else:
                n = 0
            return n

        def if_less(n, m):
            if n <= m:
                n = n
            else:
                n = m
            return n
        def contrast_value(frame):
            min = np.min(frame)
            max = np.max(frame)
            if min == 0:
                min = 1
            contrast = round(min/max,3)
            #print (min, max, contrast)
            return contrast
        pause = False
        obj_found = True
        birds = []
        blank_image = np.zeros((self.BoundingBox * 2, self.BoundingBox * 2, 3), np.uint8)
        blank_image_concat = np.zeros((self.BoundingBox * 2, self.BoundingBox * 2, 3), np.uint8)
        while (self.cap.isOpened):
            if (not pause ):
                ret, self.frame, self.cnt = FrameCapture(self.cap)
                if (ret==True):
                    frame_resized = self.frame.copy()
                    source_frame = self.frame.copy()
                    frame_resized1 = frame_resized.copy()
                    coord = []
                    if (self.cnt in self.b_id):
                        #if obj_found:
                        #    pause = not pause
                        #else:
                        #    pause = pause
                        print(COLOR.GREEN + 'Birds found in frame' + str(pause) + COLOR.GREEN)
                        i = self.b_id.index(self.cnt)
                        cv2.putText(frame_resized1, "blobs in frame =" + str(self.b_in_frame[i]), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, 1)
                        birds.clear()
                        from com.common_txt_file import SaveToTXT
                        __save_to_txt = SaveToTXT(frame=source_frame.copy(), path=self.output_path,
                                                  filename='Frame_' + str(self.cnt),
                                                  frame_id=self.cnt)

                        __save_to_txt.create_txt()
                        from com.common_frame_files import SaveToFrame
                        __save_to_frame = SaveToFrame(frame=source_frame.copy(), path=self.output_path, filename='Frame_' + str(self.cnt))
                        for ix, valx in enumerate (self.b_x[i][:]):
                            x = int (valx)
                            y = int(self.b_y[i][ix])
                            s = self.b_s[i][ix]


                            #cv2.circle(frame_resized, (x, y), 30, (0, 255, 255), 6)
                            if self.extract_frames:
                                x1 = if_more(x-self.BoundingBox)
                                y1 = if_more(y-self.BoundingBox)
                                y2 = if_less(y+self.BoundingBox,self.height)
                                x2 = if_less(x+self.BoundingBox, self.width)
                                crop_img = frame_resized[y1:y2, x1:x2].copy()
                                print (x, y, x1, y1, x2, y2, self.width, self.height)
                                contrast = contrast_value(crop_img)
                                #print('frame: ', self.cnt, ' x: ', x, ' y: ', y, ' x1, x2: ', x1, x2, ' y1, y2: ', y1, y2, ' C: ', contrast)
                                #print(crop_img.shape)
                             #   frame_resized1 = frame_resized.copy()
                                if contrast <= 0.7 and len(self.b_x[i][:]) < 20:



                                    #cv2.imwrite(self.output_path+'/'+frame_name, crop_img)
                                    #self.F.write('{0:5}{1:8}{2:8}{3:6}{4:4}\n'.format(self.cnt, x, y, s, len(self.b_x[i][:])))
                                #   cv2.rectangle(frame_resized, (x-int(s*4), y-int(s*2.5)), (x+int(s*4), y+int(s*2.5)), (0, 255, 255), 2)


                                    __save_to_txt.write_txt(x= x, y= y, s= s)
                                    __save_to_frame.create_full_frame()
                                  #  __save_to_frame.create_full_frame()
                                        #print('self.full_frame_extract_enable', self.full_frame_extract_enable)
                                        #frame_name = 'frame_' + str(self.cnt) + '_' + str(ix) + '_' + 'x_' + str(x) + '_y_' + str(y) + '_C_' + str(contrast) + '.png'
                                        #cv2.imwrite(self.output_path + '/' + frame_name, crop_img)
                                        #print
                                    birds.append(crop_img.copy())
                                    coord.append([ix, x, y, x - x1, y - y1, s, len(self.b_x[i][:])])
                                    frame_name = 'frame_' + str(self.cnt) + '_' + str(ix) + '_' + 'x_' + str(
                                        x) + '_y_' + str(y) + '_C_' + str(contrast) + '.png'
                                    cv2.rectangle(frame_resized1, (__save_to_txt.x1, __save_to_txt.y1),(__save_to_txt.x2, __save_to_txt.y2), (0, 255, 255), 2)
                                    cv2.putText(frame_resized1, str(ix), (x+50, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 2,2)
                                    cv2.putText(frame_resized1, str(s), (x + 50, y+40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255),2,)


                                else:
                                    cv2.rectangle(frame_resized1, (x - self.BoundingBox, y - self.BoundingBox), (x + self.BoundingBox, y + self.BoundingBox), (0, 255, 0),2)
                                    cv2.putText(frame_resized1, str(ix), (x + 50, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5,(0, 255, 0), 2, 2)
                                    cv2.putText(frame_resized1, str(s), (x + 50, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 1.5,(0, 255, 0), 2, )
                        __save_to_txt.close_txt()

                    frame_resized1 = ResizeImage(image=frame_resized1, fx=0.5, fy=0.5)
                    cv2.putText(frame_resized1, self.Node, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, 1)
                    cv2.putText(frame_resized1, "fps = " + str(self.fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 0, 255), 1, 1)
                    timestamp = 200
                    timestamp = timestamp * (self.cnt - 1) + 1000 / (self.fps)
                    strTimeFrame = convertMillis(abs(timestamp), True, self.cnt)
                    cv2.putText(frame_resized1, 'frame: ' + str(self.cnt) + '  timestamp: ' + strTimeFrame, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, 1)
                    cv2.imshow('frame', frame_resized1)

                    #if birds != []:
                    #    Temp = []
                    #    print(coord, coord[0][0])
                    #    for i, val in enumerate(birds):
                    #        blank_image = np.zeros((self.BoundingBox * 2, self.BoundingBox * 2, 3), np.uint8)
                    #        blank_image[0:birds[i].shape[0], 0:birds[i].shape[1]] = birds[i].copy()
                    #        img = draw_marks(blank_image, (coord[i][3], coord[i][4]), color=(255, 0, 255), Thickness=1, length=15)
                    #        Temp.append(img)
                    #        if i >0:
                     #           blank_image_concat = cv2.hconcat([blank_image_concat,img])
                     #       else:
                     #           blank_image_concat = Temp[-1]

                        # Graphics window
                     #   pba = GUI_Birds(blank_image_concat, len(birds), birds, self.cnt, coord,  self.output_path, self.F, source_frame)
                     #   pba.root.mainloop()
                      #  root = tkinter.Tk()
                       # im = Image.fromarray(blank_image_concat)
                        #imgtk = ImageTk.PhotoImage(image=im)
                        #tkinter.Label(root, image=imgtk).pack()
                        #cv2.imshow("Birds", blank_image_concat)
                        #root.mainloop()
                        #main_menu()
                     #   birds.clear()
                     #   blank_image = np.zeros((self.BoundingBox * 2, self.BoundingBox * 2, 3), np.uint8)

                    #else:
                     #   pass
                else:
                    break
            else:
                #print(COLOR.RED + 'SPACEBAR pressed' + str(pause) + COLOR.END)
                cv2.imshow('frame', frame_resized1)
                cv2.putText(frame_resized1, "<SPACEBAR pressed>", (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255),2, 1)
            chr = cv2.waitKey(1) & 0xFF
            if chr == ord('q'):
                break
            if chr == ord(' '):  # press SPACEBAR to stop the frame
                pause = not pause

        self.cap.release()
#        self.F.close()
        cv2.destroyAllWindows()