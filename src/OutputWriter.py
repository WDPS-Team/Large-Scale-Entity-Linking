class OutputWriter():

    def __init__(self, linked_entities):
        self.linked_entities = linked_entities

    def transform(self):

        def expand(row):
            # expand following row: {'linked_candidates': [{'ids': {}, 'label': 'XML-RPC'}, {'ids': {'/m/05p7hcr': {
            # 'Post'}, '/m/02hckn': {'Post'}, '/m/0px38': {'Washington Post'}, '/m/0px3s': {'NY Post',
            # 'New YORK POST'}}, 'label': 'POST'}], 'doc_id': 'clueweb12-0000tw-00-00005'}

            result = []
            for candidate in row["entities_ranked_candidates"]:
                # Only Output best candidate:
                if len(candidate["ranked_candidates"]) > 0:
                    freebase_entity = candidate["ranked_candidates"][0]
                    result.append({"_id": row["_id"], "id": freebase_entity["freebase_id"], "label": candidate["label"]})
            # for candidate in row["linked_candidates"]:
            #     for id in candidate["ids"]:
            #         result.append({"_id": row["_id"], "id": id, "label": candidate["label"]})
            return result

        self.expanded = self.linked_entities.flatMap(expand)
        return self.expanded

    def convert_to_tsv(self):
        # doc id tab surface form tab id

        def to_tsv(row):
            return "{0}\t{1}\t{2}".format(row["_id"].strip(), row["label"].strip(), row["id"].strip())

        return self.expanded.map(to_tsv)
