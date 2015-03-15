__author__ = ''

import dataset
import os


class Dbfuncs:
    def __init__(self):
        pass

    def make_new_database(self, new_database_name):
        db = dataset.connect(('sqlite:///' + new_database_name))
        table = db['test']
        # tk.messagebox('this may take a few minutes')
        for root, dirs, files in os.walk(self.media_folder):
            for file in files:
                if file.endswith((".mp4", ".avi", ".flv", ".wmv", ".mov")):
                    if table.find_one(title=file[:-4]) is None:
                        table.insert(dict(title=file[:-4], location=(root + '/' + file), genre='none', length='none'))
                        print(root + '/' + file)
                    else:
                        pass
                else:
                    pass