__author__ = 'Vernon Wenberg III'

import os
import time
import operator
import tkinter as tk
from tkinter import ttk
from sys import exit
import tkinter.messagebox
import tkinter.filedialog


class DrawGui:
    def __init__(self):
        self.root = tk.Tk()
        self.create_widgets(self.root)
        self.root.title('vidDB.py')
        self.root.state("zoomed")
        self.root.mainloop()

    def create_widgets(self, root):
        self.dirfuncs = DirFuncs()
        self.entry_string = tk.StringVar()
        self.right_click_menu = tk.Menu(self.root, tearoff=0)  # Creates the right click menu in directory list

        # Menu bar
        self.the_menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.the_menu_bar)
        self.top = self.root.winfo_toplevel()
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # File menu
        self.the_file_menu = tk.Menu(self.the_menu_bar, tearoff=0)
        self.the_menu_bar.add_cascade(label="File", menu=self.the_file_menu)
        self.the_file_menu.add_command(label="New Database", command=self.create_new_database)
        self.the_file_menu.add_command(label="Exit", command=lambda: exit(0))

        # Sort by sub-menu
        """ Each sort option must pass a 'sortby' value which must then be created in self.build_dir_list
            and class 'DirFuncs'. """
        self.the_sort_menu = tk.Menu(root, tearoff=0)
        self.the_sort_menu.add_command(label="Name", command=lambda: self.build_dir_list(sortby="name"))
        self.the_sort_menu.add_command(label="Size", command=lambda: self.build_dir_list(sortby="size"))
        self.the_sort_menu.add_command(label="Date modified", command=lambda: self.build_dir_list(sortby="date_modified"))

        # View menu
        self.the_view_menu = tk.Menu(self.the_menu_bar, tearoff=0)
        self.the_menu_bar.add_cascade(label="View", menu=self.the_view_menu)
        self.the_view_menu.add_cascade(label="Sort by", menu=self.the_sort_menu)

        # Help menu
        self.the_about_menu = tk.Menu(self.the_menu_bar, tearoff=0)
        self.the_menu_bar.add_cascade(label="Help", menu=self.the_about_menu)
        self.the_about_menu.add_command(label="About", command=lambda: tk.messagebox.showinfo
        ("About",
         """
            vidDB.py
            by Vernon Wenberg III
            http://ribbed.us
            """))

        #  Directory Entry Box
        self.directory_entry = tk.Entry(root, text="Directory")
        self.directory_entry.bind("<Return>", self.build_dir_list)
        self.directory_entry.pack(side=tk.TOP, expand=tk.NO, anchor=tk.NW, fill=tk.X)

        # Filename Tree
        self.tree = ttk.Treeview(root)  # Initialize tree
        self.tree["columns"] = ("Filename", "Size", "Date Modified")
        self.tree["show"] = 'headings'  # hide the first column
        self.tree.column("Filename", width=700)
        self.tree.column("Size", width=20)
        self.tree.column("Date Modified", width=20)
        self.tree.heading("Filename", text="Filename")
        self.tree.heading("Size", text="Size")
        self.tree.heading("Date Modified", text="Date Modified")
        self.tree.pack(fill=tk.BOTH, anchor=tk.NW, expand=tk.YES)

        # Tree scrollbar
        """ Calling ttk.Scrollbar() for self.tree must come after ttk.Treeview is initialized """
        self.scrollbar = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        """ setting 'yscrollcommand' can only be called after ttk.Scrollbar is initialized """
        self.tree.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.tree.yview)
        self.scrollbar.pack(anchor=tk.NE, fill=tk.Y, expand=tk.YES)

        # Right click menu on directory list
        self.right_click_menu.add_command(label="Open", command=self.dir_list_open)
        self.right_click_menu.add_command(label="Something Something", command=lambda: print("hola!"))
        self.tree.bind("<Button-3>", self.dir_list_right_click_menu)
        # END Right click menu on directory list

    def build_dir_list(self, event=None, sortby="name"):
        self.directory_name = self.directory_entry.get()
        for var in self.tree.get_children():
            self.tree.delete(var)

        dir_list = self.dirfuncs.directory_list(self.directory_name, sortby)
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

    def directory_list(self, directory, sortby):
        del self.a_list[:]
        del self.dir_list[:]

        if sortby == "name":
            sort_by_value = 0
        elif sortby == "size":
            sort_by_value = 1
        elif sortby == "date_modified":
            sort_by_value = 2
        else:
            pass

        if os.path.isdir(directory):
            dir_path = os.listdir(directory)
            for files in dir_path:
                fullpath = os.path.join(directory, files)
                if os.path.isfile(fullpath):
                    self.a_list.append(
                        [files, int(get_file_size("MB", os.path.getsize(fullpath))), os.path.getmtime(fullpath)])
            for a in sorted(self.a_list, key=operator.itemgetter(sort_by_value)):
                self.dir_list.append([a[0], a[1], time.ctime(a[2])])

            return self.dir_list
        else:
            tk.messagebox.showerror("Error", "Invalid directory")
            return False


def main():
    DrawGui()


def get_file_size(wanted_size, size):
    if wanted_size == "KB":
        return_size = size / 8192
    elif wanted_size == "MB":
        return_size = size / 1048576

    return return_size


if __name__ == "__main__":
    main()