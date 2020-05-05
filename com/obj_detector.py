import cv2
from com.common import *
from timecode import Timecode

"""
BACKGROUND INITIALISATION
"""
def bg_subtractorMOG(type="MOG",hist=300, thr=1000, sh=True):

    def BGSubtractor(self):
        if self.TypeBG == 1:
            self.BG = cv2.createBackgroundSubtractorMOG2()
            self.BG.setHistory (100)
            self.BG.setVarThreshold (80)
            self.BG.setDetectShadows (False)
            print('createBackgroundSubtractorMOG2')

    if (type=="MOG"):
        bg = cv2.createBackgroundSubtractorMOG2(history = 100, varThreshold= 80, detectShadows = False)
        str = 'Background Subtractor MOG2 initialized'
    elif (type=="KNN"):
        bg = cv2.createBackgroundSubtractorKNN()
        str = 'Background Subtractor KNN initialized'
        bg.setHistory(hist)
        bg.setDist2Threshold(thr)
        bg.setDetectShadows(sh)
    print(COLOR.GREEN + str + COLOR.END)
    return bg

"""
BLOB PARAM INITIALISATION
"""
def blob_detector():
    params = cv2.SimpleBlobDetector_Params()
    params.minDistBetweenBlobs = 20
    params.minRepeatability = 10
    # params.minDistBetweenBlobs = 500
    # params.minRepeatability = 1
    params.filterByArea = True
    params.minArea = 2 * 3
    params.maxArea = 32 * 32
    params.filterByCircularity = False
    params.minCircularity = 0.1
    params.filterByColor = False
    params.filterByConvexity = True
    params.minConvexity = 0.2
    params.filterByInertia = False
    params.minInertiaRatio = 0.01
    params.minThreshold = 10
    params.maxThreshold = 250
   # params.thresholdStep = 8
    ver = (cv2.__version__).split('.')
    str = 'SimpleBlobDetector initialized'
    print(COLOR.GREEN + str + COLOR.END)
    if int(ver[0]) < 3:
        return cv2.SimpleBlobDetector(params)
    else:
        return cv2.SimpleBlobDetector_create(params)