import os
from com.common import COLOR
import cv2

class SaveToFrame (object):
    def __init__(self,**kwargs):
        self.frame = kwargs['frame']
        self.f_path = kwargs['path']
        self.f_name = kwargs['filename']
        #self.frame_id = kwargs['frame_id']
        #self.x, self.y = kwargs['x'], kwargs['y']
        #self.s = kwargs['s']



    def create_full_frame(self):
        frame = os.path.join(self.f_path, self.f_name)
        print(COLOR.RED + frame + COLOR.END)
        cv2.imwrite(frame + '.png', self.frame)





