__author__ = 'Vernon'

import os
import operator
import time


def size_of(num, suffix='B'):
    """
    @:desc   Generates human readable file sizes
    @:param  num - long
    @:return Returns a human readable file size in a string variable
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


class DirFuncs:
    def __init__(self):
        self.a_list = []
        self.dir_file_list = []
        self.dir_dir_list = []

    def directory_file_list(self, directory, sortby):
        """
        @:desc   Builds a list of files, sans directories.
        @:param  directory - string, sortby - string
        @:return Returns a list[0:2] with filename, size, date modified.
        """
        del self.a_list[:]
        del self.dir_file_list[:]

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
                        [files, os.path.getsize(fullpath), os.path.getmtime(fullpath)])
                else:
                    pass
            for a in sorted(self.a_list, key=operator.itemgetter(sort_by_value)):
                self.dir_file_list.append([a[0], size_of(a[1]), time.ctime(a[2])])
            return self.dir_file_list
        else:
            return False

    def directory_dir_list(self, directory, sortby):
        """
        @:desc   Builds a list of directories, sans files.
        @:param  directory - string, sortby - string
        @:return Returns a list[0:2] with filename, " ", date modified.
        """
        del self.a_list[:]
        del self.dir_dir_list[:]

        if sortby == "name":
            sort_by_value = 0
        elif sortby == "size":
            sort_by_value = 0
        elif sortby == "date_modified":
            sort_by_value = 1
        else:
            pass

        if os.path.isdir(directory):
            dir_path = os.listdir(directory)
            for dir in dir_path:
                fullpath = os.path.join(directory, dir)
                if os.path.isdir(fullpath):
                    try:  # On Windows permission error. Don't even get the directory last modified value.
                        self.a_list.append(
                            [dir, os.path.getmtime(fullpath)])
                    except PermissionError:
                        self.a_list.append([dir, 0])
                else:
                    pass

            for a in sorted(self.a_list, key=operator.itemgetter(sort_by_value)):
                self.dir_dir_list.append([a[0], "", time.ctime(a[1])])
            return self.dir_dir_list
        else:
            return False