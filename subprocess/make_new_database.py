__author__ = 'austin'

import tkinter as tk
import dataset
import os
import time
import tkinter.filedialog
import tkinter.simpledialog


def make_new_database():
    file_ext = (".mp4", ".avi", ".flv", ".wmv", ".mpg", ".mov", ".mkv", ".mpeg")

    start_time = time.time()  # FOR TESTING ... start time

    media_folder = tk.filedialog.askdirectory(title="open folder")
    new_database_name = (tk.simpledialog.askstring(title='name new database',
                                                   prompt='name the new database'))
    db = dataset.connect('sqlite:///files.vdb')
    table = db[new_database_name]
    for root, dirs, files in os.walk(media_folder):
        for file in files:
            if file.endswith(file_ext):
                if table.find_one(title=file[:-4]) is None:
                    table.insert(dict(title=file[:-4],
                                      location=(root + '/' + file),
                                      genre='none',
                                      length='none',
                                      ispresent=True))
                    print(root + '/' + file)
                else:
                    pass
            else:
                pass

    end_time = time.time()
    print("{} files in {} seconds".format(len(db[new_database_name]), end_time - start_time))
    exit()


make_new_database()