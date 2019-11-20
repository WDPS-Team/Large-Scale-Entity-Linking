import warcio
import os
from shutil import copyfile

def suppress_invalid_gzip():
    # avoid raising error for multiple non-chunked records of .warc.gz files and encoding issues
    warcioPath = os.path.dirname(warcio.__file__)
    filePath = warcioPath + '/archiveiterator.py'
    copyfile(filePath, filePath + ".backup")

    fin = open(filePath, "rt")
    data = fin.read()
    data = data.replace("raise_invalid_gzip = True", "raise_invalid_gzip = False")
    fin.close()

    fin = open(filePath, "wt")
    fin.write(data)
    fin.close()

suppress_invalid_gzip()