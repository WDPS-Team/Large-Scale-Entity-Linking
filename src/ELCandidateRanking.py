import json
import trident
from LexVec import ModelCache

class TridentCache:
    def __init__(self, kb_path):
        self.kb_path = kb_path 
        self._kb = None

    def db(self):
        if self._kb is None:
            self._kb = trident.Db(self.kb_path)
            return self._kb
        return self._kb

class ELCandidateRanking:
    def __init__(self, candidates_rdd, kb_path, ranking_threshold, model_root_path):
        self.candidates_rdd = candidates_rdd
        self.kb_path = kb_path
        self.ranking_threshold = ranking_threshold
        self.model_root_path = model_root_path
        
    def rank_entity_candidates(self):
        """
            Rank Entity Candidates by the latent meaning using LexVec.
            - Use threshold on similiarity to reduce candidates.
            - If more labels are present, pick the label similarity with the highest value.
         """
        def rank_candidates(row, mc, ranking_threshold):
            ranking = []
            try:
                for candidate in row["linked_candidates"]:
                    label_vector = mc.model().word_rep(
                        candidate["label"].lower())
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
                    ranked_candidates.sort(
                        key=lambda rank: rank["similarity"], reverse=True)
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
        self.ranked_entities = self.candidates_rdd.map(
            lambda row: rank_candidates(row, ModelCache(model_path), ranking_threshold))
        return self.ranked_entities

    def rank_entity_type(self):

        def get_trident_class_list(e_type):
            switcher = {
                "PERSON"        : ["people.person", "celebrities.celebrity", "book.author", "base.litcentral.named_person", "people.family_member", "government.politician", "business.board_member", "organization.board_member", "organization.leader", "award.award_winner", "business.company_founder", "organization.organization_founder", "education.school_founder"],
                "NORP"          : ["location.location", "location.country"],    # Nationalities or religious or political groups
                "FAC"           : ["architecture.building", "travel.transport_terminus", "aviation.airport", "transportation.road", "transportation.bridge", "common.topic"],    # Buildings, airports, highways, bridges, etc.'
                "ORG"           : ["organization.organization", "business.business_operation", "organization.non_profit_organization", "venture_capital.venture_funded_company"],
                "GPE"           : ["location.location", "location.country", "location.citytown", "location.statistical_region"], # Countries, cities, states
                "LOC"           : ["location.location", "geography.mountain_range", "geography.body_of_water"],    # Non-GPE locations, mountain ranges, bodies of water
                "PRODUCT"       : ["business.consumer_product", "business.brand", "base.tagit.man_made_thing", "base.popstra.product", "common.topic"],
                "EVENT"         : ["common.topic"],
                "WORK_OF_ART"   : ["common.topic", "visual_art.artwork", "exhibitions.exhibit"],
                "LAW"           : ["common.topic"], # Named documents made into laws.
                "LANGUAGE"      : ["common.topic", "language.human_language"]
            }
            return switcher.get(e_type, ["common.topic"])

        def calculate_type_score(response, e_type):    #ALT method to calculate score by taking all query output
            
            class_list = get_trident_class_list(e_type)
            score = 0
            for objects in response["results"]["bindings"]:
                for t_class in class_list:
                    t_class_full = "http://rdf.freebase.com/ns/" + t_class
                    if t_class_full == objects['object']['value'].lower():
                        score = score + 1

            return score

        def get_trident_information(f_id, kb):
            sparql_id = f_id.replace("/",".")     #modify freebase ID for Trident format
            if(sparql_id[0]=="."):
                sparql_id = sparql_id[1:]
            
            q_subject = "<http://rdf.freebase.com/ns/" + sparql_id + ">"
            sparql_query = "SELECT * { ?subject ?predicate ?object } LIMIT 10000".replace("?subject", q_subject)
            
            db = kb.db()
            response = db.sparql(sparql_query)
            response = json.loads(response)
            return response

        def get_label_list(response):
            label_list_class = ['http://rdf.freebase.com/key/wikipedia.en', 'http://rdf.freebase.com/key/en', 'http://rdf.freebase.com/ns/common.topic.alias']

            labels = []
            for bindings in response["results"]["bindings"]:
                if bindings["predicate"]["value"] in label_list_class:
                    labels.append(bindings["object"]["value"].replace("_", " ").lstrip('"').replace('"@en"',''))
            return labels

        def rank_candidates(doc, kb, mc, r_threshold):
            valid_candidates = []
            for entity in doc["entities_ranked_candidates"]:
                type_ranked_ids = []
                label_vector = mc.model().word_rep(entity["label"].lower())
                for candidate in entity["ranked_candidates"]:
                    freebase_id = candidate["freebase_id"]
                    response = get_trident_information(freebase_id, kb)
                    type_score = calculate_type_score(response, entity["type"])
                    
                    label_list = get_label_list(response)
                    max_label = None
                    label_sim = 0
                    for label in label_list:
                        candidate_vector = mc.model().word_rep(label.lower())
                        new_sim = mc.model().vector_cos_sim(label_vector, candidate_vector)
                        if new_sim > label_sim or max_label is None:
                            label_sim = new_sim
                            max_label = label
                    
                    if label_sim > r_threshold:
                        type_ranked_ids.append({ 
                            "freebase_id" : freebase_id,
                            "score"       : type_score,
                            "sim"         : label_sim
                        })
                type_ranked_ids.sort(key=lambda rank: (rank["sim"], rank["score"]), reverse=True)
                valid_candidates.append({"label": entity["label"], "type": entity["type"], "ranked_candidates": type_ranked_ids })
            
            return {"_id": doc["_id"], "entities_ranked_candidates": valid_candidates}
        
        kb_path = self.kb_path
        model_path = self.model_root_path
        ranking_threshold = self.ranking_threshold

        lambda_map = lambda doc : rank_candidates(doc, TridentCache(kb_path), ModelCache(model_path), ranking_threshold)
        self.ranked_entities = self.ranked_entities.map(lambda_map)

        return self.ranked_entities