import requests
import json
import time
from LexVec import ModelCache

class DataDisambiguator:
    def __init__(self, linked_rdd, kb_path, ranking_threshold, model_root_path):
        self.linked_rdd        = linked_rdd
        self.kb_path           = kb_path
        self.ranking_threshold = ranking_threshold
        self.model_root_path   = model_root_path


    def disambiguate_label(self):

        def getLabelList(sparql_query, kb_path):
            url = 'http://{0}/sparql'.format(kb_path)
            response = None
            for _ in range(30):
                try:
                    response = requests.post(url, data={'print': True, 'query': sparql_query})
                    break
                except:
                    time.sleep(0.1)
            
            labelList = []
            response = response.json()
            for objects in response["results"]["bindings"]:
                labelList.append(objects["object"]["value"].strip('\"').replace("_", " "))
            return labelList
                
        def getTridentLabels(freebase_id, kb_path):
            sparql_id = freebase_id.replace("/",".")     #modify freebase ID for Trident format
            if(sparql_id[0]=="."):
                sparql_id = sparql_id[1:]
            
            q_subject   = "<http://rdf.freebase.com/ns/" + sparql_id + ">"
            q_predicate = "<http://rdf.freebase.com/key/wikipedia.en>"      # TODO: add <http://rdf.freebase.com/key/en> also??

            sparql_query = "SELECT * { ?subject ?predicate ?object } LIMIT 30".replace("?subject", q_subject).replace("?predicate", q_predicate)

            return getLabelList(sparql_query, kb_path)


        def rank_candidates(row, mc, ranking_threshold, kb_path):
            ranking = []
            try:
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
                        if ranking_threshold < max_sim:
                            ranked_candidates.append({
                                "similarity": max_sim,
                                "freebase_id": freebase_id,
                                "trident_label": max_label
                            })

                    # Sort by similiarty
                    ranked_candidates.sort(key=lambda rank: rank["similarity"], reverse=True)
                    ranking.append({
                        "label": entity["label"],
                        "type": entity["type"],
                        "ranked_candidates": ranked_candidates
                    })
            except Exception as e:
                print(e)
            return {"_id": row["_id"], "entities_ranked_candidates": ranking}

        kb_path           = self.kb_path
        model_path        = self.model_root_path
        ranking_threshold = self.ranking_threshold
        
        self.ranked_entities = self.linked_rdd.map(
            lambda row: rank_candidates(row, ModelCache(model_path), ranking_threshold, kb_path))
        return self.ranked_entities

    def disambiguate_type(self):

        def getTridentClass(type):
            class_type = "common.topic"
            if(type == "PERSON"):
                class_type = "people.person"
            elif(type == "GPE" or type ==  "LOC"):
                class_type = "location.location"
            elif(type == "ORG"):
                class_type = "organization.organization"
            return class_type

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
                return True
            except:
                return False
            

        def validate(id, type, kb_path):
            sparql_id = id.replace("/",".")     #modify freebase ID for Trident format
            if(sparql_id[0]=="."):
                sparql_id = sparql_id[1:]
            
            q_subject = "<http://rdf.freebase.com/ns/" + sparql_id + ">"
            q_object  = "<http://rdf.freebase.com/ns/" + getTridentClass(type) + ">"

            sparql_query = "SELECT * { ?subject ?predicate ?object } LIMIT 1".replace("?subject", q_subject).replace("?object", q_object)
            return checkRelation(sparql_query, kb_path)
            
        def disambiguate_doc(doc, kb_path):
            valid_candidates = []
            for entity in doc["entities_ranked_candidates"]:
                valid_ids = []
                for candidate in entity["ranked_candidates"]:
                    freebase_id = candidate["freebase_id"]
                    if(validate(freebase_id, entity["type"], kb_path)):   #validate the id with type using Trident
                        valid_ids.append(freebase_id)
                        break
                if len(valid_ids) == 0 and len(entity["ranked_candidates"]) > 0:   #add the id with the best score incase Trident is unable to come up with a best match
                    valid_ids.append(entity["ranked_candidates"][0]["freebase_id"])
                valid_candidates.append({"label": entity["label"], "ids": valid_ids })
            

            return {"_id": doc["_id"], "entities": valid_candidates}
        

        kb_path = self.kb_path
        lambda_map = lambda doc : disambiguate_doc(doc, kb_path)
        valid_entities = self.ranked_entities.map(lambda_map)

        return valid_entities