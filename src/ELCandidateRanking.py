import requests
import json
import time
from LexVec import ModelCache


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

    def disambiguate_type(self):

        def getTridentClassList(e_type):    #TODO: Add more classes to this
            switcher = {
                "PERSON"        : ["people.person", "celebrities.celebrity", "common.topic", "book.author", "base.litcentral.named_person", "people.family_member", "government.politician", "business.board_member", "organization.board_member", "organization.leader", "award.award_winner", "business.company_founder", "organization.organization_founder", "education.school_founder"],
                "NORP"          : ["location.location", "location.country", "people.ethnicity", "people.ethnicity.geographic_distribution", "people.ethnicity.languages_spoken", "common.topic"],    # Nationalities or religious or political groups
                "FAC"           : ["architecture.building", "travel.transport_terminus", "aviation.airport", "transportation.road", "transportation.bridge"],    # Buildings, airports, highways, bridges, etc.'
                "ORG"           : ["organization.organization", "business.business_operation", "organization.non_profit_organization", "venture_capital.venture_funded_company"],
                "GPE"           : ["location.location", "location.country", "location.citytown", "location.statistical_region"], # Countries, cities, states
                "LOC"           : ["location.location", "geography.mountain_range", "common.topic", "geography.body_of_water"],    # Non-GPE locations, mountain ranges, bodies of water
                "PRODUCT"       : ["business.consumer_product", "business.brand", "base.tagit.man_made_thing", "base.popstra.product"],
                "EVENT"         : ["common.topic"],
                "WORK_OF_ART"   : ["common.topic"],
                "LAW"           : ["common.topic"], # Named documents made into laws.
                "LANGUAGE"      : ["common.topic", "language.human_language"]
            }
            return switcher.get(e_type, ["common.topic"])

        def checkRelation(sparql_query, kb_path):
            url = 'http://{0}/sparql'.format(kb_path)
            response = None
            for _ in range(30):
                try:
                    response = requests.post(url, data={'print': True, 'query': sparql_query})
                    break
                except:
                    time.sleep(0.1)

            try:
                response = response.json()
                res = response["results"]["bindings"][0]["predicate"]
                return 1
            except:
                return 0
            

        def validateType(f_id, t_class, kb_path):
            sparql_id = f_id.replace("/",".")     #modify freebase ID for Trident format
            if(sparql_id[0]=="."):
                sparql_id = sparql_id[1:]
            
            q_subject = "<http://rdf.freebase.com/ns/" + sparql_id + ">"
            q_object  = "<http://rdf.freebase.com/ns/" + t_class + ">"

            sparql_query = "SELECT * { ?subject ?predicate ?object } LIMIT 1".replace("?subject", q_subject).replace("?object", q_object)
            return checkRelation(sparql_query, kb_path)
            
        def calculate_type_score(f_id, e_type, kb_path):
            trident_class_list = getTridentClassList(e_type)
            score = 0
            for t_class in trident_class_list:
                score = score + validateType(f_id, t_class, kb_path)

            return score

        def disambiguate_doc(doc, kb_path):
            valid_candidates = []
            for entity in doc["entities_ranked_candidates"]:
                type_scored_ids = []
                for candidate in entity["ranked_candidates"]:
                    freebase_id = candidate["freebase_id"]
                    type_score = calculate_type_score(freebase_id, entity["type"], kb_path)   #calculate type score using Trident
                    if type_score > 0:
                        type_scored_ids.append({ 
                            "freebase_id" : freebase_id,
                            "score"       : type_score
                        })
                type_scored_ids.sort(key=lambda rank: rank["score"], reverse=True)
                valid_candidates.append({"label": entity["label"], "type": entity["type"], "ranked_candidates": type_scored_ids })
            
            return {"_id": doc["_id"], "entities_ranked_candidates": valid_candidates}
        

        kb_path = self.kb_path
        lambda_map = lambda doc : disambiguate_doc(doc, kb_path)
        self.ranked_entities = self.ranked_entities.map(lambda_map)

        return self.ranked_entities

    def disambiguate_label(self):

        def getLabelList(sparql_query, kb_path):
            url = 'http://{0}/sparql'.format(kb_path)
            response = None
            for _ in range(50):
                try:
                    response = requests.post(url, data={'print': True, 'query': sparql_query})
                    break
                except:
                    time.sleep(0.1)
            
            labelList = []
            try:
                response = response.json()
                for objects in response["results"]["bindings"]:
                    labelList.append(objects["object"]["value"].strip('\"').replace("_", " "))
            except Exception as e:
                print(e)
            return labelList
                
        def getTridentLabels(freebase_id, kb_path):
            sparql_id = freebase_id.replace("/",".")     #modify freebase ID for Trident format
            if(sparql_id[0]=="."):
                sparql_id = sparql_id[1:]
            
            q_subject     = "<http://rdf.freebase.com/ns/" + sparql_id + ">"
            default_query = "SELECT * { ?subject ?predicate ?object } LIMIT 30"
            sparql_query  = default_query.replace("?subject", q_subject).replace("?predicate", "<http://rdf.freebase.com/key/wikipedia.en>")
            sparql_query2 = default_query.replace("?subject", q_subject).replace("?predicate", "<http://rdf.freebase.com/key/en>")  #TODO: Combine the separate queries to one query

            return getLabelList(sparql_query, kb_path) + getLabelList(sparql_query2, kb_path)


        def rank_candidates(row, mc, ranking_threshold, kb_path):
            ranking = []
            for entity in row["entities_ranked_candidates"]:
                label_vector = mc.model().word_rep(entity["label"].lower())
                ranked_candidates = []
                for candidate in entity["ranked_candidates"]:
                    freebase_id = candidate["freebase_id"]
                    max_sim = 0
                    max_label = None
                    for label in getTridentLabels(freebase_id, kb_path):
                        candidate_vector = mc.model().word_rep(label.lower())
                        new_sim = mc.model().vector_cos_sim(label_vector, candidate_vector)
                        if new_sim > max_sim or max_label is None:
                            max_sim = new_sim
                            max_label = label

                    # Only add if a certain threshold is met:
                    if ranking_threshold <= max_sim:
                        ranked_candidates.append({
                            "similarity": max_sim,
                            "freebase_id": freebase_id,
                            "trident_label": max_label
                        })

                # Sort by similiarty
                ranked_candidates.sort(key=lambda rank: rank["similarity"], reverse=True)
                ranking.append({
                    "label": entity["label"],
                    "type" : entity["type"],
                    "ranked_candidates": ranked_candidates
                })
            return {"_id": row["_id"], "entities_ranked_candidates": ranking}

        kb_path           = self.kb_path
        model_path        = self.model_root_path
        ranking_threshold = self.ranking_threshold
        
        self.ranked_entities = self.ranked_entities.map(
            lambda row: rank_candidates(row, ModelCache(model_path), ranking_threshold, kb_path))
        return self.ranked_entities