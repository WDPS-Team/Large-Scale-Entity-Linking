import json
import os
import spacy


class EntityRecognition:

    def __init__(self, warc_docs):
        self.warc_docs = warc_docs

    def extract(self):
        def process(row):
            spacy_nlp = spacy.load("en_core_web_md")
            
            def spacy_extract(text):
                document = spacy_nlp(text)
                entity_list = []
                for element in document.ents:
                    text = element.text.strip("\n").replace("\n", "").replace("\r", "")
                    if element.label_ not in ["CARDINAL", "DATE", "QUANTITY", "TIME", "ORDINAL", "MONEY", "PERCENT", "QUANTITY"]:
                        entity = dict(type=element.label_, text=text)
                        entity_list.append(entity)
                return entity_list
            entities = [spacy_extract(sentence) for sentence in row["sentences"]]
            return {"_id": row["_id"], "sentences_entities": entities}

        self.docs_with_sentences_entities = self.warc_docs.map(process)
        return self.docs_with_sentences_entities
    
    def join_sentences(self):
        def execute_join(row):
            entities = [entity_result for sentence in row["sentences_entities"] for entity_result in sentence]
            return {"_id": row["_id"], "entities": entities}

        self.docs_with_entities = self.docs_with_sentences_entities.map(execute_join)
        return self.docs_with_entities
