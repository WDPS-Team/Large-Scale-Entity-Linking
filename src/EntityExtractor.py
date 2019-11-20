import json
import os
import spacy

from config import TMP_FOLDER

class EntityExtractor:

    def __init__(self, type='en'):
        self.spacy_nlp = spacy.load(type)
    
    def extract(self, folder):
        files_list = os.listdir(folder)
        entityList = []
        
        for file_name in files_list:
            with open(folder + "/" + file_name) as json_file:
                data = json.load(json_file)
                for p in data:
                    document = self.spacy_nlp(p['data'].strip())
                    for element in document.ents:
                        entity = dict(doc_id=p['id'], type=element.label_, text=element.text)
                        entityList.append(entity)
        return entityList


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print('Usage: <INPUT_FOLDER>. Using "',TMP_FOLDER,'" instead.')
        INPUT = TMP_FOLDER
    else:
        INPUT = sys.argv[1]

    entities = EntityExtractor('en')
    entityList = entities.extract(INPUT)

    for entity in entityList:
        print(entity)