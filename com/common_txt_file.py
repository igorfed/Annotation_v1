import os
from com.common import COLOR

class SaveToTXT (object):
    def __init__(self,**kwargs):
        self.frame = kwargs['frame']
        self.f_path = kwargs['path']
        self.f_name = kwargs['filename']
        #self.draw_bounding_box()
    def create_txt(self):
        self.f_name = self.f_name + '.txt'
        self.F = open(os.path.join(self.f_path, self.f_name), 'w')
        if self.F.closed:
            print(COLOR.RED + self.f_name + ' is closed for writing' + COLOR.END)
        else:
            print(COLOR.GREEN + self.f_name + ' is opened for writing' + COLOR.END)
    def draw_bounding_box (self):
        def if_more(n):
            if n >= 0:
                n = n
            else:
                n = 0
            return int(n)
        def if_less(n, m):
            if n <= m:
                n = n
            else:
                n = m
            return int(n)
        self.x1 = if_more(self.x - 4*self.s)
        self.y1 = if_more(self.y - 3*self.s)
        self.h = self.frame.shape[0]
        self.w = self.frame.shape[1]
        self.x2 = if_less(self.x + 4*self.s, self.w)
        self.y2 = if_less(self.y + 3*self.s, self.h)

    def convert_to_YOLO_format(self):

        self.class_id = 0
        self.xYolo =  (self.x/self.w)
        self.yYolo =  (self.y/self.h)
        self.wYolo = (abs(self.x1 - self.x2)/self.w)
        self.hYolo = (abs(self.y1 - self.y2)/self.w)

    def write_txt(self,**kwargs):
        self.x, self.y, self.s = kwargs['x'], kwargs['y'], kwargs['s']
        self.draw_bounding_box()
        self.convert_to_YOLO_format()
        self.F.write('{0:d}{1: f}{2: f}{3: f}{4: f}\n'.format(self.class_id, self.xYolo, self.yYolo, self.wYolo, self.hYolo))

    def close_txt(self):
        self.F.close()





