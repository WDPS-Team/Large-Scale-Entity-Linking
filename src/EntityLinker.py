import requests
import time
import json
from LexVec import ModelCache


class EntityLinker:

    def __init__(self, docs_with_entities, es_path, ranking_threshold, model_root_path):
        self.docs_with_entities = docs_with_entities
        self.es_path = es_path
        self.ranking_threshold = ranking_threshold
        self.model_root_path = model_root_path

    def get_entity_linking_candidates(self):

        def link_freebase(row, es_path):

            def search(query, es_path):

                params = ()
                data = {
                    "query": {
                        "match": {"label": query}
                    },
                    "size": 30
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
        self.linked_entities = self.docs_with_entities.map(query_lambda)
        return self.linked_entities

    def rank_entity_candidates(self):
        def rank_candidates(row, mc, ranking_threshold):
            ranking = []

            try:
                for candidate in row["linked_candidates"]:
                    label_vector = mc.model().word_rep(candidate["label"].lower())
                    ranked_candidates = []
                    for freebase_id, freebase_labels in candidate["ids"].items():
                        # freebase_label can contain multiple labels
                        # use max sim:
                        max_sim = 0
                        max_label = None
                        for label in freebase_labels:
                            candidate_vector = mc.model().word_rep(label.lower())
                            new_sim = mc.model().vector_cos_sim(label_vector, candidate_vector)
                            if new_sim > max_sim or max_label is None:
                                max_sim = new_sim
                                max_label = label

                        # Only add if a certain threshold is met:
                        if ranking_threshold < max_sim:
                            ranked_candidates.append({
                                "similarity": max_sim,
                                "freebase_id": freebase_id,
                                "freebase_label": max_label
                            })

                    # Sort by similiarty
                    ranked_candidates.sort(key=lambda rank: rank["similarity"], reverse=True)
                    ranking.append({
                        "label": candidate["label"],
                        "type": candidate["type"],
                        "ranked_candidates": ranked_candidates
                    })
            except Exception as e:
                print(e)
            return {"_id": row["_id"], "entities_ranked_candidates": ranking}
        model_path = self.model_root_path
        ranking_threshold = self.ranking_threshold
        self.ranked_entities = self.linked_entities.map(
            lambda row: rank_candidates(row, ModelCache(model_path), ranking_threshold))
        return self.ranked_entities

