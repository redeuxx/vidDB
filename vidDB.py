__author__ = 'Vernon Wenberg III'

import os
import operator
import tkinter as tk

def main():
    root = tk.Tk()
    root.title('vidDB.py')

    entry_string = tk.StringVar()

    directory_label = tk.Label(root, text="Directory")
    directory_label.grid(row=0, column=0, sticky=tk.W)
    directory_entry = tk.Entry(root, width=200, textvariable=entry_string)
    # next line: use lambda to pass directory name variable from GUI entry box
    directory_entry.bind("<Return>", lambda event, arg=entry_string: test(event, arg))
    directory_entry.grid(row=0, column=1, stick=tk.EW)

    root.mainloop()

def test(event, arg):
    directory = arg.get()  # get directory from GUI entry box
    if True == os.path.isdir(directory):
        dir_path = os.listdir(directory)
        print(type(dir))

        a_list = []
        print('The current directory is:')

        for files in dir_path:
            fullpath = os.path.join(directory, files)
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