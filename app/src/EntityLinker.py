import requests
import time

class EntityLinker:

    def __init__(self, docs_with_entities, es_path):
        self.docs_with_entities = docs_with_entities
        self.es_path = es_path

    def link(self):

        def link_freebase(row):

            # TODO: Maybe paralleize?

            def search(query):
                url = 'http://%s/freebase/label/_search' % self.es_path
                response = None
                for _ in range(5):
                    try:
                        response = requests.get(url, params={'q': query, 'size': 1000})
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
                ids = search(candidate["text"])
                linked_candidates.append({"label": candidate["text"], "ids": ids })
            return {"doc_id": row["doc_id"], "linked_candidates": linked_candidates}

        linked_entities = self.docs_with_entities.map(link_freebase)
        return linked_entities
