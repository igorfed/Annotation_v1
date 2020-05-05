'''
Read text file and plot blobs
'''
__version__ = '0.1'
__author__ = 'Igofed'
from com.read_blobs import *
from com.plot_blobs import *
import argparse

def argParse():
    folder = "data"
    parser = argparse.ArgumentParser(description="Video showing")
    parser.add_argument("-v", "--v",
                        required=False,
                        help = 'Path to input video',
                        type=str,
                       # default='/annotated_lists/video1/c2_20180627_090006.mp4')
                        default='/input/c2_resolution_good.mp4')

    parser.add_argument("-b", "--b",
                        required=False,
                        help = 'Path to text file with blobs',
                        type=str,
                        default='20200320-215736.txt')
    parser.add_argument("-output_path", "-output_path",
                        required=False,
                        help = 'output folder for frames',
                        type=str,
                        default='out')
    parser.add_argument("-extract_frames", "-extract_frames",
                        required=False,
                        help='Do you want to extract frames with birds ?',
                        type=bool,
                        default=True)

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = argParse()
    print(args)


    def file_existed(filename):
        try:
            f = open(filename)
            print(COLOR.GREEN + 'File ' + filename + ' is accessible' + COLOR.END)
            f.close()
            return True
        except IOError:
            print(COLOR.RED + 'File ' + filename + ' is not accessible' + COLOR.END)
            return False
    file_existed(args.b)


    pnts = Pnt(b=args.b)
    vid  = PlotBlobs(b=args.b,v=args.v, output_path = args.output_path, extract_frames=args.extract_frames, pnts = pnts)
    vid.showFrames()
    #pnts1 = Pnt('annotated_lists/20200217-083636_annotated.txt')
    print('done')