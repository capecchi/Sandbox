# *********************************************************************************
# path = top directory level- everything within this folder will be renamed
# verbose = if set to True (default) will print out folder paths as they are renamed
# example path = 'C:\\Users\\Owner\\Desktop\\Projects\\Upwork\\Osvaldo_Landi\\dummy_files\\'
# *********************************************************************************

import os
global newfilenum
global newdirnum


def main(path=None, verbose=True):
    global newfilenum
    global newdirnum

    if path is None:
        print("Please set path keyword, ex: path='C:\\Documents\\'")
    else:
        newfilenum = 0
        newdirnum = 0
        clean(path, verbose=verbose)  # Rename everything within '\\path'
        if verbose:
            print('cleaning complete!')


def clean(path, verbose=True):
    if verbose:
        print('Cleaning: ' + path)

    global newfilenum
    global newdirnum

    contents = os.listdir(path)  # get list of contents, including subdirectories
    for c in contents:
        if os.path.isfile(path + c):  # if this is a file, we rename and move on
            # if a file exists with what we were going to rename our file, iterate newfilenum until we get a new filename
            while os.path.isfile(path+'f'+str(newfilenum)):
                newfilenum += 1
            os.rename(path + c, path + 'f' + str(newfilenum))
            newfilenum += 1
        if os.path.isdir(path + c):  # if this is a directory, we call 'clean' to rename everything within it
            clean(path + c + '\\', verbose=verbose)
            while os.path.isdir(path+'d'+str(newdirnum)):
                newdirnum += 1
            newdirname = 'd' + str(newdirnum)
            newdirnum += 1
            os.rename(path + c, path + newdirname)  # we rename the directory once everything inside has been renamed


#if __name__ == '__main__':
#    main(path='C:\\Users\\Owner\\Desktop\\Projects\\Upwork\\Osvaldo_Landi\\dummy_files\\', verbose=False)
