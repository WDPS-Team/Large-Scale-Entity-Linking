class ELMappingSelection():

    def __init__(self, ranked_entities):
        self.ranked_entities = ranked_entities

    def select(self):

        def expand(row):
            result = []
            for candidate in row["entities_ranked_candidates"]:
                if len(candidate["ranked_candidates"]) > 0:
                    result.append({"_id": row["_id"], "id": candidate["ranked_candidates"][0]["freebase_id"], "label": candidate["label"]})   #only include the best ranked freebase ID
            return result

        self.selected = self.ranked_entities.flatMap(expand)
        return self.selected

