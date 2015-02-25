__author__ = 'Vernon Wenberg III'

import os
import operator
import tkinter as tk
from sys import exit
import tkinter.messagebox


class drawGui:

    def __init__(self, root):
        # START MENU BAR
        self.theMenuBar = tk.Menu(root)
        root.config(menu=self.theMenuBar)

        self.theFileMenu = tk.Menu(self.theMenuBar, tearoff=0)  # File sub menu
        self.theFileMenu.add_command(label="Exit", command=lambda: exit(0))
        self.theAboutMenu = tk.Menu(self.theMenuBar, tearoff=0)  # Help sub menu
        self.theAboutMenu.add_command(label="About", command=lambda: tk.messagebox.showinfo("About",
            """
            vidDB.py
            by Vernon Wenberg III
            http://ribbed.us
            """))

        self.theMenuBar.add_cascade(label="File", menu=self.theFileMenu)
        self.theMenuBar.add_cascade(label="Help", menu=self.theAboutMenu)
        # END MENU BAR

        self.entry_string = tk.StringVar()

        self.directory_label = tk.Label(root, text="Directory")
        self.directory_label.grid(row=1, column=0, sticky=tk.W)
        self.directory_entry = tk.Entry(root, width=200, textvariable=self.entry_string)
        # next line: use lambda to pass directory name variable from GUI entry box
        self.directory_entry.bind("<Return>", lambda event, arg=self.entry_string: test(event, arg))
        self.directory_entry.grid(row=1, column=1, stick=tk.EW)


def main():
    root = tk.Tk()

    drawGui(root)
    root.title('vidDB.py')

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
            print("{0:>6d}MB  -  {1}".format(a[1], a[0]))
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