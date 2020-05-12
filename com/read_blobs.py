from com.common import *
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from com.common import *

class Pnt(object):
    """
        Swap Operation Test Case
    """
    def __init__(self,b):
        self.b_id = []
        self.b_x = []
        self.b_x.append([])
        self.b_y = []
        self.b_y.append([])
        self.b_s = []
        self.b_s.append([])
        self.b = []
        self.b_in_frame = []
        self.frame_id = []
        self.read_txt(b)
        #self.plot_all_blobs_in_a_video()

    def file_existed(self,filename):
        try:
            f = open(filename)
            print (COLOR.GREEN + 'File ' + filename + ' is accessible' + COLOR.END)
            f.close()
            return True
        except IOError:
            print (COLOR.RED + 'File ' + filename + ' is not accessible' + COLOR.END)
            return False

    def read_txt(self, filename):
        file = self.file_existed(filename)
        if (file==True):
            self.b = filename
            data = np.loadtxt(filename)
            previous  = [int(data[0,0]), int(data[0,4])]
            self.b_id.append(previous[0])
            self.b_in_frame.append(previous[1])
            j = 0
            for index, value in enumerate(list(data[0:,0])):
                if (data[index, 0] != previous[0]):
                    previous = [int(data[index, 0]), int(data[index, 4])]
                    self.b_id.append(previous[0])
                    self.b_in_frame.append(previous[1])
                    self.b_x.append([])
                    self.b_y.append([])
                    self.b_s.append([])
                    j = j + 1
                    self.b_x[j].append(data[index, 1])
                    self.b_y[j].append(data[index, 2])
                    self.b_s[j].append(data[index, 3])
                else:
                    self.b_x[j].append(data[index, 1])
                    self.b_y[j].append(data[index, 2])
                    self.b_s[j].append(data[index, 3])

    def plot_all_blobs_in_a_video(self):

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.scatter(self.b_id, self.b_in_frame) # , linewidth=2, markersize=5
        ax.set_yscale('log')
        ax.minorticks_on()
        ax.grid(which='major', linestyle='-', linewidth='0.5', color='blue')
        ax.grid(which='minor', linestyle=':', linewidth='0.5', color='green')
        ax.set_title('We found ' + str(int(sum(self.b_in_frame))) + ' blobs in each frame of the video: ')
        ax.set_xlabel('Time, [Frame]')
        ax.set_ylabel('Blobs')
        plt.show()
