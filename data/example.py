
from model import Model
model = Model('lexvec.commoncrawl.ngramsubwords.300d.W.pos.bin')
vector1 = model.word_rep('Walt Disney World')
vector2 = model.word_rep('WDW')
print(model.vector_cos_sim(vector1, vector2))

# Slowly implemented
word = "London"
windex = model.most_similar(word)
print(windex)
print(model.get_word(windex))
print(model.vector_cos_sim(model.word_rep(word), model.word_rep(model.get_word(windex))))
