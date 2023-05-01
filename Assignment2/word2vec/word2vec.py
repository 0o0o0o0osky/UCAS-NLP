from gensim.models import Word2Vec
import re

lines = []
corpus = []
with open('../cleaned.txt', 'r', encoding='GBK') as f:
    lines = f.read().strip().split('\n')
for line in lines:
    line_words = re.split("[ ]+", line.strip())
    corpus.append(line_words)
for line_words in corpus:
    if '' in line_words:
        line_words.remove('')
corpus = list(filter(None, corpus))

model = Word2Vec(corpus, sg=1, vector_size=200, window=2, min_count=5, hs=1,
                 sample=0.001, workers=4)

model.save('model')
