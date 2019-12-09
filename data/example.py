
from model import Model
model = Model('lexvec.commoncrawl.ngramsubwords.300d.W.pos.bin')
vector1 = model.word_rep('Walt Disney World')
vector2 = model.word_rep('WDW')
print(model.vector_cos_sim(vector1, vector2))

# Slowly implemented
windex = model.most_similar("USA")
print(windex)
print(model.get_word(windex))
