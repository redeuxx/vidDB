__author__ = 'austin'

import dataset
import os
import time

class Dbfuncs:
    def __init__(self):

        # List of file extensions we are going to scan for.
        self.file_ext = (".mp4", ".avi", ".flv", ".wmv", ".mpg", ".mov", ".mkv", ".mpeg")

    def check_current(self):  # should run anytime a database opens confirming each file still exists (update)
        db = dataset.connect(('sqlite:///files.vdb'))
        table = db['movies']
        for file in table:
            name = file['title']
            if os.path.isfile(file['location']) is True:
                pass
            else:
                table.delete(title=name)
                print(name)
        print('done')

    def find_file(self, column, name):  # search function should be associated with a search bar in main window
        pass
