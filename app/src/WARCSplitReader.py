#from config import TMP_FOLDER, WARC_ID, WARC_PER_DOC
#from warcio.archiveiterator import ArchiveIterator
#from lxml.html.clean import Cleaner
#import lxml.html as lh
#import json

# def getTextFromHTML(html):
#     cleaner = Cleaner()
#     cleaner.javascript = True
#     cleaner.style = True
#     clean_html = cleaner.clean_html(html)
#     return clean_html.text_content()
#
#
# def extractWarcRecordsList(stream):
#     warcRecords = []
#     for record in ArchiveIterator(stream):
#         try:
#             if record.rec_type == 'response':           #filters by responce warcs
#                 html = record.content_stream().read()   #reads payload from the record
#                 if len(html) > 0:
#                     rec_id = record.rec_headers.get_header(WARC_ID)
#                     data = getTextFromHTML(lh.fromstring(html))
#                     warcRecords.append({
#                         'id'  : rec_id,
#                         'data': data
#                     })
#         except:
#                 print("Parse error:", record.rec_headers.get_header(WARC_ID))
#     return warcRecords
#
#
# def extractWarcRecords(file):
#     with open(file, 'rb') as f:
#         return extractWarcRecordsList(f)
#
#
# def storeWarcData(records, folder):
#     for i in range(0, int(len(records)/WARC_PER_DOC) + 1):
#         beg = i * WARC_PER_DOC
#         end = (i + 1) * WARC_PER_DOC
#         recordPart = records[beg:end]
#         fileName = folder + "/" + "warc-{:05d}.json".format(i)
#         with open(fileName, 'w', encoding='utf-8') as json_file:
#             json.dump(recordPart, json_file)
#
#
# def emptyOutputDirectory(folder):
#     import os
#     import shutil
#
#     if os.path.exists(folder):
#         shutil.rmtree(folder)
#     os.mkdir(folder)
#
# if __name__ == "__main__":
#     import sys
#
#     if len(sys.argv) < 3:
#         print('Usage: <INPUT_FILE> <OUTPUT_FOLDER>. Using "sample.warc.gz" and "',TMP_FOLDER,'" instead.')
#         INPUT = "sample.warc.gz"
#         OUTPUT = TMP_FOLDER
#     else:
#         _, INPUT, OUTPUT = sys.argv
#
#     emptyOutputDirectory(OUTPUT)
#     records = extractWarcRecords(INPUT)
#     storeWarcData(records, OUTPUT)
