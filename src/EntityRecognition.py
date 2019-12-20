import spacy

class EntityRecognition:

    def __init__(self, warc_docs):
        self.warc_docs = warc_docs

    def extract(self):
        """
            Named Entity Recognition using 'en_core_web_md' model of spaCy.
            - Data is provided to spaCy in paragraphs for better entity recognition
            - Numerical values are ignored for improving the quality of the entities recognised
        """
        def process(row):
            spacy_nlp = spacy.load("en_core_web_md")
            
            def spacy_extract(text):
                document = spacy_nlp(text)
                entity_list = []
                for element in document.ents:
                    text = element.text.strip("\n").replace("\n", "").replace("\r", "")
                    if element.label_ not in ["CARDINAL", "DATE", "QUANTITY", "TIME", "ORDINAL", "MONEY", "PERCENT", "QUANTITY"]:
                        entity = { "type" : element.label_, "text":text }
                        entity_list.append(entity)
                return entity_list
            entities = [spacy_extract(paragraph) for paragraph in row["paragraphs"]]
            return {"_id": row["_id"], "paragraph_entities": entities}

        self.docs_with_paragraph_entities = self.warc_docs.map(process)
        return self.docs_with_paragraph_entities
    
    def join_paragraphs(self):
        def execute_join(row):
            entities = [entity_result for paragraph in row["paragraph_entities"] for entity_result in paragraph]
            return {"_id": row["_id"], "entities": entities}

        self.docs_with_entities = self.docs_with_paragraph_entities.map(execute_join)
        return self.docs_with_entities
