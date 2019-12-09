import gensim 
from gensim.models import Word2Vec

class ModelCache:
    def __init__(self, model_root_path):
        self.model_root_path = model_root_path
        self.model = None

    def w2v(self):
        if self.model is None:
            self.model = gensim.models.KeyedVectors.load_word2vec_format(self.model_root_path + '/GoogleNews-vectors-negative300.bin', binary=True)  
        return self.model