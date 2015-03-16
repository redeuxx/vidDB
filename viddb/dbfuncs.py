__author__ = ''

import dataset
import os

class Dbfuncs:

    def make_new_database(new_database_name, media_folder):
        db = dataset.connect(('sqlite:///' + new_database_name))
        table = db['test']
        # add a loading bar or message indicating this may take a minute, alternatively thread it
        for root, dirs, files in os.walk(media_folder):
            for file in files:
                if file.endswith((".mp4", ".avi", ".flv", ".wmv", ".mov")):
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
        print(len(db['test']))


    def check_current():  # should run anytime a database opens confirming each file still exists (update)
        db = dataset.connect(('sqlite:///movies.vdb'))
        table = db['test']
        for file in table:
            if os.path.isfile(file['location']) is True:
                pass
            else:
                table.update(dict(name=(file('name')), ispresent=False), ['name'])
                print(file)

    def find_file(colomn, name): # search function should be associated with a search bar in main window
        pass

