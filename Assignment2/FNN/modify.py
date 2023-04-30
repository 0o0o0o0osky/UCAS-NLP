import pandas as pd
from collections import OrderedDict

# 原始输出的word_vectors.csv不太好用，补救一下
df = pd.read_csv('word_vectors.csv', header=None, names=['vec0', 'vec1', 'vec2', 'vec3', 'vec4', 'vec5', 'vec6', 'vec7', 'vec8', 'vec9'])
f = open('../cleaned.txt', 'r', encoding='GBK')
text = f.read()
corpus = text.split()
words_set = list(OrderedDict.fromkeys(corpus).keys())
df.insert(0, 'word', '')
df['word'] = words_set
df.to_csv('modified.csv', index=False, encoding='GBK')

