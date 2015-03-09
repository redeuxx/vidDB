__author__ = 'Vernon Wenberg III'

import tkinter as tk
import os
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk

import viddb.dirfuncs


class Options(object):
    """ Stores the directory sort option that has already been selected. Default sort method is by name. """
    sortby = None

    @classmethod
    def set_option(self, sortby):
        Options.sortby = sortby


class DrawGui(Options):
    def __init__(self):
        self.root = tk.Tk()
        self.entry_string = tk.StringVar()
        self.dir_checkbutton_state = tk.IntVar()
        self.create_widgets(self.root)
        self.root.title('vidDB.py')
        self.root.geometry("765x700")
        self.root.mainloop()

    def create_widgets(self, root):
        self.dirfuncs = viddb.dirfuncs.DirFuncs()


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
        self.the_file_menu.add_command(label="Exit", command=root.quit)

        # Sort by sub-menu
        """ Each sort option must pass a 'sortby' value which must then be created in self.build_dir_list
            and class 'DirFuncs'. """
        self.the_sort_menu = tk.Menu(root, tearoff=0)
        self.the_sort_menu.add_command(label="Name", command=lambda: self.build_dir_list(sortby="name"))
        self.the_sort_menu.add_command(label="Size", command=lambda: self.build_dir_list(sortby="size"))
        self.the_sort_menu.add_command(label="Date modified",
                                       command=lambda: self.build_dir_list(sortby="date_modified"))

        # View menu
        self.the_view_menu = tk.Menu(self.the_menu_bar, tearoff=0)
        self.the_menu_bar.add_cascade(label="View", menu=self.the_view_menu)
        self.the_view_menu.add_command(label="Refresh", command=lambda: self.build_dir_list(sortby=Options.sortby))
        self.the_view_menu.add_checkbutton(label="Hide directories", variable=self.dir_checkbutton_state, command=lambda: self.build_dir_list(sortby=Options.sortby))
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

        # Directory Entry Box
        self.directory_entry = tk.Entry(root, text="Directory")
        self.directory_entry.bind("<Return>", lambda event: self.build_dir_list(sortby=Options.sortby))
        self.directory_entry.pack(side=tk.TOP, expand=tk.NO, anchor=tk.NW, fill=tk.X)

        # Filename Tree
        self.tree = ttk.Treeview(root)  # Initialize tree
        self.tree["columns"] = ("Filename", "Size", "Date Modified")
        self.tree["show"] = 'headings'  # hide the first column
        self.tree.column("Filename", width=400, stretch=False)
        self.tree.column("Size", width=150, stretch=False)
        self.tree.column("Date Modified", width=200, stretch=False)
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
        self.right_click_menu = tk.Menu(self.root, tearoff=0)  # Creates the right click menu in directory list
        self.right_click_menu.add_command(label="Open", command=self.dir_list_open)
        self.right_click_menu.add_command(label="Delete", command=self.dir_list_remove)
        self.tree.bind("<Button-3>", self.dir_list_right_click_menu)

    def get_show_dir_checkb_val(self):
        """
        :return: checks the stae of the 'Show directories' option and returns 1 or 0
        """
        checkbutton_state = self.dir_checkbutton_state.get()
        return checkbutton_state

    def build_dir_list(self, event=None, sortby=None):
        self.directory_name = self.directory_entry.get()
        for var in self.tree.get_children():
            self.tree.delete(var)

        # Set sort method if not set, otherwise use existing sort method
        if sortby is None:
            Options.set_option("name")
        else:
            Options.set_option(sortby)

        # If directory exists, list contents, otherwise pop-up an error
        if os.path.isdir(self.directory_name):
            # Only get directories if Hide directories option is not selected
            if self.get_show_dir_checkb_val() == 0:
                dir_dir_list = self.dirfuncs.directory_dir_list(self.directory_name, Options.sortby)
                if dir_dir_list:
                    for a in dir_dir_list:
                        self.tree.insert("", "end", values=a)

            dir_file_list = self.dirfuncs.directory_file_list(self.directory_name, Options.sortby)
            if dir_file_list:
                for a in dir_file_list:
                    self.tree.insert("", "end", values=a)
                self.tree.bind("<Double-1>", self.dir_list_open)
            else:
                pass
        else:
            tk.messagebox.showerror("Error", "Directory does not exist")

    def dir_list_remove(self):
        selection_id = self.tree.selection()
        delete_answer = tk.messagebox.askyesno("Delete File",
                                               "Are you sure you want to delete {0} files?".format(len(selection_id)))
        if delete_answer:
            for item_id in selection_id:
                item_name = os.path.join(self.directory_name, self.tree.item(item_id)['values'][0])
                os.remove(item_name)
        else:
            pass
        self.build_dir_list(sortby=Options.sortby)

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


def main():
    DrawGui()

if __name__ == "__main__":
    main()