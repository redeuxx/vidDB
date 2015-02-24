__author__ = 'Vernon Wenberg III'

import os
import operator
from tkinter import *


def main():
    root = Tk()
    root.mainloop()
    test()

def test():
    directory = 'Z:\pr0n\\'
    if True == os.path.isdir(directory):
        dir_path = os.listdir(directory)
        print(type(dir))

        a_list = []
        print('The current directory is:')

        for files in dir_path:
            fullpath = directory + files
            if True == os.path.isfile(fullpath):
                a_list.append([files, int(getFileSize("MB", os.path.getsize(fullpath)))])
        for a in sorted(a_list, key=operator.itemgetter(1)):
            print("{0:>6d}MB  -  {1})".format(a[1], a[0]))
    else:
        print('Not a valid directory.')

def getFileSize(wanted_size, size):
    global return_size
    if wanted_size == "KB":
        return_size = size / 8192
    elif wanted_size == "MB":
        return_size = size / 1048576

    return return_size


if __name__ == "__main__": main()
