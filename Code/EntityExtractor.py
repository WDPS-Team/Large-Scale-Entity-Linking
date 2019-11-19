import json
import sys
import os
import spacy

INPUT = ""

def extractJson(folder):
    count = 0
    files_list = os.listdir(folder)
    for file_name in files_list:
        with open(folder + "/" + file_name) as json_file:
            data = json.load(json_file)
            for p in data:
                print(p['id'])
                document = spacy_nlp(p['data'].strip())
                for element in document.ents:
                    print('Type: %s, Value: %s' % (element.label_, element))
                count = count + 1

    print("Total records:", count)


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print('Usage: <INPUT_FOLDER>. Using "warc_parse" instead.')
        INPUT = "warc_parse"
    else:
        INPUT = sys.argv[1]

    spacy_nlp = spacy.load('en')
    extractJson(INPUT)