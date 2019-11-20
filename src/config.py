SAMPLE_INPUT="data/sample.warc.gz"
FREEBASE_DOMAIN="localhost:9200"
TMP_FOLDER="intermediate"
WARC_ID = "WARC-TREC-ID"
WARC_PER_DOC = 5

def suppress_invalid_gzip():
    print("Configuring")
    import warcio
    import os
    from shutil import copyfile

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

if __name__ == "__main__":
    suppress_invalid_gzip()
