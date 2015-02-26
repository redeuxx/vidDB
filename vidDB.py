__author__ = 'Vernon Wenberg III'

import os
import operator
import tkinter as tk
from tkinter import ttk
from sys import exit
import tkinter.messagebox


class DrawGui:

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
        # self.directory_entry.bind("<Return>", (lambda event, arg=self.entry_string: DirFuncs.getDir(event, arg)))
        self.directory_entry.bind("<Return>", self.build_dir_list)
        self.directory_entry.grid(row=1, column=1, stick=tk.EW)

        #  START Filename Tree
        self.tree = ttk.Treeview(root)
        self.tree["columns"] = ("Filename", "Size")
        self.tree["show"] = 'headings' # hide the first column
        self.tree.column("Filename", width=700)
        self.tree.column("Size", width=20)
        self.tree.heading("Filename", text="Filename")
        self.tree.heading("Size", text="Size")
        # self.tree.insert("", "end", values="test, test1")
        self.tree.grid(row=2, sticky=tk.EW, columnspan=2)

    def build_dir_list(self, event):
        dirfuncs = DirFuncs()
        self.directory_name = self.directory_entry.get()
        print(self.directory_name)
        dir_list = dirfuncs.directory_list(self.directory_name)
        for a in dir_list:
            self.tree.insert("", "end", values=a)
        # TODO: Adjust column width to longest filename
        # TODO: Add size indicator (eg: MB, KB, GB)
        # self.tree.column("Filename", width=50)


class DirFuncs:

    def __init__(self):
        print("NOTHING HERE")
        self.a_list = []
        self.dir_list = []

    def directory_list(self, directory):
        # directory = arg.get()  # get directory from GUI entry box
        print(directory)
        if True == os.path.isdir(directory):
            dir_path = os.listdir(directory)
            for files in dir_path:
                fullpath = os.path.join(directory, files)
                if True == os.path.isfile(fullpath):
                    self.a_list.append([files, int(getFileSize("MB", os.path.getsize(fullpath)))])
            for a in sorted(self.a_list, key=operator.itemgetter(1)):
                print("{0:>6d}MB  -  {1}".format(a[1], a[0]))
                self.dir_list.append([a[0], a[1]])

            return self.dir_list
        else:
            print('Not a valid directory.')


def main():
    root = tk.Tk()

    DrawGui(root)
    root.title('vidDB.py')

    root.mainloop()


def getFileSize(wanted_size, size):
    global return_size
    if wanted_size == "KB":
        return_size = size / 8192
    elif wanted_size == "MB":
        return_size = size / 1048576

    return return_size

if __name__ == "__main__": main()