__author__ = 'Vernon Wenberg III'

import os
import operator
import tkinter as tk
from tkinter import ttk
from sys import exit
import tkinter.messagebox
import tkinter.filedialog


class DrawGui:
    def __init__(self, root):
        self.dirfuncs = DirFuncs()
        self.entry_string = tk.StringVar()
        self.right_click_menu = tk.Menu(root, tearoff=0)  # Creates the right click menu in directory list

        # START MENU BAR
        self.theMenuBar = tk.Menu(root)
        root.config(menu=self.theMenuBar)

        self.theFileMenu = tk.Menu(self.theMenuBar, tearoff=0)  # File sub menu
        self.theFileMenu.add_command(label="New Database", command=self.create_new_database)
        self.theFileMenu.add_command(label="Exit", command=lambda: exit(0))
        self.theAboutMenu = tk.Menu(self.theMenuBar, tearoff=0)  # Help sub menu
        self.theAboutMenu.add_command(label="About", command=lambda: tk.messagebox.showinfo
            ("About",
             """
            vidDB.py
            by Vernon Wenberg III
            http://ribbed.us
            """))

        self.theMenuBar.add_cascade(label="File", menu=self.theFileMenu)
        self.theMenuBar.add_cascade(label="Help", menu=self.theAboutMenu)
        # END MENU BAR

        # START Directory Entry Box
        self.directory_label = tk.Label(root, text="Directory")
        self.directory_label.grid(row=1, column=0, sticky=tk.W)
        self.directory_entry = tk.Entry(root, width=200, textvariable=self.entry_string)
        self.directory_entry.bind("<Return>", self.build_dir_list)
        self.directory_entry.grid(row=1, column=1, stick=tk.EW)
        # END Directory Entry Box

        # START Filename Tree
        self.tree = ttk.Treeview(root)
        self.tree["columns"] = ("Filename", "Size")
        self.tree["show"] = 'headings'  # hide the first column
        self.tree.column("Filename", width=700)
        self.tree.column("Size", width=20)
        self.tree.heading("Filename", text="Filename")
        self.tree.heading("Size", text="Size")
        self.tree.grid(row=2, sticky=tk.EW, columnspan=2)
        #  END Filename Tree

        # START Right click menu on directory list
        self.right_click_menu.add_command(label="Open", command=self.dir_list_open)
        self.right_click_menu.add_command(label="Something Something", command=lambda: print("hola!"))
        self.tree.bind("<Button-3>", self.dir_list_right_click_menu)
        # END Right click menu on directory list

    def build_dir_list(self, event=None):
        self.directory_name = self.directory_entry.get()
        for var in self.tree.get_children():
            self.tree.delete(var)

        dir_list = self.dirfuncs.directory_list(self.directory_name)
        if dir_list:
            for a in dir_list:
                self.tree.insert("", "end", values=a)
            # TODO: Adjust column width to longest filename
            # TODO: Add size indicator (eg: MB, KB, GB)
            # self.tree.column("Filename", width=50)
            self.tree.bind("<Double-1>", self.dir_list_open)
        else:
            pass

    def dir_list_open(self, event=None):
        item_id = self.tree.focus()
        item_name = os.path.join(self.directory_name, self.tree.item(item_id)['values'][0])
        os.startfile(item_name)

    def dir_list_right_click_menu(self, event):
        self.right_click_menu.post(event.x_root, event.y_root)

    def create_new_database(self):
        self.database_location = tk.filedialog.asksaveasfilename(title="Create new database",
                                                                 filetypes=[("Video Database", "*.vdb")],
                                                                 defaultextension=".vdb")
        print(self.database_location)


class DirFuncs:
    def __init__(self):
        self.a_list = []
        self.dir_list = []

    def directory_list(self, directory):
        del self.a_list[:]
        del self.dir_list[:]

        if os.path.isdir(directory):
            dir_path = os.listdir(directory)
            for files in dir_path:
                fullpath = os.path.join(directory, files)
                if os.path.isfile(fullpath):
                    self.a_list.append([files, int(get_file_size("MB", os.path.getsize(fullpath)))])
            for a in sorted(self.a_list, key=operator.itemgetter(1)):
                self.dir_list.append([a[0], a[1]])

            return self.dir_list
        else:
            tk.messagebox.showerror("Error", "Invalid Directory")
            return False


def main():
    root = tk.Tk()

    DrawGui(root)
    root.title('vidDB.py')

    root.mainloop()


def get_file_size(wanted_size, size):
    if wanted_size == "KB":
        return_size = size / 8192
    elif wanted_size == "MB":
        return_size = size / 1048576

    return return_size


if __name__ == "__main__":
    main()