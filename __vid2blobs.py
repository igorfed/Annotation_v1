__version__ = '0.1'
__author__ = 'Igofed'
from com.ShowVideo import *
import argparse

import os

def argParse():
    parser = argparse.ArgumentParser(description="Video showing")
    parser.add_argument("-v", "--v", required=False, help = 'Path to input video from Node 0 camera 0',
                        type=str, default='\input\c1_20180627_090007.mp4')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = argParse()
    print('Called with args:')
    print(args)
    mt=blobDetector(v= args.v)
    print('done')