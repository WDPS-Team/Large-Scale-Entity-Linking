import requests
import time
from config import FREEBASE_DOMAIN, FREEBASE_RETRY_COUNT, FREEBASE_RETRY_GAP

def search(query):
    url = 'http://%s/freebase/label/_search' % FREEBASE_DOMAIN
    response=None
    for _ in range(FREEBASE_RETRY_COUNT):
        try:
            response = requests.get(url, params={'q': query, 'size':1000})
            break
        except:
            time.sleep(FREEBASE_RETRY_GAP)
        
    id_labels = {}
    if response:
        response = response.json()
        for hit in response.get('hits', {}).get('hits', []):
            freebase_label = hit.get('_source', {}).get('label')
            freebase_id = hit.get('_source', {}).get('resource')
            id_labels.setdefault(freebase_id, set()).add( freebase_label )
    return id_labels

if __name__ == '__main__':
    import sys
    try:
        QUERY = sys.argv[1]
    except Exception as e:
        print("Usage: QUERY. Using 'Obama' as query instead")
        QUERY = "obama"

    for entity, labels in search(QUERY).items():
        print(entity, labels)