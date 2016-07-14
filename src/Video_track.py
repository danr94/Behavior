import numpy as np
import pylab
import skimage
import skvideo.io as skvio
import json
# import poppy

fpath = '/home/sillycat/Documents/Zebrafish/Behavioral/Data/'

class Video_track(object):
    def __init__(self, video_data):
        self.vstack = video_data
        


# fname, height, width, num_frames, as_grey, inputdict, outputdict, backend, verbosity)


def main():
    vdata = skvio.vreader(fpath+'Jun20_G2_D1.MOV', height = 1080, width = 1920)
    
    
    
    G2 = Video_track(vdata)
    
    
if __name__ == '__main__':
    main()