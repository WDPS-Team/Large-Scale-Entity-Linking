import json
import os
import spacy

class EntityExtractor:

    def __init__(self, warc_docs):
        self.warc_docs = warc_docs
    
    def extract(self):

        def process(row):
            # TODO: change to bigger model
            spacy_nlp = spacy.load("en_core_web_sm")
            document = spacy_nlp(row['data'].strip())
            entity_list = []
            for element in document.ents:
                entity = dict(type=element.label_, text=element.text)
                entity_list.append(entity)

            return {"doc_id": row["id"], "entities": entity_list}

        docs_with_entities = self.warc_docs.map(process)
        return docs_with_entities
