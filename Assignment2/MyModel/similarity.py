import csv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 读取词向量 CSV 文件
word_vectors = []
words = []
with open('modified_word_vectors.csv', 'r', encoding='GBK') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i == 0:
            continue  # 跳过表头
        word_vectors.append([float(x) for x in row[1:]])
        words.append(row[0])

# 计算一个单词w和其他单词的相似度
def find_similar_words(w, k=10):
    index = words.index(w)
    if index == -1:
        return []
    v1 = word_vectors[index]
    sims = []
    for i in range(len(words)):
        if i == index:
            continue
        v2 = word_vectors[i]
        sim = cosine_similarity(np.array(v1).reshape(1, -1), np.array(v2).reshape(1, -1))
        sims.append((words[i], sim.item()))
    sims = sorted(sims, key=lambda x: x[1], reverse=True)[:k]
    return sims

# 测试代码
similar_words = find_similar_words('青年')
print(similar_words)
