import requests
import time
import json


class EntityLinker:

    def __init__(self, docs_with_entities, es_path):
        self.docs_with_entities = docs_with_entities
        self.es_path = es_path

    def link(self):
        
        def link_freebase(row, es_path):
            
            def search(query, es_path):

                params = ()
                data = {
                    "query": { 
                        "match": { "label": query }
                    },
                    "size": 10
                }
                json_qry = json.dumps(data)

                url = 'http://{0}/freebase/label/_search'.format(es_path)
                response = None
                for _ in range(5):
                    try:
                        response = requests.post(url, params=params, data=json_qry)
                        break
                    except:
                        time.sleep(0.5)

                id_labels = {}
                if response:
                    response = response.json()
                    for hit in response.get('hits', {}).get('hits', []):
                        freebase_label = hit.get('_source', {}).get('label')
                        freebase_id = hit.get('_source', {}).get('resource')
                        id_labels.setdefault(freebase_id, set()).add(freebase_label)
                return id_labels

            linked_candidates = []
            for candidate in row["entities"]:
                # candidate is a tupel of {'text': 'XML-RPC', 'type': 'ORG'}
                ids = search(candidate["text"], es_path)
                linked_candidates.append({"label": candidate["text"], "type": candidate["type"], "ids": ids })
            return {"_id": row["_id"], "linked_candidates": linked_candidates}

        lambda_es_path = self.es_path
        query_lambda = lambda row : link_freebase(row, lambda_es_path)
        self.linked_entities = self.docs_with_entities.map(query_lambda)
        return self.linked_entities

    def disambiguate(self, model_cache):
        # Create CBOW model 
        # download model from https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/view
        def apply_word2vec(row, mc):
            try:
                row["w2v"] = mc.w2v().similarity(row["linked_candidates"][0]["label"], 'spain')
            except:
                #word might not be in dict -> what to do?
                row["w2v"] = "word not in dict"
            return row
        
        apply_lbmd = lambda row: apply_word2vec(row, model_cache)
        self.dis_entities = self.linked_entities.map(apply_lbmd)
        return self.dis_entities