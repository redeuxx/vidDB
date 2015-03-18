__author__ = 'austin'

import dataset
import os
import time
import sys


def make_new_database(new_database_name, media_folder):
    file_ext = (".mp4", ".avi", ".flv", ".wmv", ".mpg", ".mov", ".mkv", ".mpeg")

    start_time = time.time()  # FOR TESTING ... start time

    db = dataset.connect('sqlite:///{}.vdb'.format(new_database_name))
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
    exit(0)  # TODO need to specify different exit codes on different errors, so we can handle these errors


def main():
    new_database_name = sys.argv[1]
    media_folder = sys.argv[2]
    make_new_database(new_database_name, media_folder)

if __name__ == "__main__":
    main()