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
                    for hit in response.get('hits', {}).get('hits', [])[:1]:
                        freebase_label = hit.get('_source', {}).get('label')
                        freebase_id = hit.get('_source', {}).get('resource')
                        id_labels.setdefault(freebase_id, set()).add(freebase_label)
                return id_labels

            linked_candidates = []
            for candidate in row["entities"]:
                # candidate is a tupel of {'text': 'XML-RPC', 'type': 'ORG'}
                ids = search(candidate["text"], es_path)
                linked_candidates.append({"label": candidate["text"], "ids": ids })
            return {"_id": row["_id"], "linked_candidates": linked_candidates}

        lambda_es_path = self.es_path
        query_lambda = lambda row : link_freebase(row, lambda_es_path)
        linked_entities = self.docs_with_entities.map(query_lambda)
        return linked_entities