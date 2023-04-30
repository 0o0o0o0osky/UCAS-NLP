import gensim

# 加载模型
model = gensim.models.Word2Vec.load('model')

# 获取词汇
# words = model.wv.index_to_key
# print(words)


most_similar = model.wv.similar_by_word('青年')

for i in range(10):
    print(most_similar[i][0], most_similar[i][1])
