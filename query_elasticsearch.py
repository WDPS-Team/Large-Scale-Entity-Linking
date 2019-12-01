import requests
import json

def search(domain, query):
    
    params = ()
    data = {
        "query": { 
            "match": { "label": query }
        },
        "size": 20
    }
    json_qry = json.dumps(data)
    #data = '\n{\n  "query": { "match_all": {} }, "size": 10 \n}'
    url = 'http://%s/freebase/label/_search' % domain
    response = requests.post(url, params=params, data=json_qry)

    # response = requests.get(url, params={'q': query, 'size':10})
    id_labels = {}

    print(response)

    if True:
        print("query run")
        response = response.json()
        print("query json")
        print(response)
        for hit in response.get('hits', {}).get('hits', []):
            freebase_label = hit.get('_source', {}).get('label')
            freebase_id = hit.get('_source', {}).get('resource')
            id_labels.setdefault(freebase_id, set()).add( freebase_label )
    return id_labels

if __name__ == '__main__':
    import sys
    try:
        _, DOMAIN, QUERY = sys.argv
    except Exception as e:
        print('Usage: python elasticsearch.py DOMAIN QUERY')
        sys.exit(0)

    for entity, labels in search(DOMAIN, QUERY).items():
        print(entity, labels)
