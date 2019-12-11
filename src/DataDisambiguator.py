import requests
import json
import time

class DataDisambiguator:
    def __init__(self, linked_rdd, kb_path):
        self.linked_rdd = linked_rdd
        self.kb_path    = kb_path
    
    def disambiguate(self):

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
            for _ in range(10):
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
                    valid_ids.append(list(entity["ranked_candidates"][0]["freebase_id"]))
                valid_candidates.append({"label": entity["label"], "ids": valid_ids })
            

            return {"_id": doc["_id"], "entities": valid_candidates}
        

        kb_path = self.kb_path
        lambda_map = lambda doc : disambiguate_doc(doc, kb_path)
        valid_entities = self.linked_rdd.map(lambda_map)

        return valid_entities
