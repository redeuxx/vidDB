__author__ = ''

import dataset
import os

import time

class Dbfuncs:
    def __init__(self):

        # List of file extensions we are going to scan for.
        self.file_ext = (".mp4", ".avi", ".flv", ".wmv", ".mpg", ".mov", ".mkv", ".mpeg")

    def make_new_database(self, new_database_name, media_folder):
        start_time = time.time()  # FOR TESTING ... start time

        db = dataset.connect(('sqlite:///' + new_database_name))
        table = db['test']
        # add a loading bar or message indicating this may take a minute, alternatively thread it
        for root, dirs, files in os.walk(media_folder):
            for file in files:
                if file.endswith(self.file_ext):
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
        print("{} files in {} seconds".format(len(db['test']), end_time - start_time))

    def check_current(self):  # should run anytime a database opens confirming each file still exists (update)
        db = dataset.connect(('sqlite:///movies.vdb'))
        table = db['test']
        for file in table:
            if os.path.isfile(file['location']) is True:
                pass
            else:
                table.update(dict(name=(file('name')), ispresent=False), ['name'])
                print(file)

    def find_file(self, column, name):  # search function should be associated with a search bar in main window
        pass