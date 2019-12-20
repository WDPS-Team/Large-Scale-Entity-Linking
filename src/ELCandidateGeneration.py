import requests
import time
import json

class ELCandidateGeneration:

    def __init__(self, docs_with_entities, es_path, ranking_threshold, model_root_path):
        self.docs_with_entities = docs_with_entities
        self.es_path = es_path
        self.ranking_threshold = ranking_threshold
        self.model_root_path = model_root_path

    def get_candidates_from_elasticsearch(self):

        def link_freebase(row, es_path):

            def search(query, es_path):

                params = ()
                data = {
                    "query": {
                        "match": {"label": query}
                    },
                    "size": 70
                }
                json_qry = json.dumps(data)

                url = 'http://{0}/freebase/label/_search'.format(es_path)
                response = None
                for _ in range(10):
                    try:
                        response = requests.post(
                            url, params=params, data=json_qry)
                        break
                    except:
                        time.sleep(0.1)

                id_labels = {}
                if response:
                    response = response.json()
                    for hit in response.get('hits', {}).get('hits', []):
                        freebase_label = hit.get('_source', {}).get('label')
                        freebase_id = hit.get('_source', {}).get('resource')
                        id_labels.setdefault(
                            freebase_id, set()).add(freebase_label)
                return id_labels

            linked_candidates = []
            for candidate in row["entities"]:
                # candidate is a tupel of {'text': 'XML-RPC', 'type': 'ORG'}
                ids = search(candidate["text"], es_path)
                linked_candidates.append(
                    {"label": candidate["text"], "type": candidate["type"], "ids": ids})
            return {"_id": row["_id"], "linked_candidates": linked_candidates}

        lambda_es_path = self.es_path
        def query_lambda(row): return link_freebase(row, lambda_es_path)
        self.linked_candidate_entities = self.docs_with_entities.map(query_lambda)
        return self.linked_candidate_entities