import cv2
import numpy as np
import os
from com.common import *
from com.obj_detector import *

class blobDetector(object):
    def __init__(self, v):
        self.Node = os.getcwd() + v
        self.readFrom = 7 #7
        self.readTill = self.readFrom + 50
        self.keyPoints, self.kp = [], []
        self.cap, self.length, self.fps = VidCapture(self.Node, readFrom =self.readFrom)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fgmask = np.zeros((self.height, self.width, 1), 'uint8')
        [list_of_blobs, mp4_name] = filename_gen()
        self.out = cv2.VideoWriter(mp4_name, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 5, (1920, 1080))
        self.bg=bg_subtractorMOG(type="MOG", hist=300, thr=1000, sh=True)
        self.F = open(list_of_blobs, "w")
        self.detector = blob_detector()
        self.readFrames()


    def key_points(self):

        #if (self.keyPoints.__len__() > 30):
        #    self.keyPoints1.append(self.keyPoints)
        #else:
        #    self.keyPoints1.clear
        self.kp.clear()
        j = 0
        for kp in self.keyPoints:
            x, y = int(kp.pt[0]), int(kp.pt[1])

            if (kp.size >=3.0) and (FindPoint(X_filt[0], self.height - Y_filt[0], X_filt[1], self.height, x, y) and
                FindPoint(X_filt[1], self.height - Y_filt[1], X_filt[2], self.height, x, y) and
                FindPoint(X_filt[2], self.height - Y_filt[2], X_filt[3], self.height, x, y) and
                FindPoint(X_filt[3], self.height - Y_filt[3], X_filt[4], self.height, x, y) and
                FindPoint(X_filt[4], self.height - Y_filt[4], X_filt[5], self.height, x, y) and
                FindPoint(X_filt[5], self.height - Y_filt[5], X_filt[6], self.height, x, y) and
                FindPoint(X_filt[6], self.height - Y_filt[6], X_filt[7], self.height, x, y)):
                j = j + 1
                self.kp.append(cv2.KeyPoint(x=kp.pt[0], y=kp.pt[1], _size=kp.size))
        j = 0
        for kp in self.kp:
            j = j + 1
            print(kp.pt[0], kp.pt[1])
            x, y = int(kp.pt[0]), int(kp.pt[1])
            #cv2.circle(self.frame, (x, y), 40, (0, 255, 255), 8)
            cv2.rectangle(self.frame, (x - int(kp.size * 4), y - int(kp.size * 2.5)), (x + int(kp.size * 4), y + int(kp.size * 2.5)),
                          (0, 255, 255), 2)
            cv2.putText(self.frame, str(round(kp.size, 2)), (x + 60, y + 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 2, 4)
            cv2.putText(self.frame, str(j), (x + 60, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 2, 4)
                #cv2.putText(self.frame, str(self.kp.__len__()), (x + 80, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 2, 4)

            #self.F.write("%d %f %f %f %d\n" % (self.cnt, round(kp.pt[0],1), round(kp.pt[1],1), round(kp.size,1), self.keyPoints.__len__()))
            self.F.write('{0:5}{1:8}{2:8}{3:6}{4:4}\n'.format(self.cnt, round(kp.pt[0],1), round(kp.pt[1],1), round(kp.size,1), self.kp.__len__()))
            #print('{0:3d} {1:4f} {2:4f} {2:4d}'.format(self.cnt, round(kp.pt[0],1), round(kp.pt[1],2), round(kp.size,1), self.keyPoints.__len__()))

    def readFrames(self):
        kpall = 0
        while (self.cap.isOpened):
            self.kp.clear()
            ret, self.frame, self.cnt = FrameCapture(self.cap)
            if (ret==True):
                self.frame = cv2.GaussianBlur(self.frame, (9, 9), 0)
                bgfs=self.bg.apply(self.frame)
                self.keyPoints = self.detector.detect(bgfs)
                #for kp in self.keyPoints:
                 #   print (kp.pt[0], kp.pt[1])

                self.key_points()

                b, g, r = cv2.split(self.frame)
                self.frame = cv2.merge([b,g,bgfs])
                self.mask = cv2.merge([bgfs,bgfs,bgfs])

                frame_resized = ResizeImage(image=self.frame, fx=0.5, fy=0.5)
                kpall = kpall + self.kp.__len__()
                frame_resized = PutText(img=frame_resized, text=self.Node, fps=self.fps, cnt= self.cnt, x=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), y=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
                                        kp = self.kp.__len__(), kpAll=kpall)
                img_copy = frame_resized.copy()
                print (self.cnt)
                cv2.imshow('frame', img_copy)
                self.out.write(img_copy)
                #if (self.cnt > self.readTill):
                #    break

            else:
                break
            chr = cv2.waitKey(1) & 0xFF
            if chr == ord('q'):
                break
        self.out.release()
        self.cap.release()
        self.F.close()
        cv2.destroyAllWindows()
