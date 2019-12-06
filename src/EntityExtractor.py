import json
import os
import spacy


class EntityExtractor:

    def __init__(self, warc_docs):
        self.warc_docs = warc_docs

    def extract(self):
        def process(row):
            # TODO: change to bigger model
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
            entities = [entity_result for sentence in row["npl_text"] for entity_result in spacy_extract(sentence)]
            return {"doc_id": row["_id"], "entities": entities}

        docs_with_entities = self.warc_docs.map(process)
        return docs_with_entities
