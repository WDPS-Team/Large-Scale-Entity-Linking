import sys
from elasticsearch import Elasticsearch
import json

def load_file(es_host, filepath):
    file= open(filepath,'r').read()
    lines = file.splitlines(True)
    for i, line in enumerate(lines):
        freebase_label, freebase_id = line.split("\t")
        freebase_id = freebase_id.strip()
        if (freebase_label):
            body = {"label": freebase_label, "resource": freebase_id}
            es_host.index(index='freebase', doc_type='label', id=i, body=body )

if __name__ == '__main__':
    try:
        _, HOST, PORT, INFILE = sys.argv
        es = Elasticsearch(
            [HOST],
            port=PORT
        )
    except Exception as e:
        print('Usage: python HOST PORT FILE')
        sys.exit(0)

    load_file(es, INFILE)