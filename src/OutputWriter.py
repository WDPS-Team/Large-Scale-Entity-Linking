class OutputWriter():

    def __init__(self, selected_entities):
        self.selected_entities = selected_entities

    def convert_to_tsv(self):
        # doc id tab surface form tab id

        def to_tsv(row):
            return "{0}\t{1}\t{2}".format(row["_id"].strip(), row["label"].strip(), row["id"].strip())

        return self.selected_entities.map(to_tsv)
