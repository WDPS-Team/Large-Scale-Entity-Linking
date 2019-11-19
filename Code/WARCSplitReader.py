import json
import os
import sys
import shutil
import lxml.html as lh
from warcio.archiveiterator import ArchiveIterator
from lxml.html.clean import Cleaner

INPUT = ""
OUTPUT = ""
WARC_ID = "WARC-TREC-ID"
FILES_PER_DOC = 500


def storeWarcData(count, warcRecords):
    fileName = OUTPUT + "/" + "warc-{:05d}.json".format(int(count/FILES_PER_DOC))
    with open(fileName, 'w', encoding='utf-8') as json_file:
        json.dump(warcRecords, json_file)
        warcRecords = []


def getTextFromHTML(html):
    cleaner = Cleaner()
    cleaner.javascript = True
    cleaner.style = True
    clean_html = cleaner.clean_html(html)
    return clean_html.text_content()


def divideAndStoreWarc(file):
    count = 0
    error_count = 0
    warcRecords = []
    with open(file, 'rb') as f:
        for record in ArchiveIterator(f):
            try:
                if record.rec_type == 'response':           #filters by responce warcs
                    html = record.content_stream().read()   #reads payload from the record
                    if len(html) > 0:
                        id = record.rec_headers.get_header(WARC_ID)
                        data = getTextFromHTML(lh.fromstring(html))

                        print(data)

                        warcRecords.append({
                            'id'  : id,
                            'data': data
                        })
                        
                        count = count + 1
                        if count % FILES_PER_DOC == 0:
                            storeWarcData(count, warcRecords)
                            warcRecords = []                #empty warc records after storing
                            
                       
            except:
                error_count = error_count + 1
                print("Parse error:", record.rec_headers.get_header(WARC_ID))
        
        if len(warcRecords) > 0:
            storeWarcData(count + FILES_PER_DOC, warcRecords)   #store the last set of records
    print("WARC Records parsed:", count)


def emptyDirectory(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: <INPUT_FILE> <OUTPUT_FOLDER>. Using "sample.warc.gz" and "warc_parse" instead.')
        INPUT = "sample.warc.gz"
        OUTPUT = "warc_parse"
    else:
        INPUT = sys.argv[1]
        OUTPUT = sys.argv[2]	

    emptyDirectory(OUTPUT)
    divideAndStoreWarc(INPUT)